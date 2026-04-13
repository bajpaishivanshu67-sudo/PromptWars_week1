/**
 * StadiumOS Antigravity — Main Application Controller
 * Initializes all modules and manages application state.
 */
class StadiumOS {
  constructor() {
    this.modules = {};
    this.currentView = 'dashboard';
    this.init();
  }

  init() {
    // Wait for DOM
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.bootstrap());
    } else {
      this.bootstrap();
    }
  }

  bootstrap() {
    console.log('%c🏟️ StadiumOS Antigravity v1.0', 'color: #6366f1; font-size: 16px; font-weight: bold;');
    console.log('%cAI-Powered Stadium Experience Platform', 'color: #8b5cf6; font-size: 12px;');

    // Initialize modules
    this.modules.heatmap = new CrowdHeatmap('heatmap-canvas');
    this.modules.queues = new QueueManager('queue-list');
    this.modules.emergency = new EmergencySystem('emergency-alerts', 'emergency-actions');
    window.emergencySystem = this.modules.emergency;
    this.modules.analytics = new AnalyticsEngine();
    this.modules.copilot = new AICopilot('copilot-messages', 'copilot-input', 'copilot-send');
    this.modules.twin = new DigitalTwin('twin-canvas');
    this.modules.navigation = new NavigationEngine('nav-canvas');

    // Setup sidebar navigation
    this.setupNavigation();

    // Start clock
    this.startClock();

    // Start KPI updates
    this.startKPIUpdates();

    // Bind twin view controls
    this.bindTwinControls();

    // Bind navigation route selector
    this.bindNavRoutes();
  }

  setupNavigation() {
    document.querySelectorAll('.sidebar__item[data-view]').forEach(item => {
      item.addEventListener('click', () => {
        const view = item.dataset.view;
        this.switchView(view);
      });
    });
  }

  switchView(view) {
    // Update sidebar
    document.querySelectorAll('.sidebar__item[data-view]').forEach(item => {
      item.classList.toggle('sidebar__item--active', item.dataset.view === view);
    });

    // Toggle pages
    document.querySelectorAll('.page-view').forEach(panel => {
      panel.classList.toggle('page-view--active', panel.dataset.page === view);
    });

    this.currentView = view;

    // Re-render canvases on view switch
    setTimeout(() => {
      if (this.modules.heatmap) this.modules.heatmap.resize();
      if (this.modules.twin) this.modules.twin.resize();
      if (this.modules.navigation) this.modules.navigation.resize();
    }, 100);
  }

  startClock() {
    const clockEl = document.getElementById('topbar-clock');
    if (!clockEl) return;
    
    const update = () => {
      const now = new Date();
      const h = now.getHours().toString().padStart(2, '0');
      const m = now.getMinutes().toString().padStart(2, '0');
      const s = now.getSeconds().toString().padStart(2, '0');
      clockEl.textContent = `${h}:${m}:${s}`;
    };
    update();
    setInterval(update, 1000);
  }

  startKPIUpdates() {
    const kpis = {
      'kpi-attendance': { base: 47832, min: 46000, max: 52000, step: 50 },
      'kpi-avg-wait': { base: 9.2, min: 5, max: 18, step: 0.3, decimal: 1 },
      'kpi-incidents': { base: 3, min: 0, max: 12, step: 1 },
      'kpi-satisfaction': { base: 87, min: 70, max: 99, step: 1 },
    };

    setInterval(() => {
      for (const [id, cfg] of Object.entries(kpis)) {
        const el = document.getElementById(id);
        if (!el) continue;
        const delta = (Math.random() - 0.45) * cfg.step * 2;
        cfg.base = Math.max(cfg.min, Math.min(cfg.max, cfg.base + delta));
        const value = cfg.decimal ? cfg.base.toFixed(cfg.decimal) : Math.round(cfg.base);
        el.textContent = typeof value === 'string' ? value : value.toLocaleString();
      }
    }, 3000);
  }

  bindTwinControls() {
    document.querySelectorAll('.twin-control-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const mode = btn.dataset.mode;
        if (this.modules.twin) {
          this.modules.twin.setViewMode(mode);
        }
      });
    });
  }

  bindNavRoutes() {
    document.querySelectorAll('.nav-route-btn').forEach((btn, i) => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.nav-route-btn').forEach(b => b.classList.remove('twin-control-btn--active'));
        btn.classList.add('twin-control-btn--active');
        if (this.modules.navigation) {
          this.modules.navigation.setRoute(i);
        }
      });
    });
  }
}

// Launch
window.stadiumOS = new StadiumOS();
