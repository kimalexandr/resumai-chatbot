// Функции для чата и загрузки файлов
const chatBox = document.getElementById("chat-box");
const fileUpload = document.getElementById("file-upload");
const vacancyLink = document.getElementById("vacancy-link");
const resumeText = document.getElementById("resume-text");
const userInput = document.getElementById("user-input");

// Добавление сообщений в чат
function addMessage(sender, text) {
    console.log(`Добавляю сообщение: ${sender} - ${text}`);
    const msg = document.createElement("div");
    msg.className = sender === "bot" ? "bot-msg" : "user-msg";
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Отправка сообщений в чат
async function sendMessage(message, type = "chat") {
    console.log(`Отправляю сообщение: ${message} (тип: ${type})`);
    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, type })
        });
        console.log(`Получен ответ:`, response);
        const data = await response.json();
        console.log(`Данные ответа:`, data);
        
        if (data.success === false) {
            addMessage("bot", `❌ Ошибка: ${data.error}`);
        } else {
            addMessage("bot", data.reply);
        }
    } catch (error) {
        console.error(`Ошибка при отправке:`, error);
        addMessage("bot", `❌ Ошибка соединения: ${error.message}`);
    }
}

// Загрузка файла резюме
async function uploadFile() {
    console.log("Функция uploadFile вызвана");
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
    console.log("Функция analyzeVacancy вызвана");
    const link = vacancyLink.value.trim();
    if (!link) {
        alert("Введите ссылку на вакансию");
        return;
    }
    
    console.log(`Анализирую вакансию: ${link}`);
    addMessage("user", `🔗 Анализирую вакансию: ${link}`);
    await sendMessage(link, "vacancy");
    vacancyLink.value = "";
}

// Анализ текста резюме
async function analyzeText() {
    console.log("Функция analyzeText вызвана");
    const text = resumeText.value.trim();
    if (!text) {
        alert("Введите текст резюме");
        return;
    }
    
    console.log(`Анализирую текст резюме`);
    addMessage("user", `💬 Анализирую текст резюме`);
    await sendMessage(text, "resume");
    resumeText.value = "";
}

// Отправка сообщения в чат
async function sendChatMessage() {
    console.log("Функция sendChatMessage вызвана");
    const message = userInput.value.trim();
    if (!message) {
        alert("Введите сообщение");
        return;
    }
    
    console.log(`Отправляю сообщение в чат: ${message}`);
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

// Обработка изменения файла
fileUpload.addEventListener("change", function(e) {
    const file = e.target.files[0];
    if (file) {
        // Показываем имя выбранного файла
        const label = document.querySelector('.file-label span');
        if (label) {
            label.textContent = `Выбран: ${file.name}`;
        }
    }
});

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM загружен, инициализирую chat.js...');
    
    // Проверяем, что все элементы существуют
    if (!chatBox) console.error('chat-box не найден');
    if (!fileUpload) console.error('file-upload не найден');
    if (!vacancyLink) console.error('vacancy-link не найден');
    if (!resumeText) console.error('resume-text не найден');
    if (!userInput) console.error('user-input не найден');
    
    if (!chatBox || !fileUpload || !vacancyLink || !resumeText || !userInput) {
        console.error('Не все элементы найдены на странице');
        return;
    }
    
    console.log('Chat.js загружен успешно');
    console.log('Все элементы найдены:', {
        chatBox: !!chatBox,
        fileUpload: !!fileUpload,
        vacancyLink: !!vacancyLink,
        resumeText: !!resumeText,
        userInput: !!userInput
    });
});
