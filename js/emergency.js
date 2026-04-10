/**
 * StadiumOS Antigravity — Emergency Response System
 * Real-time emergency alerts, dispatch, and incident tracking.
 */
class EmergencySystem {
  constructor(containerId, actionsId) {
    this.container = document.getElementById(containerId);
    this.actionsContainer = document.getElementById(actionsId);
    this.alerts = [];
    this.teams = [
      { id: 'alpha', name: 'Alpha', status: 'available', zone: 'Gate A' },
      { id: 'bravo', name: 'Bravo', status: 'available', zone: 'North Stand' },
      { id: 'charlie', name: 'Charlie', status: 'deployed', zone: 'Food Court S' },
      { id: 'delta', name: 'Delta', status: 'available', zone: 'East Stand' },
      { id: 'echo', name: 'Echo', status: 'standby', zone: 'Medical Bay' },
      { id: 'medic1', name: 'Medic-1', status: 'available', zone: 'Medical Bay' },
    ];

    this.initAlerts();
    this.render();
    this.renderActions();
    this.startSimulation();
  }

  initAlerts() {
    this.alerts = [
      {
        id: 1,
        type: 'warning',
        title: 'High Density: Food Court South',
        desc: 'Crowd density reached 85%. AI recommends opening overflow lanes.',
        time: '2 min ago',
        zone: 'food-s',
        status: 'active',
      },
      {
        id: 2,
        type: 'info',
        title: 'Gate D Queue Reducing',
        desc: 'Wait time dropped to 3 min. Normal flow restored.',
        time: '5 min ago',
        zone: 'gate-d',
        status: 'active',
      },
      {
        id: 3,
        type: 'critical',
        title: 'Medical Request: Section 12B',
        desc: 'Attendee reporting dizziness. Medic-1 dispatched.',
        time: '8 min ago',
        zone: 'north-stand',
        status: 'active',
      },
      {
        id: 4,
        type: 'resolved',
        title: 'Resolved: Gate A Bottleneck',
        desc: 'Crowd redirected via Gate B. Flow normalized.',
        time: '15 min ago',
        zone: 'gate-a',
        status: 'resolved',
      },
    ];
  }

  getAlertIcon(type) {
    switch (type) {
      case 'critical': return '🔴';
      case 'warning': return '🟡';
      case 'info': return '🔵';
      case 'resolved': return '✅';
      default: return '⚪';
    }
  }

  render() {
    if (!this.container) return;
    const html = this.alerts.map(a => `
      <div class="alert-item alert-item--${a.type}" data-alert-id="${a.id}">
        <div class="alert-item__icon">${this.getAlertIcon(a.type)}</div>
        <div class="alert-item__content">
          <div class="alert-item__title">${a.title}</div>
          <div class="alert-item__desc">${a.desc}</div>
          <div class="alert-item__time">${a.time}</div>
        </div>
      </div>
    `).join('');
    this.container.innerHTML = html;
  }

  renderActions() {
    if (!this.actionsContainer) return;
    this.actionsContainer.innerHTML = `
      <button class="emergency-btn emergency-btn--danger" onclick="window.emergencySystem.triggerLockdown()">
        🚨 Lockdown
      </button>
      <button class="emergency-btn" onclick="window.emergencySystem.dispatchTeam()">
        👥 Dispatch Team
      </button>
      <button class="emergency-btn" onclick="window.emergencySystem.clearAll()">
        ✅ Clear All
      </button>
      <button class="emergency-btn" onclick="window.emergencySystem.broadcastPA()">
        📢 PA Broadcast
      </button>
    `;
  }

  triggerLockdown() {
    this.addAlert({
      type: 'critical',
      title: '🚨 LOCKDOWN INITIATED',
      desc: 'All gates sealed. Security teams deployed to perimeter. Awaiting all-clear.',
      zone: 'all',
    });
    this.showNotification('Lockdown Protocol Activated', 'danger');
  }

  dispatchTeam() {
    const available = this.teams.find(t => t.status === 'available');
    if (available) {
      available.status = 'deployed';
      this.addAlert({
        type: 'info',
        title: `Team ${available.name} Dispatched`,
        desc: `Deployed to ${available.zone} for crowd management support.`,
        zone: available.zone,
      });
      this.showNotification(`Team ${available.name} dispatched`, 'primary');
    } else {
      this.showNotification('No teams available for dispatch', 'warning');
    }
  }

  clearAll() {
    this.alerts = this.alerts.map(a => ({...a, type: 'resolved', status: 'resolved'}));
    this.render();
    this.showNotification('All alerts cleared', 'success');
  }

  broadcastPA() {
    this.addAlert({
      type: 'info',
      title: 'PA Broadcast Sent',
      desc: 'Public announcement broadcast to all zones: "Please use Gate B for exit."',
      zone: 'all',
    });
    this.showNotification('PA Broadcast sent to all zones', 'cyan');
  }

  addAlert(data) {
    const alert = {
      id: Date.now(),
      ...data,
      time: 'Just now',
      status: 'active',
    };
    this.alerts.unshift(alert);
    if (this.alerts.length > 8) this.alerts.pop();
    this.render();
  }

  showNotification(msg, type = 'primary') {
    const notif = document.createElement('div');
    notif.style.cssText = `
      position: fixed; top: 80px; right: 24px; z-index: 1000;
      padding: 12px 20px; border-radius: 12px;
      background: rgba(15,15,28,0.95); backdrop-filter: blur(20px);
      border: 1px solid var(--accent-${type}, rgba(255,255,255,0.1));
      color: var(--text-primary); font-size: 13px; font-weight: 500;
      font-family: 'Inter', sans-serif;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
      animation: slideUp 0.4s cubic-bezier(0.16,1,0.3,1);
      max-width: 320px;
    `;
    notif.textContent = msg;
    document.body.appendChild(notif);
    setTimeout(() => {
      notif.style.opacity = '0';
      notif.style.transform = 'translateY(-10px)';
      notif.style.transition = 'all 0.3s ease';
      setTimeout(() => notif.remove(), 300);
    }, 3000);
  }

  startSimulation() {
    const scenarios = [
      { type: 'warning', title: 'Crowd Surge Detected: East Stand', desc: 'AI predicts 90% density in 5 minutes. Recommend pre-emptive routing.' },
      { type: 'info', title: 'Temperature Alert: Section 8', desc: 'Ambient temperature elevated. HVAC systems adjusting.' },
      { type: 'warning', title: 'Queue Overflow: Merchandise', desc: 'Queue extends beyond designated area. Staff rerouting.' },
      { type: 'info', title: 'Parking Lot 3 Full', desc: 'Overflow parking activated. Digital signage updated.' },
      { type: 'critical', title: 'Unauthorized Access: VIP Zone', desc: 'Security checkpoint flagged unregistered entry. Team investigating.' },
      { type: 'info', title: 'Halftime Rush Predicted', desc: 'AI forecasts 40% increase in concession demand in 3 minutes.' },
    ];

    setInterval(() => {
      if (Math.random() > 0.6) {
        const scenario = scenarios[Math.floor(Math.random() * scenarios.length)];
        this.addAlert({ ...scenario, zone: 'auto' });
      }
    }, 8000);
  }

  getActiveAlertCount() {
    return this.alerts.filter(a => a.status === 'active').length;
  }
}

window.EmergencySystem = EmergencySystem;
