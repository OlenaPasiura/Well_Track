// ===================================
// Nutrition API (MOCK)
// ===================================

async function apiGetNutritionData() {
    return getData(STORAGE_KEYS.NUTRITION_DATA, []);
}

async function apiSaveNutritionData(data) {
    saveData(STORAGE_KEYS.NUTRITION_DATA, data);
}
