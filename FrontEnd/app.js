// App State Management
class EnergyApp {
  constructor() {
    this.state = {
      currentSection: "dashboard",
      theme: "light",
      data: null,
      charts: {},
      updateInterval: null,
    };
    this.init();
  }

  async init() {
    // Load initial data
    await this.loadData();

    // Setup event listeners
    this.setupEventListeners();

    // Initialize components
    this.initializeCharts();
    this.renderDashboard();
    this.renderAppliances();
    this.renderAnalytics();
    this.renderGamification();

    // Start real-time updates
    this.startRealTimeUpdates();

    // Hide loading screen
    this.hideLoadingScreen();

    // Show initial alert
    setTimeout(() => this.showAlert(), 2000);
  }

  async loadData() {
    try {
      // Simulate API call with provided data
      this.state.data = {
        appliances: [
          {
            id: 1,
            name: "Smart AC",
            type: "HVAC",
            power_rating: 3500,
            status: "on",
          },
          {
            id: 2,
            name: "LED Lights Living Room",
            type: "Lighting",
            power_rating: 150,
            status: "on",
          },
          {
            id: 3,
            name: "Refrigerator",
            type: "Kitchen",
            power_rating: 400,
            status: "on",
          },
          {
            id: 4,
            name: "Smart TV",
            type: "Entertainment",
            power_rating: 250,
            status: "off",
          },
          {
            id: 5,
            name: "Washing Machine",
            type: "Appliance",
            power_rating: 2000,
            status: "off",
          },
          {
            id: 6,
            name: "Water Heater",
            type: "Utility",
            power_rating: 4500,
            status: "on",
          },
          {
            id: 7,
            name: "Dishwasher",
            type: "Kitchen",
            power_rating: 1800,
            status: "off",
          },
          {
            id: 8,
            name: "Smart Thermostat",
            type: "HVAC",
            power_rating: 50,
            status: "on",
          },
          {
            id: 9,
            name: "LED Lights Bedroom",
            type: "Lighting",
            power_rating: 100,
            status: "on",
          },
          {
            id: 10,
            name: "Desktop Computer",
            type: "Electronics",
            power_rating: 500,
            status: "on",
          },
        ],
        historical_data: [
          {
            date: "2025-08-29",
            consumption: 42.3,
            cost: 5.08,
            carbon_footprint: 16.92,
            peak_hours_usage: 12.69,
            efficiency_score: 78,
          },
          {
            date: "2025-08-30",
            consumption: 38.7,
            cost: 4.64,
            carbon_footprint: 15.48,
            peak_hours_usage: 11.61,
            efficiency_score: 82,
          },
          {
            date: "2025-08-31",
            consumption: 45.9,
            cost: 5.51,
            carbon_footprint: 18.36,
            peak_hours_usage: 13.77,
            efficiency_score: 74,
          },
        ],
        real_time: {
          timestamp: "2025-09-28T01:44:00",
          total_power: 8950,
          active_appliances: 6,
          estimated_daily_cost: 6.24,
          current_efficiency: 78,
          weather: {
            temperature: 24,
            humidity: 65,
            condition: "partly_cloudy",
          },
        },
        predictions: {
          next_day_consumption: 48.5,
          next_week_average: 46.2,
          monthly_projection: 1420,
          cost_savings_potential: 15.8,
          efficiency_improvements: [
            {
              appliance: "Smart AC",
              current_efficiency: 72,
              recommended_action: "Adjust temperature to 25°C during 2-6 PM",
              potential_savings: 8.5,
            },
            {
              appliance: "Water Heater",
              current_efficiency: 65,
              recommended_action: "Schedule heating during off-peak hours",
              potential_savings: 12.3,
            },
          ],
        },
        gamification: {
          user_level: 7,
          points_earned: 2450,
          badges: [
            {
              name: "Energy Saver",
              description: "Reduced consumption by 10% this month",
            },
            {
              name: "Peak Hour Avoider",
              description: "Shifted 70% of usage to off-peak hours",
            },
          ],
          challenges: [
            {
              name: "Weekend Energy Challenge",
              description: "Keep weekend consumption below weekday average",
              progress: 75,
              reward: 150,
            },
            {
              name: "Off-Peak Champion",
              description: "Use 80% of daily energy during off-peak hours",
              progress: 45,
              reward: 200,
            },
          ],
          leaderboard_position: 12,
          total_users: 150,
        },
      };
    } catch (error) {
      console.error("Failed to load data:", error);
      this.showToast("Error", "Failed to load energy data", "error");
    }
  }

  setupEventListeners() {
    // Navigation
    document.querySelectorAll(".nav-item").forEach((item) => {
      item.addEventListener("click", (e) => {
        e.preventDefault();
        const section = e.currentTarget.getAttribute("data-section");
        this.navigateToSection(section);
      });
    });

    // Analytics tabs
    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const tab = e.target.getAttribute("data-tab");
        this.switchAnalyticsTab(tab);
      });
    });

    // Theme toggle
    const themeToggle = document.querySelector(".theme-toggle");
    if (themeToggle) {
      themeToggle.addEventListener("click", () => this.toggleTheme());
    }

    // Appliance filter
    const applianceFilter = document.getElementById("applianceFilter");
    if (applianceFilter) {
      applianceFilter.addEventListener("change", (e) => {
        this.filterAppliances(e.target.value);
      });
    }
  }

  navigateToSection(section) {
    // Update active nav item
    document.querySelectorAll(".nav-item").forEach((item) => {
      item.classList.remove("active");
    });
    document
      .querySelector(`[data-section="${section}"]`)
      .classList.add("active");

    // Update active section
    document.querySelectorAll(".content-section").forEach((section) => {
      section.classList.remove("active");
    });
    document.getElementById(section).classList.add("active");

    // Update page title
    const titles = {
      dashboard: "Dashboard",
      appliances: "Appliances",
      analytics: "Analytics",
      gamification: "Gamification",
      settings: "Settings",
    };
    document.getElementById("pageTitle").textContent = titles[section];

    this.state.currentSection = section;
  }

  switchAnalyticsTab(tab) {
    // Update active tab button
    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.classList.remove("active");
    });
    document.querySelector(`[data-tab="${tab}"]`).classList.add("active");

    // Update active tab content
    document.querySelectorAll(".tab-content").forEach((content) => {
      content.classList.remove("active");
    });
    document.getElementById(`${tab}-tab`).classList.add("active");
  }

  initializeCharts() {
    // Consumption trend chart
    const consumptionCtx = document.getElementById("consumptionChart");
    if (consumptionCtx) {
      this.state.charts.consumption = new Chart(consumptionCtx, {
        type: "line",
        data: {
          labels: this.state.data.historical_data.map((d) =>
            new Date(d.date).toLocaleDateString()
          ),
          datasets: [
            {
              label: "Consumption (kWh)",
              data: this.state.data.historical_data.map((d) => d.consumption),
              borderColor: "#1FB8CD",
              backgroundColor: "rgba(31, 184, 205, 0.1)",
              fill: true,
              tension: 0.4,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: "rgba(0,0,0,0.1)",
              },
            },
            x: {
              grid: {
                display: false,
              },
            },
          },
        },
      });
    }

    // Appliance usage chart
    const applianceCtx = document.getElementById("applianceChart");
    if (applianceCtx) {
      const applianceTypes = {};
      this.state.data.appliances.forEach((appliance) => {
        if (appliance.status === "on") {
          applianceTypes[appliance.type] =
            (applianceTypes[appliance.type] || 0) + appliance.power_rating;
        }
      });

      this.state.charts.appliance = new Chart(applianceCtx, {
        type: "doughnut",
        data: {
          labels: Object.keys(applianceTypes),
          datasets: [
            {
              data: Object.values(applianceTypes),
              backgroundColor: [
                "#1FB8CD",
                "#FFC185",
                "#B4413C",
                "#ECEBD5",
                "#5D878F",
                "#DB4545",
              ],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "bottom",
            },
          },
        },
      });
    }

    // Historical chart in analytics
    const historicalCtx = document.getElementById("historicalChart");
    if (historicalCtx) {
      this.state.charts.historical = new Chart(historicalCtx, {
        type: "bar",
        data: {
          labels: this.state.data.historical_data.map((d) =>
            new Date(d.date).toLocaleDateString()
          ),
          datasets: [
            {
              label: "Consumption (kWh)",
              data: this.state.data.historical_data.map((d) => d.consumption),
              backgroundColor: "#1FB8CD",
            },
            {
              label: "Efficiency Score",
              data: this.state.data.historical_data.map(
                (d) => d.efficiency_score
              ),
              backgroundColor: "#FFC185",
              yAxisID: "y1",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              type: "linear",
              display: true,
              position: "left",
            },
            y1: {
              type: "linear",
              display: true,
              position: "right",
              max: 100,
              grid: {
                drawOnChartArea: false,
              },
            },
          },
        },
      });
    }
  }

  renderDashboard() {
    // Update real-time metrics
    const currentUsage = (this.state.data.real_time.total_power / 1000).toFixed(
      2
    );
    document.getElementById("currentUsage").textContent = currentUsage;
    document.getElementById("activeAppliances").textContent =
      this.state.data.real_time.active_appliances;
    document.getElementById("efficiencyScore").textContent =
      this.state.data.real_time.current_efficiency;
    document.getElementById("dailyCost").textContent =
      this.state.data.real_time.estimated_daily_cost;

    // Update progress bar
    const progressFill = document.querySelector(
      ".efficiency-progress .progress-fill"
    );
    if (progressFill) {
      progressFill.style.width = `${this.state.data.real_time.current_efficiency}%`;
    }
  }

  renderAppliances() {
    const appliancesGrid = document.getElementById("appliancesGrid");
    if (!appliancesGrid) return;

    appliancesGrid.innerHTML = "";

    this.state.data.appliances.forEach((appliance) => {
      const applianceCard = document.createElement("div");
      applianceCard.className = `appliance-card ${
        appliance.status === "on" ? "active" : ""
      }`;

      applianceCard.innerHTML = `
                <div class="appliance-header">
                    <div class="appliance-info">
                        <h4>${appliance.name}</h4>
                        <div class="appliance-type">${appliance.type}</div>
                    </div>
                    <button class="appliance-toggle ${
                      appliance.status === "on" ? "active" : ""
                    }" 
                            onclick="energyApp.toggleAppliance(${
                              appliance.id
                            })">
                    </button>
                </div>
                <div class="appliance-stats">
                    <div class="appliance-stat">
                        <div class="appliance-stat-label">Power Rating</div>
                        <div class="appliance-stat-value">${
                          appliance.power_rating
                        }W</div>
                    </div>
                    <div class="appliance-stat">
                        <div class="appliance-stat-label">Status</div>
                        <div class="appliance-stat-value">${
                          appliance.status === "on" ? "ON" : "OFF"
                        }</div>
                    </div>
                </div>
            `;

      appliancesGrid.appendChild(applianceCard);
    });

    this.updateApplianceStats();
  }

  toggleAppliance(id) {
    const appliance = this.state.data.appliances.find((a) => a.id === id);
    if (!appliance) return;

    // Toggle status
    appliance.status = appliance.status === "on" ? "off" : "on";

    // Update UI
    this.renderAppliances();
    this.renderDashboard();

    // Update charts
    this.updateCharts();

    // Show feedback
    const action = appliance.status === "on" ? "turned on" : "turned off";
    this.showToast(
      "Appliance Updated",
      `${appliance.name} has been ${action}`,
      "success"
    );

    // Simulate real-time update
    this.updateRealTimeData();
  }

  filterAppliances(type) {
    const cards = document.querySelectorAll(".appliance-card");
    cards.forEach((card) => {
      const applianceType = card.querySelector(".appliance-type").textContent;
      if (type === "all" || applianceType === type) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  }

  updateApplianceStats() {
    const totalAppliances = this.state.data.appliances.length;
    const activeAppliances = this.state.data.appliances.filter(
      (a) => a.status === "on"
    ).length;
    const totalPower = this.state.data.appliances
      .filter((a) => a.status === "on")
      .reduce((sum, a) => sum + a.power_rating, 0);

    document.getElementById("totalAppliances").textContent = totalAppliances;
    document.getElementById("activeAppliancesCount").textContent =
      activeAppliances;
    document.getElementById("totalPower").textContent = `${(
      totalPower / 1000
    ).toFixed(2)} kW`;
  }

  renderAnalytics() {
    // Analytics content is mostly static charts, already initialized
  }

  renderGamification() {
    // Update user level progress
    const xpProgress = document.querySelector(".xp-progress");
    if (xpProgress) {
      const progress = (this.state.data.gamification.points_earned % 1000) / 10;
      xpProgress.style.width = `${progress}%`;
    }

    // Update challenge progress bars
    document
      .querySelectorAll(".challenge-progress .progress-fill")
      .forEach((bar, index) => {
        if (this.state.data.gamification.challenges[index]) {
          bar.style.width = `${this.state.data.gamification.challenges[index].progress}%`;
        }
      });
  }

  updateCharts() {
    // Update appliance chart
    if (this.state.charts.appliance) {
      const applianceTypes = {};
      this.state.data.appliances.forEach((appliance) => {
        if (appliance.status === "on") {
          applianceTypes[appliance.type] =
            (applianceTypes[appliance.type] || 0) + appliance.power_rating;
        }
      });

      this.state.charts.appliance.data.labels = Object.keys(applianceTypes);
      this.state.charts.appliance.data.datasets[0].data =
        Object.values(applianceTypes);
      this.state.charts.appliance.update();
    }
  }

  updateRealTimeData() {
    // Simulate real-time data updates
    const activeAppliances = this.state.data.appliances.filter(
      (a) => a.status === "on"
    );
    const totalPower = activeAppliances.reduce(
      (sum, a) => sum + a.power_rating,
      0
    );

    this.state.data.real_time.total_power = totalPower;
    this.state.data.real_time.active_appliances = activeAppliances.length;
    this.state.data.real_time.estimated_daily_cost = (
      (totalPower * 24 * 0.12) /
      1000
    ).toFixed(2);

    // Update dashboard
    this.renderDashboard();
  }

  startRealTimeUpdates() {
    this.state.updateInterval = setInterval(() => {
      this.updateLastUpdateTime();
      // Simulate minor data fluctuations
      this.simulateDataFluctuations();
    }, 30000); // Update every 30 seconds
  }

  updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById(
      "lastUpdate"
    ).textContent = `Last updated: ${timeString}`;
  }

  simulateDataFluctuations() {
    // Add small random variations to simulate real-time changes
    const variation = (Math.random() - 0.5) * 0.1;
    const currentPower = this.state.data.real_time.total_power;
    this.state.data.real_time.total_power = Math.max(
      0,
      currentPower + currentPower * variation
    );

    // Update efficiency score slightly
    const efficiencyVariation = Math.floor((Math.random() - 0.5) * 2);
    this.state.data.real_time.current_efficiency = Math.max(
      50,
      Math.min(
        100,
        this.state.data.real_time.current_efficiency + efficiencyVariation
      )
    );

    if (this.state.currentSection === "dashboard") {
      this.renderDashboard();
    }
  }

  toggleTheme() {
    const newTheme = this.state.theme === "light" ? "dark" : "light";
    this.state.theme = newTheme;

    document.documentElement.setAttribute("data-color-scheme", newTheme);

    const themeIcon = document.querySelector(".theme-icon");
    if (themeIcon) {
      themeIcon.textContent = newTheme === "light" ? "🌙" : "☀️";
    }

    this.showToast("Theme Changed", `Switched to ${newTheme} mode`, "success");
  }

  showAlert() {
    const alertBanner = document.getElementById("alertBanner");
    if (alertBanner) {
      alertBanner.classList.remove("hidden");
    }
  }

  hideLoadingScreen() {
    const loadingScreen = document.getElementById("loadingScreen");
    if (loadingScreen) {
      setTimeout(() => {
        loadingScreen.style.opacity = "0";
        setTimeout(() => {
          loadingScreen.style.display = "none";
        }, 300);
      }, 1000);
    }
  }

  showToast(title, message, type = "info") {
    const container = document.getElementById("toastContainer");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;

    toast.innerHTML = `
            <div class="toast-content">
                <div class="toast-message">
                    <div class="toast-title">${title}</div>
                    <div class="toast-description">${message}</div>
                </div>
                <button class="toast-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
            </div>
        `;

    container.appendChild(toast);

    // Show toast
    setTimeout(() => toast.classList.add("show"), 100);

    // Auto-hide after 5 seconds
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }, 5000);
  }
}

// Global functions for HTML event handlers
function closeAlert() {
  const alertBanner = document.getElementById("alertBanner");
  if (alertBanner) {
    alertBanner.classList.add("hidden");
  }
}

function toggleTheme() {
  if (window.energyApp) {
    window.energyApp.toggleTheme();
  }
}

function exportData(format) {
  if (!window.energyApp || !window.energyApp.state.data) return;

  const data = window.energyApp.state.data;
  let content, filename, mimeType;

  if (format === "csv") {
    // Convert historical data to CSV
    const headers = [
      "Date",
      "Consumption (kWh)",
      "Cost ($)",
      "Carbon Footprint (kg)",
      "Efficiency Score (%)",
    ];
    const rows = data.historical_data.map((row) => [
      row.date,
      row.consumption,
      row.cost,
      row.carbon_footprint,
      row.efficiency_score,
    ]);

    content = [headers, ...rows].map((row) => row.join(",")).join("\n");
    filename = "energy_data.csv";
    mimeType = "text/csv";
  } else if (format === "json") {
    content = JSON.stringify(data, null, 2);
    filename = "energy_data.json";
    mimeType = "application/json";
  }

  // Create and trigger download
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  window.energyApp.showToast(
    "Export Complete",
    `Data exported as ${format.toUpperCase()}`,
    "success"
  );
}

// Environment and export handling
if (typeof window !== "undefined") {
  // Browser environment code
  document.addEventListener("DOMContentLoaded", () => {
    window.energyApp = new EnergyApp();
  });

  // Handle page visibility changes
  document.addEventListener("visibilitychange", () => {
    if (window.energyApp) {
      if (document.hidden) {
        if (window.energyApp.state.updateInterval) {
          clearInterval(window.energyApp.state.updateInterval);
        }
      } else {
        window.energyApp.startRealTimeUpdates();
      }
    }
  });

  // Event listeners
  window.addEventListener("online", () => {
    if (window.energyApp) {
      window.energyApp.showToast(
        "Connection Restored",
        "You are back online",
        "success"
      );
    }
  });

  window.addEventListener("offline", () => {
    if (window.energyApp) {
      window.energyApp.showToast(
        "Connection Lost",
        "You are now offline",
        "warning"
      );
    }
  });

  document.addEventListener("keydown", (e) => {
    if (!window.energyApp) return;

    // Navigation shortcuts
    if (e.altKey) {
      switch (e.key) {
        case "1":
          e.preventDefault();
          window.energyApp.navigateToSection("dashboard");
          break;
        case "2":
          e.preventDefault();
          window.energyApp.navigateToSection("appliances");
          break;
        case "3":
          e.preventDefault();
          window.energyApp.navigateToSection("analytics");
          break;
        case "4":
          e.preventDefault();
          window.energyApp.navigateToSection("gamification");
          break;
        case "5":
          e.preventDefault();
          window.energyApp.navigateToSection("settings");
          break;
      }
    }

    // Theme toggle with Ctrl+Shift+T
    if (e.ctrlKey && e.shiftKey && e.key === "T") {
      e.preventDefault();
      window.energyApp.toggleTheme();
    }
  });

  // Performance monitoring
  if ("performance" in window) {
    window.addEventListener("load", () => {
      setTimeout(() => {
        const perfData = performance.getEntriesByType("navigation")[0];
        console.log(
          `App loaded in ${Math.round(
            perfData.loadEventEnd - perfData.fetchStart
          )}ms`
        );
      }, 0);
    });
  }

  // Error handling
  window.addEventListener("error", (e) => {
    console.error("Application error:", e.error);
    if (window.energyApp) {
      window.energyApp.showToast(
        "Application Error",
        "An unexpected error occurred",
        "error"
      );
    }
  });

  window.addEventListener("unhandledrejection", (e) => {
    console.error("Unhandled promise rejection:", e.reason);
    if (window.energyApp) {
      window.energyApp.showToast(
        "System Error",
        "A system error occurred",
        "error"
      );
    }
  });

  // Service Worker check
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      console.log("Service Worker support detected");
    });
  }
}

// Export for Node.js environment
if (typeof module !== "undefined" && module.exports) {
  module.exports = { EnergyApp };
}
