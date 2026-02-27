// ===================================
// WEll-track Chat page
// ===================================

document.addEventListener('DOMContentLoaded', function () {

    // 🔐 захист сторінки
    protectPage();

    loadMessages();

    const sendBtn = document.getElementById('sendBtn');
    const input = document.getElementById('messageInput');

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage();
    });
});


// Завантаження історії повідомлень
function loadMessages() {
    const chatData = getData(STORAGE_KEYS.CHAT_DATA, []);
    const chatMessages = document.getElementById('chatMessages');

    chatMessages.innerHTML = "";

    // перше повідомлення бота
    addMessageToUI(
        "Вітаю! Я ваш дієтолог. Чим можу допомогти?",
        "received",
        new Date().toISOString()
    );

    chatData.forEach(msg => {
        addMessageToUI(msg.text, msg.type, msg.timestamp);
    });
}


// Надсилання повідомлення
function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    if (!message) return;

    const timestamp = new Date().toISOString();
    const chatData = getData(STORAGE_KEYS.CHAT_DATA, []);

    // повідомлення користувача
    chatData.push({
        text: message,
        type: 'sent',
        timestamp: timestamp
    });

    saveData(STORAGE_KEYS.CHAT_DATA, chatData);
    addMessageToUI(message, 'sent', timestamp);

    input.value = "";

    // 🤖 фейкова відповідь дієтолога
    setTimeout(() => {
        const response = getDietitianReply(message);
        const respTime = new Date().toISOString();

        chatData.push({
            text: response,
            type: 'received',
            timestamp: respTime
        });

        saveData(STORAGE_KEYS.CHAT_DATA, chatData);
        addMessageToUI(response, 'received', respTime);
    }, 1000);
}


// Відображення повідомлення в чаті
function addMessageToUI(text, type, timestamp) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + type;

    const time = new Date(timestamp);
    const timeStr = time.getHours() + ':' + String(time.getMinutes()).padStart(2, '0');

    messageDiv.innerHTML =
        `<div class="message-bubble">${text}</div>
         <div class="message-time">Сьогодні, ${timeStr}</div>`;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// Простий бот-дієтолог (тимчасово)
function getDietitianReply(message) {
    const msg = message.toLowerCase();

    if (msg.includes("калор")) return "Рекомендую почати з норми 2000 ккал на день.";
    if (msg.includes("схуд")) return "Для схуднення важливий дефіцит калорій і регулярність.";
    if (msg.includes("набір")) return "Для набору ваги збільш калорійність і білок.";
    if (msg.includes("біл")) return "Норма білка ≈ 1.6–2 г на кг ваги.";
    if (msg.includes("прив")) return "Привіт 🙂 Чим можу допомогти щодо харчування?";

    return "Дякую за повідомлення! Скоро додамо справжній чат із бекендом 🙂";
}
