/**
 * StadiumOS Antigravity — Particle Engine
 * Creates an ambient, zero-gravity floating particle background.
 */
class AntigravityParticles {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.particles = [];
    this.connections = [];
    this.mouse = { x: null, y: null, radius: 150 };
    this.animId = null;
    this.dpr = window.devicePixelRatio || 1;

    this.resize();
    this.init();
    this.animate();

    window.addEventListener('resize', () => this.resize());
    window.addEventListener('mousemove', (e) => {
      this.mouse.x = e.clientX * this.dpr;
      this.mouse.y = e.clientY * this.dpr;
    });
    window.addEventListener('mouseout', () => {
      this.mouse.x = null;
      this.mouse.y = null;
    });
  }

  resize() {
    this.width = window.innerWidth * this.dpr;
    this.height = window.innerHeight * this.dpr;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
    this.canvas.style.width = window.innerWidth + 'px';
    this.canvas.style.height = window.innerHeight + 'px';
  }

  init() {
    const count = Math.min(Math.floor((this.width * this.height) / 25000), 80);
    this.particles = [];
    for (let i = 0; i < count; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 2 + 0.5,
        opacity: Math.random() * 0.4 + 0.1,
        hue: Math.random() > 0.7 ? 250 : (Math.random() > 0.5 ? 200 : 280),
        pulseSpeed: Math.random() * 0.02 + 0.005,
        pulsePhase: Math.random() * Math.PI * 2,
      });
    }
  }

  drawParticle(p, time) {
    const pulse = Math.sin(time * p.pulseSpeed + p.pulsePhase) * 0.3 + 0.7;
    const size = p.size * pulse;
    const opacity = p.opacity * pulse;

    this.ctx.beginPath();
    this.ctx.arc(p.x, p.y, size * this.dpr, 0, Math.PI * 2);
    this.ctx.fillStyle = `hsla(${p.hue}, 70%, 70%, ${opacity})`;
    this.ctx.fill();

    // Glow
    if (p.size > 1.2) {
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, size * 3 * this.dpr, 0, Math.PI * 2);
      this.ctx.fillStyle = `hsla(${p.hue}, 70%, 70%, ${opacity * 0.1})`;
      this.ctx.fill();
    }
  }

  drawConnections() {
    const maxDist = 120 * this.dpr;
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const dx = this.particles[i].x - this.particles[j].x;
        const dy = this.particles[i].y - this.particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < maxDist) {
          const opacity = (1 - dist / maxDist) * 0.08;
          this.ctx.beginPath();
          this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
          this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
          this.ctx.strokeStyle = `rgba(99, 102, 241, ${opacity})`;
          this.ctx.lineWidth = 0.5 * this.dpr;
          this.ctx.stroke();
        }
      }
    }
  }

  update() {
    for (const p of this.particles) {
      // Antigravity drift
      p.x += p.vx;
      p.y += p.vy;

      // Mouse repulsion (antigravity effect)
      if (this.mouse.x !== null) {
        const dx = p.x - this.mouse.x;
        const dy = p.y - this.mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const mouseRadius = this.mouse.radius * this.dpr;
        if (dist < mouseRadius) {
          const force = (mouseRadius - dist) / mouseRadius * 0.03;
          p.vx += (dx / dist) * force;
          p.vy += (dy / dist) * force;
        }
      }

      // Damping
      p.vx *= 0.999;
      p.vy *= 0.999;

      // Wrap edges
      if (p.x < 0) p.x = this.width;
      if (p.x > this.width) p.x = 0;
      if (p.y < 0) p.y = this.height;
      if (p.y > this.height) p.y = 0;
    }
  }

  animate() {
    const time = performance.now();
    this.ctx.clearRect(0, 0, this.width, this.height);
    this.update();
    this.drawConnections();
    for (const p of this.particles) {
      this.drawParticle(p, time);
    }
    this.animId = requestAnimationFrame(() => this.animate());
  }

  destroy() {
    if (this.animId) cancelAnimationFrame(this.animId);
  }
}

// Initialize
window.antigravityParticles = new AntigravityParticles('particle-canvas');
