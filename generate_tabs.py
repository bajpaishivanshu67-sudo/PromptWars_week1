with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_html = """
      <!-- ===== Dashboard Tab (Default) ===== -->
      <div class="page-view page-view--active" data-page="dashboard" id="dashboard-grid">
        <div class="stats-row" style="margin-bottom: 24px;">
          <div class="stat-card">
            <div class="stat-card__icon stat-card__icon--primary">👥</div>
            <div class="stat-card__label">Total Attendance</div>
            <div class="stat-card__value" id="kpi-attendance">47,832</div>
            <div class="stat-card__trend stat-card__trend--up">
              ↑ 12% vs last match
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-card__icon stat-card__icon--success">⏱️</div>
            <div class="stat-card__label">Avg Wait Time</div>
            <div class="stat-card__value" id="kpi-avg-wait">9.2</div>
            <div class="stat-card__trend stat-card__trend--up">
              ↓ 18% improved
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-card__icon stat-card__icon--warning">🚨</div>
            <div class="stat-card__label">Active Incidents</div>
            <div class="stat-card__value" id="kpi-incidents">3</div>
            <div class="stat-card__trend stat-card__trend--neutral">
              → 5 resolved today
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-card__icon stat-card__icon--cyan">😊</div>
            <div class="stat-card__label">Satisfaction Score</div>
            <div class="stat-card__value" id="kpi-satisfaction">87</div>
            <div class="stat-card__trend stat-card__trend--up">
              ↑ 5pts above target
            </div>
          </div>
        </div>

        <div class="card col-12">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">⚡</span> Dashboard Briefing</div>
          </div>
          <div class="card__body" style="display:flex; gap: 20px;">
            <div style="flex: 2;">
              <h3 style="margin-bottom:10px; color:var(--accent-primary)">All systems nominal.</h3>
              <p style="color:var(--text-muted); font-size:14px;">The current match proceeds without major interruption. Weather is clear, temp 72°F. Wait times are well within normal bounds. There are 3 active low-level security incidents currently being addressed by Team Alpha and Charlie.</p>
            </div>
            <div style="flex: 1; display:flex; flex-direction:column; gap:10px;">
              <button class="twin-control-btn twin-control-btn--active" style="width:100%; text-align:center;">Generate Daily Report</button>
              <button class="twin-control-btn" style="width:100%; text-align:center;">Send Broadcast to Staff</button>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== Heatmap Tab ===== -->
      <div class="page-view" data-page="heatmap">
        <div class="card col-8">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">🔥</span> Crowd Density Heatmap</div>
            <span class="card__badge card__badge--live">● Live</span>
          </div>
          <div class="card__body">
            <div class="heatmap-container">
              <canvas id="heatmap-canvas"></canvas>
            </div>
            <div class="heatmap-legend">
              <div class="heatmap-legend__item"><div class="heatmap-legend__color" style="background:#10b981"></div> Low (&lt;30%)</div>
              <div class="heatmap-legend__item"><div class="heatmap-legend__color" style="background:#06b6d4"></div> Moderate (30-50%)</div>
              <div class="heatmap-legend__item"><div class="heatmap-legend__color" style="background:#f59e0b"></div> High (50-70%)</div>
              <div class="heatmap-legend__item"><div class="heatmap-legend__color" style="background:#ef4444"></div> Critical (&gt;70%)</div>
            </div>
          </div>
        </div>
        <div class="card col-4">
          <div class="card__header">
            <div class="card__title">Heatmap Controls & Actions</div>
          </div>
          <div class="card__body" style="display:flex; flex-direction:column; gap:15px;">
            <div>
              <p style="font-size:12px; color:var(--text-muted); margin-bottom:5px;">Time Prediction</p>
              <input type="range" min="0" max="60" value="0" style="width:100%;">
              <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-muted);">
                <span>Now</span><span>+60 Mins</span>
              </div>
            </div>
            <hr style="border:none; border-top:1px solid var(--border-subtle);">
            <div>
              <h4 style="margin-bottom:5px; font-size:13px;">Hotspot Alerts</h4>
              <p style="font-size:12px; color:var(--text-muted); margin-bottom:10px;">Gate C shows rapid gathering. Deploy line management?</p>
              <button class="twin-control-btn twin-control-btn--active" style="width:100%; border-color:var(--accent-warning); color:var(--accent-warning);">Deploy Delta Team to Gate C</button>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== Queues Tab ===== -->
      <div class="page-view" data-page="queues">
        <div class="card col-6">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">⏱️</span> Smart Queues List</div>
            <span class="card__badge card__badge--ai">AI</span>
          </div>
          <div class="card__body">
            <div class="queue-list" id="queue-list"></div>
          </div>
        </div>
        <div class="card col-6">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">📊</span> Wait Time Trends & Routing</div>
          </div>
          <div class="card__body">
            <div class="chart-container" style="height:200px;">
              <canvas id="chart-queues"></canvas>
            </div>
            <hr style="border:none; border-top:1px solid var(--border-subtle); margin:15px 0;">
            <p style="font-size:13px; margin-bottom:10px;">Queue Routing Suggestions:</p>
            <button class="twin-control-btn twin-control-btn--active" style="display:block; width:100%; margin-bottom:8px;">Open Backup Gate A2</button>
            <button class="twin-control-btn" style="display:block; width:100%;">Redirect 20% traffic to Concourse B</button>
          </div>
        </div>
      </div>

      <!-- ===== Emergency Tab ===== -->
      <div class="page-view" data-page="emergency">
        <div class="card col-6">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">🚨</span> Emergency Console</div>
            <span class="card__badge card__badge--live">● Active</span>
          </div>
          <div class="card__body">
            <div class="emergency-console">
              <div class="emergency-alerts" id="emergency-alerts"></div>
            </div>
          </div>
        </div>
        <div class="card col-6">
           <div class="card__header">
             <div class="card__title">Response Actions</div>
           </div>
           <div class="card__body">
             <div class="emergency-actions" id="emergency-actions">
               <!-- Will be populated by JS, or we can add static fallbacks -->
             </div>
             <hr style="border:none; border-top:1px solid var(--border-subtle); margin:15px 0;">
             <h4 style="margin-bottom:10px; font-size:13px; color:var(--accent-danger)">Critical Authority Actions</h4>
             <button class="twin-control-btn" style="border-color:var(--accent-danger); color:var(--accent-danger); width:100%; margin-bottom:8px;">Trigger Section Evacuation</button>
             <button class="twin-control-btn" style="border-color:var(--accent-danger); color:var(--accent-danger); width:100%;">Initiate Stadium Lockdown</button>
           </div>
        </div>
      </div>

      <!-- ===== Analytics Tab ===== -->
      <div class="page-view" data-page="analytics">
        <div class="card col-8">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">📊</span> Attendance Flow Analysis</div>
            <span class="card__badge card__badge--ai">Predictive</span>
          </div>
          <div class="card__body">
            <div class="chart-container" style="height:350px;">
              <canvas id="chart-attendance"></canvas>
            </div>
          </div>
        </div>
        <div class="card col-4">
          <div class="card__header">
            <div class="card__title">Demographics & Details</div>
          </div>
          <div class="card__body" style="display:flex; flex-direction:column; gap:15px;">
            <div class="stat-card" style="padding:15px;">
              <div class="stat-card__label">Peak Entry Rate</div>
              <div class="stat-card__value" style="font-size:20px;">12,400 / hr</div>
            </div>
            <div class="stat-card" style="padding:15px;">
              <div class="stat-card__label">Current No-Shows</div>
              <div class="stat-card__value" style="font-size:20px; color:var(--accent-warning)">2,143</div>
            </div>
            <button class="twin-control-btn twin-control-btn--active" style="width:100%;">Download CSV</button>
          </div>
        </div>
      </div>

      <!-- ===== Twin Tab ===== -->
      <div class="page-view" data-page="twin">
        <div class="card col-8">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">🏗️</span> 3D Digital Twin</div>
            <span class="card__badge card__badge--ai">3D</span>
          </div>
          <div class="card__body">
            <div class="twin-viewport" style="height:450px;">
              <canvas id="twin-canvas"></canvas>
            </div>
          </div>
        </div>
        <div class="card col-4">
          <div class="card__header">
            <div class="card__title">Twin Environment Controls</div>
          </div>
          <div class="card__body">
            <div class="twin-controls" style="display:flex; flex-direction:column; gap:10px;">
              <button class="twin-control-btn twin-control-btn--active" data-mode="density">Toggle Density View</button>
              <button class="twin-control-btn" data-mode="flow">Toggle Flow View</button>
              <button class="twin-control-btn" data-mode="security">Toggle Security Cam Overlays</button>
            </div>
            <hr style="border:none; border-top:1px solid var(--border-subtle); margin:15px 0;">
            <p style="font-size:12px; color:var(--text-muted); margin-bottom:5px;">Lighting Override</p>
            <input type="range" min="0" max="100" value="80" style="width:100%;">
          </div>
        </div>
      </div>

      <!-- ===== Navigation Tab ===== -->
      <div class="page-view" data-page="navigation">
        <div class="card col-8">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">🗺️</span> Indoor Navigation Map</div>
            <span class="card__badge card__badge--ok">Dynamic</span>
          </div>
          <div class="card__body">
             <div class="nav-map" style="height:450px;">
              <canvas id="nav-canvas"></canvas>
            </div>
          </div>
        </div>
        <div class="card col-4">
          <div class="card__header">
            <div class="card__title">Wayfinding & Routing</div>
          </div>
          <div class="card__body">
            <div class="twin-controls" style="display:flex; flex-direction:column; gap:10px;">
              <button class="twin-control-btn twin-control-btn--active nav-route-btn">Gate A → Food North</button>
              <button class="twin-control-btn nav-route-btn">Gate A → Section A1</button>
              <button class="twin-control-btn nav-route-btn">Section B3 → Gate C</button>
            </div>
            <hr style="border:none; border-top:1px solid var(--border-subtle); margin:15px 0;">
            <button class="twin-control-btn" style="border-color:var(--accent-warning); color:var(--accent-warning); width:100%;">Block Route (Congested)</button>
          </div>
        </div>
      </div>

      <!-- ===== Copilot Tab ===== -->
      <div class="page-view" data-page="copilot">
        <div class="card col-8">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">🤖</span> AI Copilot Interface</div>
            <span class="card__badge card__badge--ai">GPT</span>
          </div>
          <div class="card__body">
            <div class="copilot-panel" style="height:450px;">
              <div class="copilot-messages" id="copilot-messages"></div>
              <div class="copilot-input">
                <input type="text" class="copilot-input__field" id="copilot-input" placeholder="Ask anything about the stadium..." autocomplete="off">
                <button class="copilot-input__send" id="copilot-send">➤</button>
              </div>
            </div>
          </div>
        </div>
        <div class="card col-4">
           <div class="card__header">
            <div class="card__title">Quick Commands</div>
          </div>
          <div class="card__body" style="display:flex; flex-direction:column; gap:10px;">
             <button class="twin-control-btn" onclick="document.getElementById('copilot-input').value='Show me the busiest gate right now.'; document.getElementById('copilot-send').click();">"Show busiest gate"</button>
             <button class="twin-control-btn" onclick="document.getElementById('copilot-input').value='Draft evacuation plan for Section B.'; document.getElementById('copilot-send').click();">"Draft evac plan for Sec B"</button>
             <button class="twin-control-btn" onclick="document.getElementById('copilot-input').value='What is the predicted wait time at half time?'; document.getElementById('copilot-send').click();">"Predict half-time wait"</button>
          </div>
        </div>
      </div>

      <!-- ===== Teams Tab ===== -->
      <div class="page-view" data-page="teams">
        <div class="card col-8">
           <div class="card__header">
            <div class="card__title"><span class="card__title-icon">👥</span> Team Roster</div>
            <span class="card__badge card__badge--ok">6 Active</span>
          </div>
          <div class="card__body">
             <div class="team-grid">
              <div class="team-member">
                <div class="team-member__avatar" style="background:linear-gradient(135deg,#6366f1,#8b5cf6)">AJ</div>
                <div>
                  <div class="team-member__name">Alpha Team — AJ Martinez</div>
                  <div class="team-member__role">Security Lead · Gate A</div>
                </div>
                <div class="team-member__status team-member__status--online"></div>
              </div>
              <div class="team-member">
                <div class="team-member__avatar" style="background:linear-gradient(135deg,#10b981,#06b6d4)">RK</div>
                <div>
                  <div class="team-member__name">Bravo Team — R. Kapoor</div>
                  <div class="team-member__role">Crowd Ops · North Stand</div>
                </div>
                <div class="team-member__status team-member__status--online"></div>
              </div>
              <div class="team-member">
                <div class="team-member__avatar" style="background:linear-gradient(135deg,#f59e0b,#ef4444)">SC</div>
                <div>
                  <div class="team-member__name">Charlie Team — S. Chen</div>
                  <div class="team-member__role">Operations · Food Court South</div>
                </div>
                <div class="team-member__status team-member__status--busy"></div>
              </div>
              <div class="team-member">
                <div class="team-member__avatar" style="background:linear-gradient(135deg,#06b6d4,#6366f1)">DL</div>
                <div>
                  <div class="team-member__name">Delta Team — D. Lee</div>
                  <div class="team-member__role">Security · East Stand</div>
                </div>
                <div class="team-member__status team-member__status--online"></div>
              </div>
              <div class="team-member">
                <div class="team-member__avatar" style="background:linear-gradient(135deg,#ec4899,#8b5cf6)">EN</div>
                <div>
                  <div class="team-member__name">Echo Team — E. Nakamura</div>
                  <div class="team-member__role">Medical · Standby</div>
                </div>
                <div class="team-member__status team-member__status--online"></div>
              </div>
              <div class="team-member">
                <div class="team-member__avatar" style="background:linear-gradient(135deg,#ef4444,#f59e0b)">M1</div>
                <div>
                  <div class="team-member__name">Medic-1 — Dr. A. Patel</div>
                  <div class="team-member__role">Medical · Section 12B (deployed)</div>
                </div>
                <div class="team-member__status team-member__status--busy"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="card col-4">
           <div class="card__header">
            <div class="card__title">Team Actions</div>
          </div>
          <div class="card__body" style="display:flex; flex-direction:column; gap:10px;">
            <button class="twin-control-btn twin-control-btn--active">Broadcast to All Teams</button>
            <button class="twin-control-btn">Dispatch Medical Team</button>
            <button class="twin-control-btn">Call Security Backup</button>
          </div>
        </div>
      </div>
"""

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<div class="dashboard" id="dashboard-grid">' in line:
        start_idx = i
    if '</div><!-- /dashboard -->' in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + [new_html] + lines[end_idx+1:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Success")
else:
    print("Failed to find boundaries", start_idx, end_idx)
