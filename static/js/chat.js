// ===================================
// Chat page logic (frontend only)
// ===================================

document.addEventListener("DOMContentLoaded", async function () {
    protectPage();

    await loadMessages();

    document.getElementById("sendBtn").addEventListener("click", sendMessage);
    document.getElementById("messageInput").addEventListener("keypress", function (e) {
        if (e.key === "Enter") sendMessage();
    });
});

async function loadMessages() {
    const chatMessages = document.getElementById("chatMessages");
    chatMessages.innerHTML = "";

    const messages = await apiGetMessages();

    messages.forEach(msg => {
        addMessageToUI(msg.text, msg.sender, msg.timestamp);
    });

    scrollToBottom();
}

async function sendMessage() {
    const input = document.getElementById("messageInput");
    const text = input.value.trim();
    if (!text) return;

    const message = await apiSendMessage(text);
    addMessageToUI(message.text, "sent", message.timestamp);

    input.value = "";
    scrollToBottom();
}

function addMessageToUI(text, sender, timestamp) {
    const chatMessages = document.getElementById("chatMessages");
    const div = document.createElement("div");

    div.className = "message " + (sender === "user" ? "sent" : "received");

    const time = new Date(timestamp);
    const timeStr = time.getHours() + ":" + String(time.getMinutes()).padStart(2, "0");

    div.innerHTML = `
        <div class="message-bubble">${text}</div>
        <div class="message-time">Сьогодні, ${timeStr}</div>
    `;

    chatMessages.appendChild(div);
}

function scrollToBottom() {
    const chatMessages = document.getElementById("chatMessages");
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
