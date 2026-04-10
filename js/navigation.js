/**
 * StadiumOS Antigravity — Indoor Navigation Module
 * Dynamic rerouting navigation system with pathfinding.
 */
class NavigationEngine {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.time = 0;
    this.selectedRoute = 0;

    this.waypoints = [
      { id: 'gate-a', name: 'Gate A', x: 0.5, y: 0.05, type: 'gate' },
      { id: 'gate-b', name: 'Gate B', x: 0.95, y: 0.5, type: 'gate' },
      { id: 'gate-c', name: 'Gate C', x: 0.5, y: 0.95, type: 'gate' },
      { id: 'gate-d', name: 'Gate D', x: 0.05, y: 0.5, type: 'gate' },
      { id: 'food-n', name: 'Food North', x: 0.35, y: 0.25, type: 'food' },
      { id: 'food-s', name: 'Food South', x: 0.65, y: 0.75, type: 'food' },
      { id: 'restroom-ne', name: 'Restroom NE', x: 0.75, y: 0.2, type: 'facility' },
      { id: 'restroom-sw', name: 'Restroom SW', x: 0.25, y: 0.8, type: 'facility' },
      { id: 'vip', name: 'VIP Lounge', x: 0.78, y: 0.35, type: 'vip' },
      { id: 'merch', name: 'Merchandise', x: 0.22, y: 0.65, type: 'shop' },
      { id: 'medical', name: 'Medical Bay', x: 0.12, y: 0.18, type: 'medical' },
      { id: 'seat-1', name: 'Section A1', x: 0.4, y: 0.4, type: 'seat' },
      { id: 'seat-2', name: 'Section B3', x: 0.6, y: 0.6, type: 'seat' },
    ];

    this.routes = [
      { from: 'gate-a', to: 'food-n', path: ['gate-a', 'food-n'], time: 2, distance: 120, status: 'clear', color: '#10b981' },
      { from: 'gate-a', to: 'seat-1', path: ['gate-a', 'food-n', 'seat-1'], time: 4, distance: 250, status: 'moderate', color: '#f59e0b' },
      { from: 'seat-2', to: 'gate-c', path: ['seat-2', 'food-s', 'gate-c'], time: 3, distance: 180, status: 'clear', color: '#10b981' },
    ];

    this.resize();
    this.animate();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    this.ctx.scale(dpr, dpr);
    this.w = rect.width;
    this.h = rect.height;
  }

  getWaypointIcon(type) {
    switch (type) {
      case 'gate': return '🚪';
      case 'food': return '🍔';
      case 'facility': return '🚻';
      case 'vip': return '⭐';
      case 'shop': return '🏪';
      case 'medical': return '🏥';
      case 'seat': return '💺';
      default: return '📍';
    }
  }

  draw() {
    const ctx = this.ctx;
    this.time += 0.016;
    ctx.clearRect(0, 0, this.w, this.h);

    // Background grid
    ctx.strokeStyle = 'rgba(255,255,255,0.03)';
    ctx.lineWidth = 0.5;
    const gridSize = 30;
    for (let x = 0; x < this.w; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, this.h);
      ctx.stroke();
    }
    for (let y = 0; y < this.h; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(this.w, y);
      ctx.stroke();
    }

    // Connections between adjacent waypoints (background paths)
    const connections = [
      ['gate-a', 'food-n'], ['gate-a', 'restroom-ne'],
      ['food-n', 'seat-1'], ['food-n', 'vip'],
      ['gate-b', 'vip'], ['gate-b', 'restroom-ne'],
      ['seat-1', 'seat-2'], ['seat-1', 'merch'],
      ['seat-2', 'food-s'], ['food-s', 'gate-c'],
      ['gate-d', 'merch'], ['gate-d', 'restroom-sw'],
      ['restroom-sw', 'food-s'], ['merch', 'medical'],
      ['medical', 'gate-d'],
    ];

    for (const [from, to] of connections) {
      const a = this.waypoints.find(w => w.id === from);
      const b = this.waypoints.find(w => w.id === to);
      if (!a || !b) continue;

      ctx.beginPath();
      ctx.moveTo(a.x * this.w, a.y * this.h);
      ctx.lineTo(b.x * this.w, b.y * this.h);
      ctx.strokeStyle = 'rgba(255,255,255,0.06)';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 4]);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // Active route
    const route = this.routes[this.selectedRoute];
    if (route) {
      const pathPoints = route.path.map(id => this.waypoints.find(w => w.id === id));
      if (pathPoints.every(p => p)) {
        // Draw route path
        ctx.beginPath();
        for (let i = 0; i < pathPoints.length; i++) {
          const p = pathPoints[i];
          if (i === 0) ctx.moveTo(p.x * this.w, p.y * this.h);
          else ctx.lineTo(p.x * this.w, p.y * this.h);
        }
        ctx.strokeStyle = route.color;
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.stroke();

        // Animated dot along path
        const totalSegments = pathPoints.length - 1;
        const progress = (this.time * 0.3) % 1;
        const segIdx = Math.floor(progress * totalSegments);
        const segProgress = (progress * totalSegments) % 1;
        
        if (segIdx < totalSegments) {
          const a = pathPoints[segIdx];
          const b = pathPoints[segIdx + 1];
          const dx = b.x * this.w - a.x * this.w;
          const dy = b.y * this.h - a.y * this.h;
          const dotX = a.x * this.w + dx * segProgress;
          const dotY = a.y * this.h + dy * segProgress;

          // Glow
          ctx.beginPath();
          ctx.arc(dotX, dotY, 10, 0, Math.PI * 2);
          ctx.fillStyle = route.color + '40';
          ctx.fill();

          ctx.beginPath();
          ctx.arc(dotX, dotY, 5, 0, Math.PI * 2);
          ctx.fillStyle = route.color;
          ctx.fill();
        }
      }
    }

    // Draw waypoints
    for (const wp of this.waypoints) {
      const x = wp.x * this.w;
      const y = wp.y * this.h;

      // Background circle
      ctx.beginPath();
      ctx.arc(x, y, 14, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(15,15,28,0.9)';
      ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,0.1)';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Icon
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(this.getWaypointIcon(wp.type), x, y);

      // Label
      ctx.fillStyle = 'rgba(255,255,255,0.5)';
      ctx.font = '500 9px Inter, sans-serif';
      ctx.fillText(wp.name, x, y + 22);
    }

    // Route info overlay
    if (route) {
      const infoX = 10;
      const infoY = this.h - 50;
      ctx.fillStyle = 'rgba(10,10,20,0.85)';
      ctx.beginPath();
      ctx.roundRect(infoX, infoY, 200, 40, 8);
      ctx.fill();
      ctx.strokeStyle = route.color + '40';
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.fillStyle = '#f0f0f5';
      ctx.font = '600 11px Inter, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(`${route.from.replace('-',' ')} → ${route.to.replace('-',' ')}`, infoX + 10, infoY + 16);
      ctx.fillStyle = '#a0a0b8';
      ctx.font = '400 10px "JetBrains Mono", monospace';
      ctx.fillText(`${route.time} min · ${route.distance}m · ${route.status}`, infoX + 10, infoY + 32);
    }
  }

  setRoute(index) {
    this.selectedRoute = index;
  }

  animate() {
    this.draw();
    requestAnimationFrame(() => this.animate());
  }
}

window.NavigationEngine = NavigationEngine;
