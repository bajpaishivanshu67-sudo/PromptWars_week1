/**
 * StadiumOS Antigravity — Queue Management Module
 * Smart queue management with AI-predicted wait times.
 */
class QueueManager {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;
    this.queues = this.generateQueues();
    this.render();
    this.startUpdates();
  }

  generateQueues() {
    return [
      {
        id: 'food-n',
        name: 'Food Court North',
        icon: '🍔',
        type: 'food',
        people: 45,
        maxCapacity: 80,
        avgWaitMin: 12,
        trend: 'rising',
        counters: { open: 6, total: 8 },
        color: '#f59e0b',
      },
      {
        id: 'food-s',
        name: 'Food Court South',
        icon: '🍕',
        type: 'food',
        people: 62,
        maxCapacity: 80,
        avgWaitMin: 18,
        trend: 'rising',
        counters: { open: 5, total: 8 },
        color: '#ef4444',
      },
      {
        id: 'merch-main',
        name: 'Merchandise Store',
        icon: '🏪',
        type: 'retail',
        people: 28,
        maxCapacity: 50,
        avgWaitMin: 8,
        trend: 'falling',
        counters: { open: 3, total: 4 },
        color: '#6366f1',
      },
      {
        id: 'restroom-ne',
        name: 'Restroom NE',
        icon: '🚻',
        type: 'facility',
        people: 15,
        maxCapacity: 30,
        avgWaitMin: 4,
        trend: 'stable',
        counters: { open: 10, total: 12 },
        color: '#06b6d4',
      },
      {
        id: 'restroom-sw',
        name: 'Restroom SW',
        icon: '🚻',
        type: 'facility',
        people: 22,
        maxCapacity: 30,
        avgWaitMin: 7,
        trend: 'rising',
        counters: { open: 8, total: 12 },
        color: '#f59e0b',
      },
      {
        id: 'gate-entry',
        name: 'VIP Entry',
        icon: '🎫',
        type: 'entry',
        people: 8,
        maxCapacity: 40,
        avgWaitMin: 2,
        trend: 'falling',
        counters: { open: 4, total: 4 },
        color: '#10b981',
      },
    ];
  }

  getStatusColor(ratio) {
    if (ratio < 0.4) return 'var(--accent-success)';
    if (ratio < 0.65) return 'var(--accent-cyan)';
    if (ratio < 0.8) return 'var(--accent-warning)';
    return 'var(--accent-danger)';
  }

  getTrendIcon(trend) {
    switch (trend) {
      case 'rising': return '↑';
      case 'falling': return '↓';
      default: return '→';
    }
  }

  getTrendClass(trend) {
    switch (trend) {
      case 'rising': return 'stat-card__trend--down';
      case 'falling': return 'stat-card__trend--up';
      default: return 'stat-card__trend--neutral';
    }
  }

  render() {
    if (!this.container) return;
    const html = this.queues.map(q => {
      const ratio = q.people / q.maxCapacity;
      const statusColor = this.getStatusColor(ratio);
      const fillPercent = Math.round(ratio * 100);
      return `
        <div class="queue-item" data-queue="${q.id}">
          <div class="queue-item__icon" style="background:rgba(${this.hexToRgb(q.color)},0.12);color:${q.color};">
            ${q.icon}
          </div>
          <div class="queue-item__info">
            <div class="queue-item__name">${q.name}</div>
            <div class="queue-item__detail">
              ${q.people}/${q.maxCapacity} people · ${q.counters.open}/${q.counters.total} counters
            </div>
            <div class="queue-item__bar">
              <div class="queue-item__fill" style="width:${fillPercent}%;background:${statusColor};"></div>
            </div>
          </div>
          <div class="queue-item__wait">
            <div class="queue-item__time" style="color:${statusColor}">${q.avgWaitMin}m</div>
            <div class="queue-item__status ${this.getTrendClass(q.trend)}">
              ${this.getTrendIcon(q.trend)} ${q.trend}
            </div>
          </div>
        </div>
      `;
    }).join('');
    this.container.innerHTML = html;
  }

  hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? `${parseInt(result[1],16)},${parseInt(result[2],16)},${parseInt(result[3],16)}` : '255,255,255';
  }

  simulateUpdate() {
    for (const q of this.queues) {
      const delta = Math.floor(Math.random() * 7) - 3;
      q.people = Math.max(2, Math.min(q.maxCapacity, q.people + delta));
      
      const ratio = q.people / q.maxCapacity;
      q.avgWaitMin = Math.max(1, Math.round(ratio * 25 + Math.random() * 3));
      
      if (delta > 1) q.trend = 'rising';
      else if (delta < -1) q.trend = 'falling';
      else q.trend = 'stable';

      // AI: Suggest opening more counters
      if (ratio > 0.75 && q.counters.open < q.counters.total) {
        q.counters.open = Math.min(q.counters.total, q.counters.open + 1);
      }

      q.color = this.getStatusColor(ratio).replace('var(--accent-', '').replace(')', '');
      if (ratio < 0.4) q.color = '#10b981';
      else if (ratio < 0.65) q.color = '#06b6d4';
      else if (ratio < 0.8) q.color = '#f59e0b';
      else q.color = '#ef4444';
    }
    this.render();
  }

  startUpdates() {
    setInterval(() => this.simulateUpdate(), 3000);
  }

  getQueueData() {
    return this.queues.map(q => ({
      id: q.id,
      name: q.name,
      people: q.people,
      wait: q.avgWaitMin,
      capacity: Math.round((q.people / q.maxCapacity) * 100),
    }));
  }
}

window.QueueManager = QueueManager;
