/**
 * StadiumOS Antigravity — Digital Twin Engine
 * Simplified 3D-like stadium visualization using 2D Canvas.
 */
class DigitalTwin {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.time = 0;
    this.viewMode = 'density'; // density, flow, security
    this.zoneData = {};
    this.hoveredZone = null;

    this.resize();
    this.animate();
    window.addEventListener('resize', () => this.resize());

    // Mouse interaction
    this.canvas.addEventListener('mousemove', (e) => this.handleMouse(e));
    this.canvas.addEventListener('mouseleave', () => { this.hoveredZone = null; });
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

  handleMouse(e) {
    const rect = this.canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    // Simple zone detection
    this.hoveredZone = null;
    const zones = this.getZonePositions();
    for (const z of zones) {
      if (mx > z.x - z.w/2 && mx < z.x + z.w/2 && my > z.y - z.h/2 && my < z.y + z.h/2) {
        this.hoveredZone = z;
        break;
      }
    }
  }

  setViewMode(mode) {
    this.viewMode = mode;
    // Update button states
    document.querySelectorAll('.twin-control-btn').forEach(btn => {
      btn.classList.toggle('twin-control-btn--active', btn.dataset.mode === mode);
    });
  }

  getZonePositions() {
    const cx = this.w / 2;
    const cy = this.h / 2;
    return [
      { id: 'north', name: 'North Stand', x: cx, y: cy - this.h*0.35, w: this.w*0.5, h: this.h*0.08, density: 0.72, people: 8400 },
      { id: 'south', name: 'South Stand', x: cx, y: cy + this.h*0.35, w: this.w*0.5, h: this.h*0.08, density: 0.55, people: 6200 },
      { id: 'east', name: 'East Stand', x: cx + this.w*0.35, y: cy, w: this.h*0.06, h: this.h*0.45, density: 0.50, people: 5800 },
      { id: 'west', name: 'West Stand', x: cx - this.w*0.35, y: cy, w: this.h*0.06, h: this.h*0.45, density: 0.45, people: 5200 },
      { id: 'ne-corner', name: 'NE Corner', x: cx + this.w*0.28, y: cy - this.h*0.28, w: this.w*0.08, h: this.h*0.08, density: 0.65, people: 1800 },
      { id: 'nw-corner', name: 'NW Corner', x: cx - this.w*0.28, y: cy - this.h*0.28, w: this.w*0.08, h: this.h*0.08, density: 0.58, people: 1600 },
      { id: 'se-corner', name: 'SE Corner', x: cx + this.w*0.28, y: cy + this.h*0.28, w: this.w*0.08, h: this.h*0.08, density: 0.42, people: 1200 },
      { id: 'sw-corner', name: 'SW Corner', x: cx - this.w*0.28, y: cy + this.h*0.28, w: this.w*0.08, h: this.h*0.08, density: 0.38, people: 1000 },
      { id: 'field', name: 'Playing Field', x: cx, y: cy, w: this.w*0.35, h: this.h*0.35, density: 0, people: 22 },
    ];
  }

  getDensityColor(d) {
    if (d < 0.01) return 'rgba(16,185,129,0.1)';
    if (d < 0.3) return 'rgba(16,185,129,0.4)';
    if (d < 0.5) return 'rgba(6,182,212,0.4)';
    if (d < 0.7) return 'rgba(245,158,11,0.4)';
    if (d < 0.85) return 'rgba(239,68,68,0.4)';
    return 'rgba(220,38,38,0.5)';
  }

  drawIsometric() {
    const ctx = this.ctx;
    this.time += 0.016;
    ctx.clearRect(0, 0, this.w, this.h);

    const cx = this.w / 2;
    const cy = this.h / 2;

    // Stadium outline (oval) with 3D depth
    const sx = this.w * 0.42;
    const sy = this.h * 0.42;

    // Shadow
    ctx.beginPath();
    ctx.ellipse(cx, cy + 8, sx + 5, sy + 5, 0, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(0,0,0,0.2)';
    ctx.fill();

    // Outer ring
    ctx.beginPath();
    ctx.ellipse(cx, cy, sx, sy, 0, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(99,102,241,0.15)';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.fillStyle = 'rgba(10,10,18,0.6)';
    ctx.fill();

    // Inner ring
    ctx.beginPath();
    ctx.ellipse(cx, cy, sx * 0.75, sy * 0.75, 0, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Draw zones
    const zones = this.getZonePositions();
    for (const z of zones) {
      const isHovered = this.hoveredZone && this.hoveredZone.id === z.id;

      // Animate density
      const pulse = Math.sin(this.time * 1.5) * 0.05;
      const d = Math.min(1, z.density + pulse);

      ctx.beginPath();
      ctx.roundRect(z.x - z.w/2, z.y - z.h/2, z.w, z.h, 4);
      ctx.fillStyle = this.getDensityColor(d);
      ctx.fill();

      if (isHovered) {
        ctx.strokeStyle = 'rgba(99,102,241,0.6)';
        ctx.lineWidth = 2;
        ctx.stroke();
      } else {
        ctx.strokeStyle = 'rgba(255,255,255,0.06)';
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }

      // Zone label
      if (z.w > 30 && z.h > 20) {
        ctx.fillStyle = 'rgba(255,255,255,0.6)';
        ctx.font = `500 ${Math.max(8, Math.min(11, z.w * 0.08))}px Inter, sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(z.name, z.x, z.y - 6);

        ctx.font = `700 ${Math.max(9, Math.min(13, z.w * 0.1))}px "JetBrains Mono", monospace`;
        ctx.fillStyle = this.getDensityColor(d).replace('0.4', '1').replace('0.1', '0.6');
        ctx.fillText(`${Math.round(d * 100)}%`, z.x, z.y + 8);
      }
    }

    // Floating people dots (flow visualization)
    if (this.viewMode === 'flow' || this.viewMode === 'density') {
      for (let i = 0; i < 30; i++) {
        const angle = (this.time * 0.3 + i * 0.21) % (Math.PI * 2);
        const r = sx * 0.5 + Math.sin(i * 1.7) * sx * 0.25;
        const x = cx + Math.cos(angle) * r;
        const y = cy + Math.sin(angle) * r * 0.85;
        
        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(99,102,241,${0.3 + Math.sin(this.time + i) * 0.2})`;
        ctx.fill();
      }
    }

    // Security overlay
    if (this.viewMode === 'security') {
      const secPoints = [
        { x: cx, y: cy - this.h*0.42, label: '📷' },
        { x: cx + this.w*0.38, y: cy, label: '📷' },
        { x: cx, y: cy + this.h*0.42, label: '📷' },
        { x: cx - this.w*0.38, y: cy, label: '📷' },
        { x: cx + this.w*0.28, y: cy - this.h*0.28, label: '👮' },
        { x: cx - this.w*0.28, y: cy + this.h*0.28, label: '👮' },
      ];
      for (const sp of secPoints) {
        // Scan radius
        const scanR = 30 + Math.sin(this.time * 2) * 5;
        ctx.beginPath();
        ctx.arc(sp.x, sp.y, scanR, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(6,182,212,0.2)';
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.fillStyle = 'rgba(6,182,212,0.05)';
        ctx.fill();

        ctx.font = '14px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(sp.label, sp.x, sp.y + 5);
      }
    }

    // Hover tooltip
    if (this.hoveredZone) {
      const z = this.hoveredZone;
      const tx = z.x + z.w/2 + 10;
      const ty = z.y - z.h/2;
      const tw = 140;
      const th = 56;

      ctx.fillStyle = 'rgba(10,10,20,0.9)';
      ctx.beginPath();
      ctx.roundRect(tx, ty, tw, th, 8);
      ctx.fill();
      ctx.strokeStyle = 'rgba(99,102,241,0.3)';
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.fillStyle = '#f0f0f5';
      ctx.font = '600 11px Inter, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(z.name, tx + 10, ty + 18);

      ctx.fillStyle = '#a0a0b8';
      ctx.font = '400 10px Inter, sans-serif';
      ctx.fillText(`Density: ${Math.round(z.density*100)}%`, tx + 10, ty + 33);
      ctx.fillText(`People: ${z.people.toLocaleString()}`, tx + 10, ty + 47);
    }
  }

  animate() {
    this.drawIsometric();
    requestAnimationFrame(() => this.animate());
  }
}

window.DigitalTwin = DigitalTwin;
