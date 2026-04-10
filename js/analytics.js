/**
 * StadiumOS Antigravity — Analytics Engine
 * Predictive analytics with live charts rendered on Canvas.
 */
class AnalyticsEngine {
  constructor() {
    this.charts = {};
    this.data = this.generateHistorical();
    this.initCharts();
    this.startUpdates();
  }

  generateHistorical() {
    const hours = [];
    for (let h = 0; h < 24; h++) {
      const base = h < 10 ? 10 + h * 5 :
                   h < 14 ? 60 + Math.sin(h) * 15 :
                   h < 18 ? 80 + Math.sin(h * 0.5) * 10 :
                   h < 21 ? 70 - (h - 18) * 10 :
                   20 - (h - 21) * 5;
      hours.push({
        hour: h,
        attendance: Math.max(0, Math.round(base * 500 + Math.random() * 2000)),
        queueAvg: Math.max(1, Math.round(base * 0.2 + Math.random() * 5)),
        incidents: Math.floor(Math.random() * (base > 50 ? 4 : 2)),
        satisfaction: Math.max(60, Math.min(99, Math.round(100 - base * 0.3 + Math.random() * 10))),
      });
    }
    return hours;
  }

  initCharts() {
    this.initChart('chart-attendance', 'Attendance Flow', '#6366f1', d => d.attendance, 50000);
    this.initChart('chart-queues', 'Avg Queue Wait (min)', '#f59e0b', d => d.queueAvg, 30);
    this.initSparklines();
  }

  initChart(canvasId, label, color, getter, maxVal) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    this.charts[canvasId] = { canvas, ctx, label, color, getter, maxVal };
    this.drawChart(canvasId);
  }

  drawChart(chartId) {
    const chart = this.charts[chartId];
    if (!chart) return;
    
    const { canvas, ctx, color, getter, maxVal } = chart;
    const rect = canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    const w = rect.width;
    const h = rect.height;

    ctx.clearRect(0, 0, w, h);

    // Grid lines
    for (let i = 0; i < 5; i++) {
      const y = (h / 5) * i + 20;
      ctx.beginPath();
      ctx.moveTo(40, y);
      ctx.lineTo(w - 10, y);
      ctx.strokeStyle = 'rgba(255,255,255,0.04)';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Y-axis labels
      ctx.fillStyle = 'rgba(255,255,255,0.25)';
      ctx.font = '10px "JetBrains Mono", monospace';
      ctx.textAlign = 'right';
      const val = Math.round(maxVal - (maxVal / 5) * i);
      ctx.fillText(val.toLocaleString(), 35, y + 4);
    }

    // X-axis labels
    const dataPoints = this.data;
    const step = (w - 50) / (dataPoints.length - 1);
    for (let i = 0; i < dataPoints.length; i += 3) {
      const x = 40 + i * step;
      ctx.fillStyle = 'rgba(255,255,255,0.25)';
      ctx.font = '10px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`${dataPoints[i].hour}:00`, x, h - 5);
    }

    // Area fill
    ctx.beginPath();
    ctx.moveTo(40, h - 25);
    for (let i = 0; i < dataPoints.length; i++) {
      const x = 40 + i * step;
      const val = getter(dataPoints[i]);
      const y = 20 + (1 - val / maxVal) * (h - 50);
      if (i === 0) ctx.lineTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.lineTo(40 + (dataPoints.length - 1) * step, h - 25);
    ctx.closePath();
    
    const gradient = ctx.createLinearGradient(0, 0, 0, h);
    gradient.addColorStop(0, color + '30');
    gradient.addColorStop(1, color + '00');
    ctx.fillStyle = gradient;
    ctx.fill();

    // Line
    ctx.beginPath();
    for (let i = 0; i < dataPoints.length; i++) {
      const x = 40 + i * step;
      const val = getter(dataPoints[i]);
      const y = 20 + (1 - val / maxVal) * (h - 50);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    ctx.stroke();

    // Current point (last data point)
    const lastIdx = dataPoints.length - 1;
    const lastX = 40 + lastIdx * step;
    const lastVal = getter(dataPoints[lastIdx]);
    const lastY = 20 + (1 - lastVal / maxVal) * (h - 50);

    ctx.beginPath();
    ctx.arc(lastX, lastY, 4, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.beginPath();
    ctx.arc(lastX, lastY, 8, 0, Math.PI * 2);
    ctx.fillStyle = color + '30';
    ctx.fill();
  }

  initSparklines() {
    document.querySelectorAll('.sparkline').forEach(el => {
      const type = el.dataset.type;
      const bars = 12;
      let html = '';
      for (let i = 0; i < bars; i++) {
        let height;
        if (type === 'attendance') height = 30 + Math.random() * 70;
        else if (type === 'queue') height = 20 + Math.sin(i * 0.8) * 30 + Math.random() * 20;
        else if (type === 'incidents') height = 10 + Math.random() * 40;
        else height = 50 + Math.random() * 50;

        const color = type === 'attendance' ? 'var(--accent-primary)' :
                      type === 'queue' ? 'var(--accent-warning)' :
                      type === 'incidents' ? 'var(--accent-danger)' : 'var(--accent-cyan)';
        
        html += `<div class="sparkline__bar" style="height:${height}%;background:${color};opacity:${0.4 + (i/bars)*0.6}"></div>`;
      }
      el.innerHTML = html;
    });
  }

  startUpdates() {
    setInterval(() => {
      // Shift data to simulate real-time
      const now = new Date();
      const currentHour = now.getHours();
      const lastEntry = this.data[this.data.length - 1];
      
      lastEntry.attendance += Math.floor(Math.random() * 500 - 200);
      lastEntry.queueAvg = Math.max(1, lastEntry.queueAvg + Math.floor(Math.random() * 3 - 1));
      lastEntry.satisfaction = Math.max(60, Math.min(99, lastEntry.satisfaction + Math.floor(Math.random() * 3 - 1)));

      Object.keys(this.charts).forEach(id => this.drawChart(id));
    }, 5000);
  }
}

window.AnalyticsEngine = AnalyticsEngine;
