// ===================================
// WEll-track Dashboard
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    // Protect page
    //protectPage();

    const user = getCurrentUser();

    // Update user name
    const userNameEl = document.getElementById('userName');
    if (userNameEl && user) {
        userNameEl.textContent = user.name;
    }

    // Load and display stats
    loadDashboardStats();

    // Create charts
    createStressChart();
    createSleepChart();
});

function loadDashboardStats() {
    const today = getTodayString();

    // Load stress data
    const stressData = getData(STORAGE_KEYS.STRESS_DATA, []);
    const todayStress = stressData.find(function(item) { return item.date === today; });
    const stressLevelEl = document.getElementById('stressLevel');
    if (stressLevelEl) {
        stressLevelEl.textContent = todayStress ? getStressLabel(todayStress.level) : 'Не вказано';
    }

    // Load sleep data
    const sleepData = getData(STORAGE_KEYS.SLEEP_DATA, []);
    const todaySleep = sleepData.find(function(item) { return item.date === today; });
    const sleepHoursEl = document.getElementById('sleepHours');
    if (sleepHoursEl) {
        sleepHoursEl.textContent = todaySleep ? todaySleep.hours + ' год' : 'Не вказано';
    }

    // Load nutrition data
    const nutritionData = getData(STORAGE_KEYS.NUTRITION_DATA, []);
    const todayNutrition = nutritionData.find(function(item) { return item.date === today; });
    const caloriesEl = document.getElementById('calories');
    if (caloriesEl) {
        if (todayNutrition && todayNutrition.meals) {
            const totalCalories = todayNutrition.meals.reduce(function(sum, meal) {
                return sum + (meal.calories || 0);
            }, 0);
            caloriesEl.textContent = totalCalories + ' ккал';
        } else {
            caloriesEl.textContent = 'Не вказано';
        }
    }
}

function getStressLabel(level) {
    const labels = {
        1: 'Дуже низький',
        2: 'Низький',
        3: 'Середній',
        4: 'Високий',
        5: 'Дуже високий'
    };
    return labels[level] || 'Не вказано';
}

function createStressChart() {
    const ctx = document.getElementById('stressChart');
    if (!ctx) return;

    const stressData = getData(STORAGE_KEYS.STRESS_DATA, []);

    // Get last 7 days
    const labels = [];
    const data = [];
    const today = new Date();

    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const dateStr = date.toISOString().split('T')[0];

        labels.push(formatDate(dateStr));

        const dayData = stressData.find(function(item) { return item.date === dateStr; });
        data.push(dayData ? dayData.level : 0);
    }

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Рівень стресу',
                data: data,
                borderColor: 'rgb(239, 68, 68)',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function createSleepChart() {
    const ctx = document.getElementById('sleepChart');
    if (!ctx) return;

    const sleepData = getData(STORAGE_KEYS.SLEEP_DATA, []);

    // Get last 7 days
    const labels = [];
    const data = [];
    const today = new Date();

    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const dateStr = date.toISOString().split('T')[0];

        labels.push(formatDate(dateStr));

        const dayData = sleepData.find(function(item) { return item.date === dateStr; });
        data.push(dayData ? dayData.hours : 0);
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Години сну',
                data: data,
                backgroundColor: 'rgba(139, 92, 246, 0.8)',
                borderColor: 'rgb(139, 92, 246)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 12,
                    ticks: {
                        stepSize: 2
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}
