const chatBox = document.getElementById("chat-box");
const fileUpload = document.getElementById("file-upload");
const vacancyLink = document.getElementById("vacancy-link");
const resumeText = document.getElementById("resume-text");
const userInput = document.getElementById("user-input");

function addMessage(sender, text) {
  const msg = document.createElement("div");
  msg.className = sender === "bot" ? "bot-msg" : "user-msg";
  msg.innerText = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(message, type = "chat") {
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, type })
    });
    const data = await response.json();
    
    if (data.success === false) {
      addMessage("bot", `❌ Ошибка: ${data.error}`);
    } else {
      addMessage("bot", data.reply);
    }
  } catch (error) {
    addMessage("bot", `❌ Ошибка соединения: ${error.message}`);
  }
}

// Загрузка файла резюме
async function uploadFile() {
  const file = fileUpload.files[0];
  if (!file) {
    alert("Выберите файл для загрузки");
    return;
  }
  
  addMessage("user", `📄 Загружаю файл: ${file.name}`);
  
  const formData = new FormData();
  formData.append("file", file);
  
  try {
    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData
    });
    
    const data = await response.json();
    if (data.success) {
      addMessage("bot", data.reply);
    } else {
      addMessage("bot", `❌ Ошибка: ${data.error}`);
    }
  } catch (error) {
    addMessage("bot", `❌ Ошибка загрузки: ${error.message}`);
  }
}

// Анализ вакансии по ссылке
async function analyzeVacancy() {
  const link = vacancyLink.value.trim();
  if (!link) {
    alert("Введите ссылку на вакансию");
    return;
  }
  
  addMessage("user", `🔗 Анализирую вакансию: ${link}`);
  await sendMessage(link, "vacancy");
  vacancyLink.value = "";
}

// Анализ текста резюме
async function analyzeText() {
  const text = resumeText.value.trim();
  if (!text) {
    alert("Введите текст резюме");
    return;
  }
  
  addMessage("user", `💬 Анализирую текст резюме`);
  await sendMessage(text, "resume");
  resumeText.value = "";
}

// Отправка сообщения в чат
async function sendChatMessage() {
  const message = userInput.value.trim();
  if (!message) {
    alert("Введите сообщение");
    return;
  }
  
  addMessage("user", message);
  await sendMessage(message, "chat");
  userInput.value = "";
}

// Обработка Enter для чата
userInput.addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    sendChatMessage();
  }
});

// Обработка Enter для текста резюме
resumeText.addEventListener("keypress", function(e) {
  if (e.key === "Enter" && e.ctrlKey) {
    analyzeText();
  }
});

// Обработка Enter для ссылки на вакансию
vacancyLink.addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    analyzeVacancy();
  }
});