/**
 * StadiumOS Antigravity — AI Copilot
 * Natural language interface for querying stadium state.
 */
class AICopilot {
  constructor(messagesId, inputId, sendId) {
    this.messagesContainer = document.getElementById(messagesId);
    this.inputField = document.getElementById(inputId);
    this.sendBtn = document.getElementById(sendId);

    if (!this.messagesContainer || !this.inputField || !this.sendBtn) return;

    this.messages = [];
    this.context = {};

    this.initWelcome();
    this.bindEvents();
  }

  initWelcome() {
    this.addMessage('ai', `👋 Welcome to **StadiumOS Copilot**. I can help you with:

• Real-time crowd status & predictions
• Queue wait times & optimization
• Emergency dispatch & coordination
• Navigation & routing suggestions
• Analytics & trend insights

Try asking: *"What's the busiest zone right now?"*`);
  }

  bindEvents() {
    this.sendBtn.addEventListener('click', () => this.handleSend());
    this.inputField.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.handleSend();
    });
  }

  handleSend() {
    const text = this.inputField.value.trim();
    if (!text) return;
    this.addMessage('user', text);
    this.inputField.value = '';
    
    setTimeout(() => {
      const response = this.generateResponse(text);
      this.addMessage('ai', response);
    }, 600 + Math.random() * 800);
  }

  generateResponse(query) {
    const q = query.toLowerCase();

    // Crowd / Zone queries
    if (q.includes('busy') || q.includes('crowd') || q.includes('density') || q.includes('busiest')) {
      return `📊 **Current Crowd Analysis:**

• **Food Court South** — 85% density ⚠️ (highest)
• **North Stand** — 72% density
• **Gate A** — 68% density (entry surge)
• **East Stand** — 52% density ✅

🤖 **AI Recommendation:** Redirect incoming attendees to Gate D (40% density). Consider opening overflow food counters at Food Court North.`;
    }

    // Queue queries
    if (q.includes('queue') || q.includes('wait') || q.includes('line') || q.includes('food')) {
      return `⏱️ **Queue Status:**

| Location | Wait | People | Trend |
|----------|------|--------|-------|
| Food Court S | 18 min | 62/80 | ↑ Rising |
| Food Court N | 12 min | 45/80 | ↑ Rising |
| Merchandise | 8 min | 28/50 | ↓ Falling |
| Restroom NE | 4 min | 15/30 | → Stable |

🤖 **AI Suggestion:** Open 2 additional counters at Food Court South. Predicted wait reduction: **-7 minutes**.`;
    }

    // Emergency queries
    if (q.includes('emergency') || q.includes('incident') || q.includes('alert') || q.includes('security')) {
      return `🚨 **Active Incidents:** 3

1. 🟡 High density at Food Court South — monitoring
2. 🔴 Medical request Section 12B — Medic-1 deployed
3. 🔵 Gate D queue normalized — resolved

**Available Teams:** Alpha (Gate A), Bravo (North Stand), Delta (East Stand)

🤖 **Recommendation:** Pre-position Team Delta near Food Court South for potential crowd management.`;
    }

    // Navigation queries
    if (q.includes('navigate') || q.includes('route') || q.includes('direction') || q.includes('how to get')) {
      return `🗺️ **Smart Navigation Active:**

Current fastest routes:
• **To Food Court** → via Corridor B (2 min) ✅
• **To Exit** → Gate D recommended (3 min wait)
• **To Restroom** → NE restroom has shortest queue (4 min)

🤖 Avoiding: Gate A (congested), Corridor A (high density)

*Dynamic rerouting updates every 30 seconds.*`;
    }

    // Prediction queries
    if (q.includes('predict') || q.includes('forecast') || q.includes('expect') || q.includes('halftime')) {
      return `🔮 **AI Predictions (next 30 min):**

• Halftime rush expected in **12 minutes**
• Concession demand will increase **40%**
• Gate C will see exit surge (estimated 3,200 people)
• Restroom queues will peak at **8-10 min** wait

🤖 **Pre-emptive Actions Recommended:**
1. Open all food counters now
2. Deploy crowd management to Gate C
3. Activate overflow parking signage
4. Pre-stage cleaning crews at restrooms`;
    }

    // Stats / analytics
    if (q.includes('stats') || q.includes('analytics') || q.includes('numbers') || q.includes('report')) {
      return `📈 **Live Stadium Analytics:**

• **Total Attendance:** 47,832 / 52,000 (92%)
• **Avg Wait Time:** 9.2 minutes
• **Satisfaction Score:** 87/100
• **Incidents Today:** 7 (5 resolved)
• **AI Interventions:** 23 automated actions
• **Time Saved (est.):** 4,200 person-hours

*Performance is 12% above last match day.*`;
    }

    // Default intelligent response
    const defaults = [
      `🤖 Great question! Based on current stadium data, I can see all systems are operating normally. Current attendance is at 92% capacity with 3 active monitoring alerts. Would you like me to drill down into any specific area?`,
      `📊 I'm monitoring 16 zones, 6 queue points, and 12 IoT sensors in real-time. Everything looks stable. What specific insight can I help you with? Try asking about crowds, queues, or predictions.`,
      `🏟️ StadiumOS is tracking **47,832 attendees** across all zones. The AI has made **23 automated interventions** today to optimize flow. Ask me about any specific zone or system for details!`,
    ];
    return defaults[Math.floor(Math.random() * defaults.length)];
  }

  addMessage(role, text) {
    const msg = { role, text, time: new Date() };
    this.messages.push(msg);
    this.renderMessage(msg);
    this.scrollToBottom();
  }

  renderMessage(msg) {
    const div = document.createElement('div');
    div.className = `copilot-msg copilot-msg--${msg.role}`;
    
    const avatar = msg.role === 'ai' ? '🤖' : '👤';
    
    // Simple markdown-like formatting
    let html = msg.text
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>')
      .replace(/• /g, '&bull; ');

    div.innerHTML = `
      <div class="copilot-msg__avatar">${avatar}</div>
      <div class="copilot-msg__bubble">${html}</div>
    `;
    this.messagesContainer.appendChild(div);
  }

  scrollToBottom() {
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }
}

window.AICopilot = AICopilot;
