// ===================================
// Sleep API (MOCK)
// ===================================

async function apiGetSleepData() {
    return getData(STORAGE_KEYS.SLEEP_DATA, []);
}

async function apiSaveSleepData(data) {
    saveData(STORAGE_KEYS.SLEEP_DATA, data);
}
