// ===================================
// WEll-track Sleep page logic (frontend only)
// Depends on: main.js (protectPage, STORAGE_KEYS, getData, saveData, formatDate, getTodayString)
// ===================================

document.addEventListener("DOMContentLoaded", function () {
  protectPage();

  let selectedQuality = null;
  let sleepChart = null;
  let currentPeriod = "week";

  const sleepSlider = document.getElementById("sleepSlider");
  const sleepValue = document.getElementById("sleepValue");
  const qualityButtons = document.querySelectorAll(".quality-btn");
  const saveBtn = document.getElementById("saveBtn");

  // slider value
  if (sleepSlider && sleepValue) {
    sleepSlider.addEventListener("input", function () {
      sleepValue.textContent = this.value;
    });
  }

  // quality selection
  qualityButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      qualityButtons.forEach(function (b) {
        b.classList.remove("selected");
      });
      this.classList.add("selected");
      selectedQuality = this.getAttribute("data-quality");
    });
  });

  // save
  if (saveBtn) {
    saveBtn.addEventListener("click", function () {
      const hours = sleepSlider ? parseFloat(sleepSlider.value) : 0;
      const noteEl = document.getElementById("note");
      const note = noteEl ? noteEl.value : "";
      const today = getTodayString();

      const sleepData = getData(STORAGE_KEYS.SLEEP_DATA, []);
      const existingIndex = sleepData.findIndex(function (item) {
        return item.date === today;
      });

      const entry = {
        date: today,
        hours: hours,
        quality: selectedQuality || "average",
        note: note,
        timestamp: new Date().toISOString(),
      };

      if (existingIndex >= 0) sleepData[existingIndex] = entry;
      else sleepData.push(entry);

      saveData(STORAGE_KEYS.SLEEP_DATA, sleepData);

      alert("Збережено!");
      updateChart();
      updateStats();
    });
  }

  // expose for onclick in HTML
  window.switchPeriod = function (period) {
    currentPeriod = period;

    const weekBtn = document.getElementById("weekBtn");
    const monthBtn = document.getElementById("monthBtn");
    if (weekBtn) weekBtn.classList.toggle("active", period === "week");
    if (monthBtn) monthBtn.classList.toggle("active", period === "month");

    updateChart();
    updateStats();
  };

  function updateChart() {
    const canvas = document.getElementById("sleepChart");
    if (!canvas || typeof Chart === "undefined") return;

    const sleepData = getData(STORAGE_KEYS.SLEEP_DATA, []);
    const days = currentPeriod === "week" ? 7 : 30;

    const labels = [];
    const data = [];
    const today = new Date();

    for (let i = days - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split("T")[0];

      labels.push(currentPeriod === "week" ? formatDate(dateStr) : `${d.getDate()}.${d.getMonth() + 1}`);

      const dayData = sleepData.find(function (item) {
        return item.date === dateStr;
      });
      data.push(dayData ? dayData.hours : null);
    }

    if (sleepChart) sleepChart.destroy();

    sleepChart = new Chart(canvas, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Години сну",
            data,
            // без кастомних кольорів — залишимо дефолт, щоб “не ламати стиль” (або стилізуєш потім)
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 12,
            ticks: { stepSize: 2 },
          },
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function (ctx) {
                return ctx.parsed.y != null ? `${ctx.parsed.y} год` : "Немає даних";
              },
            },
          },
        },
      },
    });
  }

  function updateStats() {
    const sleepData = getData(STORAGE_KEYS.SLEEP_DATA, []);
    const days = currentPeriod === "week" ? 7 : 30;

    const today = new Date();
    const periodData = [];

    for (let i = days - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split("T")[0];

      const dayData = sleepData.find(function (item) {
        return item.date === dateStr;
      });
      if (dayData) periodData.push(dayData);
    }

    const avgHoursEl = document.getElementById("avgHours");
    const avgQualityEl = document.getElementById("avgQuality");
    const totalRecordsEl = document.getElementById("totalRecords");

    if (!avgHoursEl || !avgQualityEl || !totalRecordsEl) return;

    if (periodData.length === 0) {
      avgHoursEl.textContent = "Немає даних";
      avgQualityEl.textContent = "-";
      totalRecordsEl.textContent = "0";
      return;
    }

    const avgHours =
      periodData.reduce(function (sum, item) {
        return sum + (item.hours || 0);
      }, 0) / periodData.length;

    avgHoursEl.textContent = `${avgHours.toFixed(1)} год`;

    const qualityMap = { poor: 1, average: 2, good: 3 };
    const avgQualityNum =
      periodData.reduce(function (sum, item) {
        return sum + (qualityMap[item.quality] || 2);
      }, 0) / periodData.length;

    let qualityText = "Нормально";
    if (avgQualityNum >= 2.5) qualityText = "Відмінно";
    else if (avgQualityNum < 1.5) qualityText = "Погано";

    avgQualityEl.textContent = qualityText;
    totalRecordsEl.textContent = String(periodData.length);
  }

  // initial draw
  updateChart();
  updateStats();
});
