// Функции для личного кабинета
let currentResumes = [];

// Загрузка резюме при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadResumes();
    updateStats();
});

// Загрузка резюме с фильтрами
async function loadResumes() {
    const fromDate = document.getElementById('date-from').value;
    const toDate = document.getElementById('date-to').value;
    const vacancyFilter = document.getElementById('vacancy-filter').value;

    let url = '/api/resumes?';
    if (fromDate) url += `&from=${fromDate}`;
    if (toDate) url += `&to=${toDate}`;
    if (vacancyFilter) url += `&vacancy=${encodeURIComponent(vacancyFilter)}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        currentResumes = data;
        displayResumes(data);
        updateStats();
    } catch (error) {
        console.error('Error loading resumes:', error);
        showError('Ошибка загрузки резюме: ' + error.message);
    }
}

// Отображение резюме
function displayResumes(resumes) {
    const container = document.getElementById('resumes-list');
    
    if (resumes.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    <i class="fas fa-file-alt"></i>
                </div>
                <h3>Резюме не найдены</h3>
                <p>Попробуйте изменить фильтры или создайте новое резюме</p>
                <a href="/" class="btn btn-primary">
                    <i class="fas fa-plus"></i>
                    Создать резюме
                </a>
            </div>
        `;
        return;
    }

    container.innerHTML = resumes.map(resume => `
        <div class="resume-card" data-id="${resume.id}">
            <div class="resume-header">
                <div class="resume-date">
                    <i class="fas fa-calendar"></i>
                    ${formatDate(resume.created_at)}
                </div>
                <div class="resume-actions">
                    <button onclick="viewResume(${resume.id})" class="btn btn-sm btn-secondary" title="Просмотр">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button onclick="downloadPDF(${resume.id})" class="btn btn-sm btn-primary" title="Скачать PDF">
                        <i class="fas fa-download"></i>
                    </button>
                    <button onclick="deleteResume(${resume.id})" class="btn btn-sm btn-danger" title="Удалить">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            
            <div class="resume-content">
                <div class="resume-preview">
                    ${truncateText(resume.content, 200)}
                </div>
                
                ${resume.vacancy_link ? `
                    <div class="resume-vacancy">
                        <i class="fas fa-link"></i>
                        <span>Адаптировано под: ${resume.vacancy_link}</span>
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

// Просмотр резюме
function viewResume(resumeId) {
    const resume = currentResumes.find(r => r.id === resumeId);
    if (!resume) return;

    // Создаем модальное окно для просмотра
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Резюме от ${formatDate(resume.created_at)}</h3>
                <button onclick="closeModal()" class="close-btn">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <div class="resume-full-content">
                    <pre>${resume.content}</pre>
                </div>
                ${resume.vacancy_link ? `
                    <div class="resume-vacancy-info">
                        <strong>Адаптировано под:</strong>
                        <a href="${resume.vacancy_link}" target="_blank">${resume.vacancy_link}</a>
                    </div>
                ` : ''}
            </div>
            <div class="modal-footer">
                <button onclick="downloadPDF(${resume.id})" class="btn btn-primary">
                    <i class="fas fa-download"></i>
                    Скачать PDF
                </button>
                <button onclick="closeModal()" class="btn btn-secondary">
                    Закрыть
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'flex';
}

// Закрытие модального окна
function closeModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.remove();
    }
}

// Скачивание PDF
function downloadPDF(resumeId) {
    const resume = currentResumes.find(r => r.id === resumeId);
    if (!resume) return;

    // Простое создание PDF через браузер
    const content = `
        Резюме от ${formatDate(resume.created_at)}
        
        ${resume.content}
        
        ${resume.vacancy_link ? `Адаптировано под: ${resume.vacancy_link}` : ''}
    `;

    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `resume_${resumeId}_${formatDate(resume.created_at)}.txt`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Удаление резюме
async function deleteResume(resumeId) {
    if (!confirm('Вы уверены, что хотите удалить это резюме?')) {
        return;
    }

    try {
        const response = await fetch(`/api/resumes/${resumeId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            // Удаляем из списка и обновляем отображение
            currentResumes = currentResumes.filter(r => r.id !== resumeId);
            displayResumes(currentResumes);
            updateStats();
            showSuccess('Резюме успешно удалено');
        } else {
            throw new Error('Ошибка удаления');
        }
    } catch (error) {
        console.error('Error deleting resume:', error);
        showError('Ошибка удаления резюме');
    }
}

// Применение фильтров
function applyFilters() {
    loadResumes();
}

// Обновление резюме
function refreshResumes() {
    loadResumes();
}

// Обновление статистики
function updateStats() {
    document.getElementById('total-resumes').textContent = currentResumes.length;
    document.getElementById('total-analyses').textContent = currentResumes.filter(r => r.vacancy_link).length;
}

// Вспомогательные функции
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Показываем уведомление
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Скрываем через 3 секунды
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Закрытие модального окна по клику вне его
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        closeModal();
    }
});
