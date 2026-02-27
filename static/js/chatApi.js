// ===================================
// Chat API (mock backend)
// Later will be replaced by Django API
// ===================================

async function apiGetMessages() {
    // 🟡 MOCK VERSION (теперішня)
    return getData(STORAGE_KEYS.CHAT_DATA, []);
}

async function apiSendMessage(text) {
    const messages = getData(STORAGE_KEYS.CHAT_DATA, []);

    const message = {
        id: Date.now(),
        text: text,
        sender: "user",
        timestamp: new Date().toISOString()
    };

    messages.push(message);
    saveData(STORAGE_KEYS.CHAT_DATA, messages);

    return message;
}
