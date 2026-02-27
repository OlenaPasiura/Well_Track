// ===================================
// WEll-track Main JavaScript
// ===================================

// LocalStorage keys
const STORAGE_KEYS = {
    USER: 'welltrack_user',
    STRESS_DATA: 'welltrack_stress',
    SLEEP_DATA: 'welltrack_sleep',
    NUTRITION_DATA: 'welltrack_nutrition',
    CHAT_DATA: 'welltrack_chat'
};

// Get current user
function getCurrentUser() {
    const userStr = localStorage.getItem(STORAGE_KEYS.USER);
    return userStr ? JSON.parse(userStr) : null;
}

// Set current user
function setCurrentUser(user) {
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
}

// Check if user is authenticated
function isAuthenticated() {
    return getCurrentUser() !== null;
}

// Logout function
function logout() {
    localStorage.removeItem(STORAGE_KEYS.USER);
    // ✅ Django home route
    window.location.href = '/';
}

// Protect page (redirect if not authenticated)
function protectPage() {
    if (!isAuthenticated()) {
        // ✅ Django home route
        window.location.href = '/';
    }
}

// Initialize logout button
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }

    // Show/hide navigation items based on user type
    const user = getCurrentUser();
    if (user) {
        const chatNavItem = document.getElementById('chatNavItem');
        const responsesNavItem = document.getElementById('responsesNavItem');

        if (user.userType === 'dietitian') {
            if (chatNavItem) chatNavItem.classList.add('d-none');
            if (responsesNavItem) responsesNavItem.classList.remove('d-none');
        } else {
            if (chatNavItem) chatNavItem.classList.remove('d-none');
            if (responsesNavItem) responsesNavItem.classList.add('d-none');
        }
    }

    // AI Assistant functionality
    const aiAssistantBtn = document.getElementById('aiAssistantBtn');
    const aiModal = document.getElementById('aiModal');
    const aiSendBtn = document.getElementById('aiSendBtn');
    const aiInput = document.getElementById('aiInput');
    const aiChatBody = document.getElementById('aiChatBody');

    if (aiAssistantBtn && aiModal) {
        aiAssistantBtn.addEventListener('click', function() {
            const modal = new bootstrap.Modal(aiModal);
            modal.show();
        });
    }

    if (aiSendBtn && aiInput && aiChatBody) {
        function sendAIMessage() {
            const message = aiInput.value.trim();
            if (message) {
                // Add user message
                const userMsg = document.createElement('div');
                userMsg.className = 'user-message';
                userMsg.innerHTML = '<strong>Ви:</strong> ' + message;
                aiChatBody.appendChild(userMsg);

                aiInput.value = '';

                // Simulate AI response
                setTimeout(function() {
                    const aiMsg = document.createElement('div');
                    aiMsg.className = 'ai-message';
                    aiMsg.innerHTML = '<strong>AI:</strong> ' + getAIResponse(message);
                    aiChatBody.appendChild(aiMsg);
                    aiChatBody.scrollTop = aiChatBody.scrollHeight;
                }, 1000);
            }
        }

        aiSendBtn.addEventListener('click', sendAIMessage);
        aiInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendAIMessage();
            }
        });
    }
});

// Simple AI response generator
function getAIResponse(message) {
    const responses = {
        'стрес': 'Рекомендую практикувати техніки релаксації, такі як глибоке дихання або медитація.',
        'сон': 'Важливо дотримуватися регулярного графіку сну. Намагайтеся лягати і прокидатися в один і той же час.',
        'харчування': 'Збалансоване харчування включає білки, жири та вуглеводи. Не забувайте про овочі та фрукти!',
        'допомога': 'Я можу допомогти вам з питаннями про стрес, сон, харчування та загальне здоров\'я.',
        'привіт': 'Привіт! Чим можу допомогти?',
        'дякую': 'Будь ласка! Звертайтеся, якщо виникнуть питання.'
    };

    const lowerMessage = message.toLowerCase();

    for (const key in responses) {
        if (lowerMessage.includes(key)) {
            return responses[key];
        }
    }

    return 'Дякую за ваше повідомлення. Я тут, щоб допомогти вам з питаннями здоров\'я!';
}

// Get or initialize data
function getData(key, defaultValue = []) {
    const dataStr = localStorage.getItem(key);
    return dataStr ? JSON.parse(dataStr) : defaultValue;
}

// Save data
function saveData(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
}

// Format date
function formatDate(date) {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return day + '.' + month + '.' + year;
}

// Get today's date string
function getTodayString() {
    const today = new Date();
    return today.toISOString().split('T')[0];
}
