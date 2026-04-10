/**
 * StadiumOS Antigravity — Crowd Heatmap Engine
 * Renders a real-time crowd density heatmap on Canvas.
 */
class CrowdHeatmap {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.zones = [];
    this.animId = null;
    this.time = 0;

    this.initZones();
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

  initZones() {
    // Stadium zones with relative positions
    const zoneData = [
      { id: 'gate-a',     name: 'Gate A (North)',      rx: 0.5,  ry: 0.05, rw: 0.2, rh: 0.06, base: 0.7 },
      { id: 'gate-b',     name: 'Gate B (East)',       rx: 0.95, ry: 0.5,  rw: 0.06, rh: 0.2, base: 0.5 },
      { id: 'gate-c',     name: 'Gate C (South)',      rx: 0.5,  ry: 0.95, rw: 0.2, rh: 0.06, base: 0.6 },
      { id: 'gate-d',     name: 'Gate D (West)',       rx: 0.05, ry: 0.5,  rw: 0.06, rh: 0.2, base: 0.4 },
      { id: 'north-stand', name: 'North Stand',         rx: 0.5,  ry: 0.18, rw: 0.6, rh: 0.1, base: 0.65 },
      { id: 'south-stand', name: 'South Stand',         rx: 0.5,  ry: 0.82, rw: 0.6, rh: 0.1, base: 0.55 },
      { id: 'east-stand',  name: 'East Stand',          rx: 0.85, ry: 0.5,  rw: 0.1, rh: 0.4, base: 0.5 },
      { id: 'west-stand',  name: 'West Stand',          rx: 0.15, ry: 0.5,  rw: 0.1, rh: 0.4, base: 0.45 },
      { id: 'food-n',      name: 'Food Court North',    rx: 0.3,  ry: 0.3,  rw: 0.08, rh: 0.06, base: 0.8 },
      { id: 'food-s',      name: 'Food Court South',    rx: 0.7,  ry: 0.7,  rw: 0.08, rh: 0.06, base: 0.75 },
      { id: 'vip-lounge',  name: 'VIP Lounge',          rx: 0.7,  ry: 0.3,  rw: 0.1, rh: 0.08, base: 0.3 },
      { id: 'merch',       name: 'Merchandise',         rx: 0.3,  ry: 0.7,  rw: 0.08, rh: 0.06, base: 0.6 },
      { id: 'field',       name: 'Playing Field',       rx: 0.5,  ry: 0.5,  rw: 0.35, rh: 0.25, base: 0.0 },
      { id: 'restroom-ne', name: 'Restroom NE',         rx: 0.75, ry: 0.2,  rw: 0.04, rh: 0.04, base: 0.5 },
      { id: 'restroom-sw', name: 'Restroom SW',         rx: 0.25, ry: 0.8,  rw: 0.04, rh: 0.04, base: 0.55 },
      { id: 'medical',     name: 'Medical Bay',         rx: 0.15, ry: 0.2,  rw: 0.05, rh: 0.05, base: 0.1 },
    ];

    this.zones = zoneData.map(z => ({
      ...z,
      density: z.base,
      targetDensity: z.base,
      phase: Math.random() * Math.PI * 2,
    }));
  }

  getDensityColor(density) {
    if (density < 0.3) return { r: 16, g: 185, b: 129, a: 0.5 };  // Green
    if (density < 0.5) return { r: 6, g: 182, b: 212, a: 0.55 };   // Cyan
    if (density < 0.7) return { r: 245, g: 158, b: 11, a: 0.6 };   // Amber
    if (density < 0.85) return { r: 239, g: 68, b: 68, a: 0.65 };  // Red
    return { r: 220, g: 38, b: 38, a: 0.75 };                      // Dark Red
  }

  drawStadiumOutline() {
    const cx = this.w / 2;
    const cy = this.h / 2;
    const rx = this.w * 0.45;
    const ry = this.h * 0.43;

    // Outer boundary
    this.ctx.beginPath();
    this.ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
    this.ctx.strokeStyle = 'rgba(255,255,255,0.08)';
    this.ctx.lineWidth = 2;
    this.ctx.stroke();

    // Inner ring
    this.ctx.beginPath();
    this.ctx.ellipse(cx, cy, rx * 0.65, ry * 0.65, 0, 0, Math.PI * 2);
    this.ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    this.ctx.lineWidth = 1;
    this.ctx.stroke();

    // Playing field (center rectangle)
    const fw = this.w * 0.3;
    const fh = this.h * 0.2;
    this.ctx.beginPath();
    this.ctx.roundRect(cx - fw/2, cy - fh/2, fw, fh, 6);
    this.ctx.strokeStyle = 'rgba(16, 185, 129, 0.15)';
    this.ctx.lineWidth = 1.5;
    this.ctx.stroke();

    // Center circle
    this.ctx.beginPath();
    this.ctx.arc(cx, cy, Math.min(fw, fh) * 0.25, 0, Math.PI * 2);
    this.ctx.strokeStyle = 'rgba(16, 185, 129, 0.1)';
    this.ctx.stroke();

    // Center line
    this.ctx.beginPath();
    this.ctx.moveTo(cx, cy - fh/2);
    this.ctx.lineTo(cx, cy + fh/2);
    this.ctx.strokeStyle = 'rgba(16, 185, 129, 0.1)';
    this.ctx.stroke();
  }

  drawZone(zone) {
    const x = zone.rx * this.w;
    const y = zone.ry * this.h;
    const w = zone.rw * this.w;
    const h = zone.rh * this.h;
    const color = this.getDensityColor(zone.density);

    // Zone fill with gradient
    const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, Math.max(w, h));
    gradient.addColorStop(0, `rgba(${color.r},${color.g},${color.b},${color.a})`);
    gradient.addColorStop(1, `rgba(${color.r},${color.g},${color.b},0)`);

    this.ctx.beginPath();
    this.ctx.ellipse(x, y, w, h, 0, 0, Math.PI * 2);
    this.ctx.fillStyle = gradient;
    this.ctx.fill();

    // Zone label
    if (zone.density > 0.05) {
      this.ctx.fillStyle = `rgba(255,255,255,${Math.min(zone.density + 0.3, 0.8)})`;
      this.ctx.font = `500 ${Math.max(9, this.w * 0.012)}px Inter, sans-serif`;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(zone.name, x, y - h * 0.3);

      // Density percentage
      this.ctx.font = `700 ${Math.max(10, this.w * 0.016)}px "JetBrains Mono", monospace`;
      this.ctx.fillText(`${Math.round(zone.density * 100)}%`, x, y + h * 0.15);
    }
  }

  updateDensities() {
    this.time += 0.016;
    for (const zone of this.zones) {
      // Simulate density fluctuations
      const wave = Math.sin(this.time * 0.5 + zone.phase) * 0.15;
      const noise = (Math.random() - 0.5) * 0.02;
      zone.targetDensity = Math.max(0, Math.min(1, zone.base + wave + noise));
      zone.density += (zone.targetDensity - zone.density) * 0.05;
    }
  }

  draw() {
    this.ctx.clearRect(0, 0, this.w, this.h);
    this.drawStadiumOutline();
    for (const zone of this.zones) {
      if (zone.id !== 'field') {
        this.drawZone(zone);
      }
    }
  }

  animate() {
    this.updateDensities();
    this.draw();
    this.animId = requestAnimationFrame(() => this.animate());
  }

  getZoneData() {
    return this.zones.map(z => ({
      id: z.id,
      name: z.name,
      density: Math.round(z.density * 100),
    }));
  }

  destroy() {
    if (this.animId) cancelAnimationFrame(this.animId);
  }
}

window.CrowdHeatmap = CrowdHeatmap;
