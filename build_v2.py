html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="StadiumOS Antigravity — AI-powered command center for large-scale sporting venues.">
  <title>StadiumOS Antigravity — AI Stadium Command Center</title>
  <link rel="stylesheet" href="css/stadium-os.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='28' font-size='28'>🏟️</text></svg>">
</head>
<body>

  <!-- Antigravity Particle Background -->
  <canvas id="particle-canvas"></canvas>

  <!-- Ambient Light Orbs -->
  <div class="ambient-orb ambient-orb--primary"></div>
  <div class="ambient-orb ambient-orb--secondary"></div>
  <div class="ambient-orb ambient-orb--cyan"></div>

  <!-- App Shell -->
  <div class="app">

    <!-- ===== Sidebar Navigation ===== -->
    <nav class="sidebar">
      <div class="sidebar__logo" title="StadiumOS">⚡</div>
      <div class="sidebar__nav">
        <div class="sidebar__item sidebar__item--active" data-view="dashboard" id="nav-dashboard">
          🏠 <span class="tooltip">Dashboard</span>
        </div>
        <div class="sidebar__item" data-view="heatmap" id="nav-heatmap">
          🔥 <span class="tooltip">Crowd Heatmap</span>
        </div>
        <div class="sidebar__item" data-view="queues" id="nav-queues">
          ⏱️ <span class="tooltip">Queue Management</span>
        </div>
        <div class="sidebar__item" data-view="emergency" id="nav-emergency">
          🚨 <span class="tooltip">Emergency Console</span>
        </div>
        <div class="sidebar__item" data-view="analytics" id="nav-analytics">
          📊 <span class="tooltip">Analytics</span>
        </div>
        <div class="sidebar__item" data-view="twin" id="nav-twin">
          🏗️ <span class="tooltip">Digital Twin</span>
        </div>
        <div class="sidebar__item" data-view="navigation" id="nav-navigation">
          🗺️ <span class="tooltip">Navigation</span>
        </div>
        <div class="sidebar__item" data-view="teams" id="nav-teams">
          👥 <span class="tooltip">Teams</span>
        </div>
      </div>
      <div class="sidebar__bottom">
        <div class="sidebar__status" title="Systems Online"></div>
      </div>
    </nav>

    <!-- ===== Main Area ===== -->
    <main class="main">

      <!-- Top Bar -->
      <header class="topbar">
        <div class="topbar__left">
          <div>
            <div class="topbar__title">StadiumOS Antigravity</div>
            <div class="topbar__subtitle">MetLife Stadium • NFL Week 14 — Giants vs Eagles</div>
          </div>
          <div class="live-badge">
            <div class="live-badge__dot"></div>
            LIVE
          </div>
        </div>
        <div class="topbar__right" style="position:relative;">
          <div class="topbar__clock" id="topbar-clock">00:00:00</div>
          
          <div class="dropdown-wrapper">
             <button class="topbar__btn" id="btn-alerts" title="Alerts">
               🔔 <span class="notif-dot"></span>
             </button>
             <div class="dropdown-menu" id="dropdown-alerts">
               <h4 style="margin-bottom:10px; font-size:12px; border-bottom:1px solid var(--border-subtle); padding-bottom:5px;">Recent Alerts</h4>
               <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">HIGH: Gate B Congestion (ETA 5m) <button class="twin-control-btn" style="padding:2px 8px; font-size:10px;">Acknowledge</button></div>
               <div style="font-size:12px; margin-bottom:8px;">MED: Stand 314 Temp Variance <button class="twin-control-btn" style="padding:2px 8px; font-size:10px;">Review</button></div>
               <div style="font-size:12px; color:var(--text-muted);">LOW: Network latency spike cleared.</div>
               <button class="twin-control-btn" style="width:100%; margin-top:10px; padding:4px;">View All Alerts</button>
             </div>
          </div>

          <div class="dropdown-wrapper">
             <button class="topbar__btn" id="btn-settings" title="Settings">⚙️</button>
             <div class="dropdown-menu" id="dropdown-settings">
               <h4 style="margin-bottom:10px; font-size:12px; border-bottom:1px solid var(--border-subtle); padding-bottom:5px;">System Configuration</h4>
               <label style="font-size:11px; display:flex; justify-content:space-between; margin-bottom:10px;">Telemetry Update Rate <select style="background:var(--bg-void); color:white; border:1px solid var(--border-subtle)"><option>1s (Live)</option><option>5s</option></select></label>
               <label style="font-size:11px; display:flex; justify-content:space-between; margin-bottom:10px;">Predictive Overlays <input type="checkbox" checked></label>
               <label style="font-size:11px; display:flex; justify-content:space-between;">Thermal Imaging <input type="checkbox"></label>
               <button class="twin-control-btn" style="width:100%; margin-top:15px; padding:4px;">Advanced Settings</button>
             </div>
          </div>

          <div class="dropdown-wrapper">
             <div class="topbar__avatar" id="btn-admin" title="Admin">SB</div>
             <div class="dropdown-menu" id="dropdown-admin" style="right:0;">
               <h4 style="margin-bottom:10px; font-size:12px; border-bottom:1px solid var(--border-subtle); padding-bottom:5px;">Administrator</h4>
               <div style="font-size:12px; margin-bottom:15px; color:var(--text-muted)">Session Authorization: Level 4</div>
               <button class="twin-control-btn" style="width:100%; text-align:left; margin-bottom:5px;">Initiate Shift Handover</button>
               <button class="twin-control-btn" style="width:100%; text-align:left; margin-bottom:5px;">Export Logs & Compliance</button>
               <button class="twin-control-btn" style="width:100%; text-align:left; border-color:var(--accent-danger); color:var(--accent-danger)">Lock Command Session</button>
             </div>
          </div>
        </div>
      </header>

      <!-- ===== Dashboard Tab (Default) ===== -->
      <div class="page-view page-view--active" data-page="dashboard" id="dashboard-grid">
        <div class="stats-row" style="grid-column: span 12; margin-bottom:5px;">
          <div class="stat-card">
            <div class="stat-card__icon stat-card__icon--primary">👥</div>
            <div class="stat-card__label">Total Attendance</div>
            <div class="stat-card__value" id="kpi-attendance" style="font-size:32px;">47,832</div>
            <div class="stat-card__trend stat-card__trend--up">↑ 12% (<span style="color:#fff">Target: 44k</span>)</div>
          </div>
          <div class="stat-card">
            <div class="stat-card__icon stat-card__icon--success">⏱️</div>
            <div class="stat-card__label">System Flow Rate</div>
            <div class="stat-card__value" id="kpi-avg-wait" style="font-size:32px;">1.4s</div>
            <div class="stat-card__trend stat-card__trend--up">Entry Per Passenger (Optimal)</div>
          </div>
          <div class="stat-card">
            <div class="stat-card__icon stat-card__icon--warning">🚨</div>
            <div class="stat-card__label">Active Incidents</div>
            <div class="stat-card__value" id="kpi-incidents" style="font-size:32px;">3</div>
            <div class="stat-card__trend stat-card__trend--neutral">All contained to Outer Ring.</div>
          </div>
          <div class="stat-card">
            <div class="stat-card__icon stat-card__icon--cyan">🛒</div>
            <div class="stat-card__label">Avg Cart Payload</div>
            <div class="stat-card__value" id="kpi-satisfaction" style="font-size:32px;">$34</div>
            <div class="stat-card__trend stat-card__trend--up">↑ +$4 via Dynamic Signage</div>
          </div>
        </div>

        <div class="card col-8">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">⚡</span> In-Depth Crowd Demographics & Briefing</div>
          </div>
          <div class="card__body" style="display:flex; gap: 20px;">
            <div style="flex: 2;">
              <h3 style="margin-bottom:10px; color:var(--accent-primary)">All systems nominal. Pre-Game Surge Expected in 14 mins.</h3>
              <p style="color:var(--text-muted); font-size:13px; margin-bottom:15px; line-height: 1.6;">
                The current match proceeds without major interruption. Weather is clear, internal bowl temp is 72°F. Wait times are well within normal bounds. There are 3 active low-level security incidents currently being addressed by Team Alpha and Charlie.<br><br>
                <strong>Crowd Profile:</strong> Analyzing ticketing profiles, the audience is leaning 62% Away-Side supporters in South Endzones. We recommend adjusting POS displays in South Concourse to higher margins items matching historical away-fan preferences.
              </p>
            </div>
          </div>
        </div>
        <div class="card col-4">
          <div class="card__header">
             <div class="card__title">Global Directives</div>
          </div>
          <div class="card__body" style="display:flex; flex-direction:column; gap:10px;">
             <button class="twin-control-btn twin-control-btn--active" style="width:100%; text-align:left;">↳ Initialize Match Start Sequence</button>
             <button class="twin-control-btn" style="width:100%; text-align:left;">↳ Deploy Secondary Concession Units</button>
             <button class="twin-control-btn" style="width:100%; text-align:left;">↳ Trigger Synchronized Lighting Test</button>
             <button class="twin-control-btn" style="width:100%; text-align:left;">↳ Generate Operational Daily Report</button>
          </div>
        </div>
      </div>

      <!-- ===== Heatmap Tab ===== -->
      <div class="page-view" data-page="heatmap">
        <div class="card col-8">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">🔥</span> Crowd Density & Thermals</div>
            <span class="card__badge card__badge--live">● Live Tracking</span>
          </div>
          <div class="card__body">
            <div class="heatmap-container" style="height:450px;">
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
            <div class="card__title">Layered Analysis Controls</div>
          </div>
          <div class="card__body" style="display:flex; flex-direction:column; gap:15px; overflow-y:auto; max-height:450px;">
            <div>
              <p style="font-size:12px; color:var(--text-muted); margin-bottom:5px;">Predictive Chronology Engine</p>
              <input type="range" min="-30" max="60" value="0" style="width:100%; margin-bottom:5px;">
              <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-muted);">
                <span>-30 Mins (Replay)</span> <span>Now</span> <span>+60 Mins (Forecast)</span>
              </div>
            </div>
            <hr style="border:none; border-top:1px solid var(--border-subtle);">
            <div>
              <h4 style="margin-bottom:10px; font-size:13px;">Layer Isolation Overlays</h4>
              <div style="display:flex; gap:10px; flex-wrap:wrap;">
                 <label class="twin-control-btn twin-control-btn--active" style="flex:1; text-align:center;"><input type="checkbox" style="display:none;" checked> Density</label>
                 <label class="twin-control-btn" style="flex:1; text-align:center;"><input type="checkbox" style="display:none;"> Ticket Class</label>
                 <label class="twin-control-btn" style="flex:1; text-align:center;"><input type="checkbox" style="display:none;"> Demographics</label>
                 <label class="twin-control-btn" style="flex:1; text-align:center;"><input type="checkbox" style="display:none;"> Thermals</label>
              </div>
            </div>
            <hr style="border:none; border-top:1px solid var(--border-subtle);">
            <div>
              <h4 style="margin-bottom:5px; font-size:13px; color:var(--accent-warning)">Detected Hotspots</h4>
              <div style="background:var(--bg-void); border:1px solid rgba(245, 158, 11, 0.2); padding:10px; border-radius:8px; margin-bottom:10px;">
                 <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:5px;">
                   <strong>Gate C Entrance</strong> <span style="color:var(--accent-warning);">88% Density</span>
                 </div>
                 <p style="font-size:11px; color:var(--text-muted); margin-bottom:10px;">Flow bottlenecking at central stanchion. Projection: Gridlock in 4m.</p>
                 <button class="twin-control-btn" style="width:100%; border-color:var(--accent-warning); color:var(--accent-warning); font-size:11px;">Deploy Soft Barriers via Delta Team</button>
              </div>
              <div style="background:var(--bg-void); border:1px solid rgba(245, 158, 11, 0.2); padding:10px; border-radius:8px;">
                 <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:5px;">
                   <strong>Concession Block 4</strong> <span style="color:var(--accent-warning);">94% Capacity</span>
                 </div>
                 <button class="twin-control-btn" style="width:100%; border-color:var(--accent-warning); color:var(--accent-warning); font-size:11px;">Send Mobile Vendors to Area</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== Queues Tab ===== -->
      <div class="page-view" data-page="queues">
        <div class="card col-6">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">⏱️</span> Smart Node Queues</div>
            <span class="card__badge card__badge--ai">Deep Learning</span>
          </div>
          <div class="card__body">
            <div class="queue-list" id="queue-list"></div>
          </div>
        </div>
        <div class="card col-6">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">📊</span> Wait Time Trends & Dynamic Routing</div>
          </div>
          <div class="card__body" style="display:flex; flex-direction:column; gap:15px;">
            <div class="chart-container" style="height:220px;">
              <canvas id="chart-queues"></canvas>
            </div>
            
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px;">
              <div style="background:var(--bg-void); padding:15px; border-radius:8px; border:1px solid var(--border-subtle);">
                <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:5px;">North Endzone Delta</div>
                <div style="font-size:24px; font-family:var(--font-mono); color:var(--accent-primary);">+2m 14s</div>
                <div style="font-size:11px; margin-top:5px; color:var(--accent-danger);">Rising Demand</div>
              </div>
              <div style="background:var(--bg-void); padding:15px; border-radius:8px; border:1px solid var(--border-subtle);">
                <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:5px;">South Endzone Delta</div>
                <div style="font-size:24px; font-family:var(--font-mono); color:var(--accent-success);">-1m 40s</div>
                <div style="font-size:11px; margin-top:5px; color:var(--accent-success);">Efficient Clearance</div>
              </div>
            </div>

            <hr style="border:none; border-top:1px solid var(--border-subtle);">
            
            <h4 style="font-size:13px;">AI Queue Routing Suggestions</h4>
            <div style="display:flex; gap:10px;">
              <button class="twin-control-btn twin-control-btn--active" style="flex:1; padding:12px; font-size:12px;">Open Backup Gate A2 <br><span style="font-size:9px; font-weight:normal; opacity:0.7;">Reduces North wait by 35%</span></button>
              <button class="twin-control-btn" style="flex:1; padding:12px; font-size:12px;">Trigger Concourse Redirect <br><span style="font-size:9px; font-weight:normal; opacity:0.7;">Route 20% to South via Signage</span></button>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== Emergency Tab ===== -->
      <div class="page-view" data-page="emergency">
        <div class="card col-7">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">🚨</span> Threat Matrix & Event Console</div>
            <span class="card__badge card__badge--live">● Global Scan</span>
          </div>
          <div class="card__body">
            <div class="emergency-console">
              <div class="emergency-alerts" id="emergency-alerts" style="max-height:450px;"></div>
            </div>
          </div>
        </div>
        <div class="card col-5">
           <div class="card__header">
             <div class="card__title">Tiered Response Protocols (SOP)</div>
           </div>
           <div class="card__body" style="overflow-y:auto; max-height:480px;">
             
             <!-- Tier 1 Protocol -->
             <div style="border-left:3px solid var(--accent-danger); padding-left:15px; margin-bottom:20px;">
                <h4 style="color:var(--accent-danger); font-size:14px; margin-bottom:5px;">CODE RED ACTIONS</h4>
                <p style="font-size:11px; color:var(--text-muted); margin-bottom:10px;">Critical authority overrides. Use for severe breaches, structural failure, or panic.</p>
                <div style="display:flex; flex-direction:column; gap:8px;">
                   <button class="twin-control-btn" style="border-color:var(--accent-danger); color:var(--accent-danger); width:100%; text-align:left;">⚠️ Isolate Sector & Trigger Blast Doors</button>
                   <button class="twin-control-btn" style="border-color:var(--accent-danger); color:var(--accent-danger); width:100%; text-align:left;">⚠️ Clear Exit Path 4 / Broadcast Evac Map</button>
                   <button class="twin-control-btn" style="background:rgba(239, 68, 68, 0.1); border-color:var(--accent-danger); color:var(--accent-danger); width:100%; text-align:left; font-weight:bold;">🚨 INITIATE STADIUM LOCKDOWN</button>
                </div>
             </div>

             <!-- Tier 2 Protocol -->
             <div style="border-left:3px solid var(--accent-warning); padding-left:15px; margin-bottom:20px;">
                <h4 style="color:var(--accent-warning); font-size:14px; margin-bottom:5px;">CODE YELLOW ACTIONS</h4>
                <p style="font-size:11px; color:var(--text-muted); margin-bottom:10px;">Medical instances, fights, extreme congestion. Handled by rapid response pods.</p>
                <div style="display:flex; flex-direction:column; gap:8px;">
                   <button class="twin-control-btn" style="width:100%; text-align:left;">Dispatch Nearest Med-Pod (Beta Team)</button>
                   <button class="twin-control-btn" style="width:100%; text-align:left;">Deploy De-escalation Squad to Point</button>
                   <button class="twin-control-btn" style="width:100%; text-align:left;">Focus Security PTZ Cameras on Incident</button>
                </div>
             </div>

             <!-- Tier 3 Protocol -->
             <div style="border-left:3px solid var(--accent-success); padding-left:15px;">
                <h4 style="color:var(--accent-success); font-size:14px; margin-bottom:5px;">CODE GREEN ACTIONS</h4>
                <p style="font-size:11px; color:var(--text-muted); margin-bottom:10px;">Routine janitorial, restocking, or general facility requests.</p>
                <div style="display:flex; flex-wrap:wrap; gap:8px;">
                   <button class="twin-control-btn" style="font-size:11px;">Send Janitorial</button>
                   <button class="twin-control-btn" style="font-size:11px;">Restock Vendors</button>
                   <button class="twin-control-btn" style="font-size:11px;">Resolve Ticket Issue</button>
                </div>
             </div>

           </div>
        </div>
      </div>

      <!-- ===== Analytics Tab ===== -->
      <div class="page-view" data-page="analytics">
        <div class="card col-12" style="margin-bottom:0;">
           <div class="card__header">
             <div class="card__title"><span class="card__title-icon">📈</span> Predictive Analytics & Conversion</div>
           </div>
        </div>
        <div class="card col-8">
          <div class="card__body">
            <h4 style="font-size:12px; color:var(--text-muted); margin-bottom:10px;">Attendance Ingress Velocity (Historical vs Current Modeled)</h4>
            <div class="chart-container" style="height:350px;">
              <canvas id="chart-attendance"></canvas>
            </div>
            <div style="display:flex; justify-content:space-around; margin-top:20px;">
              <div style="text-align:center;">
                <div style="font-size:11px; color:var(--text-muted)">Peak Entry Extrapolated</div>
                <div style="font-size:22px; color:var(--accent-primary);">12,400 / hr</div>
              </div>
              <div style="text-align:center;">
                <div style="font-size:11px; color:var(--text-muted)">Projected Dropoff</div>
                <div style="font-size:22px; color:var(--text-primary);">Q1 12:00</div>
              </div>
            </div>
          </div>
        </div>
        <div class="card col-4">
          <div class="card__body" style="display:flex; flex-direction:column; gap:15px; height:100%;">
            <div class="stat-card" style="padding:15px;">
              <div class="stat-card__label">Vendor Sales / Flow Correlation</div>
              <div class="stat-card__value" style="font-size:24px; color:var(--accent-success)">0.84 R²</div>
              <p style="font-size:10px; margin-top:5px; color:var(--text-muted);">High correlation. Higher flow equates to massive boosts in Section 12 concessions.</p>
            </div>
            <div class="stat-card" style="padding:15px;">
              <div class="stat-card__label">Predicted Departure Bottleneck</div>
              <div class="stat-card__value" style="font-size:20px; color:var(--accent-warning)">Gate E (Post-Game)</div>
              <p style="font-size:10px; margin-top:5px; color:var(--text-muted);">Anticipate 45m wait times on transit lines outside Gate E based on demographic exit habits.</p>
            </div>
            
            <div style="flex:1;"></div>
            <button class="twin-control-btn twin-control-btn--active" style="width:100%; padding:15px;">Export Complex Analytics Payload (CSV/JSON)</button>
          </div>
        </div>
      </div>

      <!-- ===== Twin Tab ===== -->
      <div class="page-view" data-page="twin">
        <div class="card col-8">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">🏗️</span> Macro-Scale Digital Twin</div>
            <span class="card__badge card__badge--ai">Unreal Engine Node Integration</span>
          </div>
          <div class="card__body">
            <div class="twin-viewport" style="height:450px;">
              <canvas id="twin-canvas"></canvas>
            </div>
          </div>
        </div>
        <div class="card col-4">
          <div class="card__header">
            <div class="card__title">Live Infrastructure Controls</div>
          </div>
          <div class="card__body" style="overflow-y:auto; max-height:480px;">
            <div class="twin-controls" style="display:flex; flex-direction:column; gap:10px;">
              <button class="twin-control-btn twin-control-btn--active" data-mode="density">Data Over: Density Fields</button>
              <button class="twin-control-btn" data-mode="flow">Data Over: Flow Vectors</button>
              <button class="twin-control-btn" data-mode="security">Data Over: Security Nodes (CCTV)</button>
            </div>
            
            <hr style="border:none; border-top:1px solid var(--border-subtle); margin:20px 0;">
            
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:20px;">
               <div style="background:var(--bg-void); padding:10px; border-radius:6px; text-align:center;">
                  <span style="font-size:10px; color:var(--text-muted); display:block; text-transform:uppercase;">Roof Motor Relays</span>
                  <strong style="color:var(--accent-success); font-size:14px;">LOCKED-OPEN</strong>
               </div>
               <div style="background:var(--bg-void); padding:10px; border-radius:6px; text-align:center;">
                  <span style="font-size:10px; color:var(--text-muted); display:block; text-transform:uppercase;">Structural Tension</span>
                  <strong style="color:var(--accent-success); font-size:14px;">NOMINAL 1.2%</strong>
               </div>
               <div style="background:var(--bg-void); padding:10px; border-radius:6px; text-align:center;">
                  <span style="font-size:10px; color:var(--text-muted); display:block; text-transform:uppercase;">Decibel Levels (Acoustics)</span>
                  <strong style="color:var(--text-primary); font-size:14px;">102 dB avg</strong>
               </div>
               <div style="background:var(--bg-void); padding:10px; border-radius:6px; text-align:center;">
                  <span style="font-size:10px; color:var(--text-muted); display:block; text-transform:uppercase;">Stadium Lighting Matrix</span>
                  <strong style="color:var(--accent-warning); font-size:14px;">80% ON</strong>
               </div>
            </div>

            <p style="font-size:12px; color:var(--text-muted); margin-bottom:5px;">Lighting Bank Dimmer Override</p>
            <input type="range" min="0" max="100" value="80" style="width:100%; margin-bottom:15px;">
            <button class="twin-control-btn" style="width:100%; border-color:var(--accent-danger); color:var(--text-primary);">Test Sprinkler Head Calibration Node</button>
          </div>
        </div>
      </div>

      <!-- ===== Navigation Tab ===== -->
      <div class="page-view" data-page="navigation">
        <div class="card col-8">
          <div class="card__header">
            <div class="card__title"><span class="card__title-icon">🗺️</span> Multithreaded Indoor Wayfinding Matrix</div>
          </div>
          <div class="card__body">
             <div class="nav-map" style="height:480px;">
              <canvas id="nav-canvas"></canvas>
            </div>
          </div>
        </div>
        <div class="card col-4">
          <div class="card__header">
            <div class="card__title">Live Path Orchestration</div>
          </div>
          <div class="card__body" style="overflow-y:auto; max-height:480px;">
            <p style="font-size:12px; color:var(--text-muted); margin-bottom:10px;">Select to highlight and manage traffic flow for simultaneous paths globally integrated to passenger mobile devices.</p>
            <div class="twin-controls" style="display:flex; flex-direction:column; gap:10px;">
              <div style="border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                   <strong style="font-size:13px;">Gate A → Food North</strong>
                   <span class="card__badge card__badge--ok">Clear</span>
                </div>
                <div style="display:flex; gap:5px;">
                  <button class="twin-control-btn twin-control-btn--active nav-route-btn" style="flex:1; padding:5px; font-size:11px;">View</button>
                  <button class="twin-control-btn" style="flex:1; padding:5px; font-size:11px;">Stall Route</button>
                </div>
              </div>
              <div style="border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                   <strong style="font-size:13px;">Gate A → Section A1</strong>
                   <span class="card__badge" style="background:rgba(245,158,11,0.2); color:var(--accent-warning);">Med Traffic</span>
                </div>
                <div style="display:flex; gap:5px;">
                  <button class="twin-control-btn nav-route-btn" style="flex:1; padding:5px; font-size:11px;">View</button>
                  <button class="twin-control-btn" style="flex:1; padding:5px; font-size:11px;">Stall Route</button>
                </div>
              </div>
              <div style="border:1px solid var(--border-medium); padding:10px; border-radius:8px; background:rgba(239,68,68,0.05);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                   <strong style="font-size:13px;">Section B3 → Gate C</strong>
                   <span class="card__badge" style="background:rgba(239,68,68,0.2); color:var(--accent-danger);">Bottlenecked</span>
                </div>
                <div style="display:flex; gap:5px;">
                  <button class="twin-control-btn nav-route-btn" style="flex:1; padding:5px; font-size:11px;">View</button>
                  <button class="twin-control-btn" style="flex:1; padding:5px; font-size:11px; border-color:var(--accent-danger); color:var(--accent-danger)">Hard Block & Reroute</button>
                </div>
              </div>
               <div style="border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                   <strong style="font-size:13px;">VIP Lounge → Box Suites</strong>
                   <span class="card__badge card__badge--ok">Clear</span>
                </div>
                <div style="display:flex; gap:5px;">
                   <button class="twin-control-btn nav-route-btn" style="flex:1; padding:5px; font-size:11px;">View</button>
                   <button class="twin-control-btn" style="flex:1; padding:5px; font-size:11px;">Lock VIP Turnstiles</button>
                </div>
              </div>
            </div>
            
          </div>
        </div>
      </div>


      <!-- ===== Teams Tab ===== -->
      <div class="page-view" data-page="teams">
        <div class="card col-12">
           <div class="card__header">
            <div class="card__title"><span class="card__title-icon">👥</span> Advanced Tactical Personnel Roster</div>
            <div style="display:flex; gap:10px;">
              <button class="twin-control-btn twin-control-btn--active" style="padding:4px 12px; font-size:11px;">Broadcast to All Nodes</button>
              <button class="twin-control-btn" style="padding:4px 12px; font-size:11px;">Deploy QRF (Quick Reaction Force)</button>
            </div>
          </div>
          <div class="card__body">
             <div class="team-grid" style="grid-template-columns: repeat(3, 1fr); gap:20px;">
              <!-- Roster 1 -->
              <div class="team-member" style="flex-direction:column; align-items:flex-start; padding:15px; border:1px solid var(--border-subtle); position:relative;">
                <div class="team-member__status team-member__status--online" style="position:absolute; top:15px; right:15px;"></div>
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                  <div class="team-member__avatar" style="background:linear-gradient(135deg,#6366f1,#8b5cf6); width:48px; height:48px; font-size:18px;">AJ</div>
                  <div>
                    <div class="team-member__name" style="font-size:16px;">Alpha Tactical</div>
                    <div class="team-member__role">Security Lead · Gate A</div>
                  </div>
                </div>
                <div style="display:flex; gap:20px; font-size:11px; margin-bottom:15px; background:var(--bg-void); padding:10px; width:100%; border-radius:6px; color:var(--text-muted);">
                  <div>BPM: <strong style="color:var(--accent-success)">92</strong></div>
                  <div>BAT: <strong style="color:#fff">84%</strong></div>
                  <div>LINK: <strong style="color:var(--accent-success)">SECURE</strong></div>
                </div>
                <div style="display:flex; gap:5px; width:100%;">
                   <button class="twin-control-btn" style="flex:1; font-size:10px; padding:6px;">Msg</button>
                   <button class="twin-control-btn" style="flex:2; font-size:10px; padding:6px;">Reassign Vector</button>
                </div>
              </div>

               <!-- Roster 2 -->
              <div class="team-member" style="flex-direction:column; align-items:flex-start; padding:15px; border:1px solid var(--border-subtle); position:relative;">
                <div class="team-member__status team-member__status--online" style="position:absolute; top:15px; right:15px;"></div>
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                  <div class="team-member__avatar" style="background:linear-gradient(135deg,#10b981,#06b6d4); width:48px; height:48px; font-size:18px;">RK</div>
                  <div>
                    <div class="team-member__name" style="font-size:16px;">Bravo Ops</div>
                    <div class="team-member__role">Crowd Flow · North</div>
                  </div>
                </div>
                <div style="display:flex; gap:20px; font-size:11px; margin-bottom:15px; background:var(--bg-void); padding:10px; width:100%; border-radius:6px; color:var(--text-muted);">
                  <div>BPM: <strong style="color:#fff">81</strong></div>
                  <div>BAT: <strong style="color:#fff">90%</strong></div>
                  <div>LINK: <strong style="color:var(--accent-success)">SECURE</strong></div>
                </div>
                <div style="display:flex; gap:5px; width:100%;">
                   <button class="twin-control-btn" style="flex:1; font-size:10px; padding:6px;">Msg</button>
                   <button class="twin-control-btn" style="flex:2; font-size:10px; padding:6px;">Reassign Vector</button>
                </div>
              </div>

              <!-- Roster 3 -->
              <div class="team-member" style="flex-direction:column; align-items:flex-start; padding:15px; border:1px solid var(--border-medium); background:rgba(245,158,11,0.05); position:relative;">
                <div class="team-member__status team-member__status--busy" style="position:absolute; top:15px; right:15px;"></div>
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                  <div class="team-member__avatar" style="background:linear-gradient(135deg,#f59e0b,#ef4444); width:48px; height:48px; font-size:18px;">SC</div>
                  <div>
                    <div class="team-member__name" style="font-size:16px;">Charlie Ops</div>
                    <div class="team-member__role">Incident Res. · South</div>
                  </div>
                </div>
                <div style="display:flex; gap:20px; font-size:11px; margin-bottom:15px; background:var(--bg-void); padding:10px; width:100%; border-radius:6px; color:var(--text-muted);">
                  <div>BPM: <strong style="color:var(--accent-warning)">124</strong></div>
                  <div>BAT: <strong style="color:var(--accent-warning)">18%</strong></div>
                  <div>LINK: <strong style="color:var(--accent-success)">SECURE</strong></div>
                </div>
                <div style="display:flex; gap:5px; width:100%;">
                   <button class="twin-control-btn" style="flex:1; font-size:10px; padding:6px;">Msg</button>
                   <button class="twin-control-btn" style="flex:2; font-size:10px; padding:6px; border-color:var(--accent-warning); color:var(--accent-warning);">Override to Base</button>
                </div>
              </div>

              <!-- Additional teams... -->
              <!-- Medic -->
              <div class="team-member" style="flex-direction:column; align-items:flex-start; padding:15px; border:1px solid var(--border-subtle); position:relative;">
                <div class="team-member__status team-member__status--busy" style="position:absolute; top:15px; right:15px;"></div>
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                   <div class="team-member__avatar" style="background:linear-gradient(135deg,#ef4444,#f59e0b); width:48px; height:48px; font-size:18px;">M1</div>
                  <div>
                    <div class="team-member__name" style="font-size:16px;">Medic-1 Prime</div>
                    <div class="team-member__role">Deployed · Sec 12B</div>
                  </div>
                </div>
                <div style="display:flex; gap:20px; font-size:11px; margin-bottom:15px; background:var(--bg-void); padding:10px; width:100%; border-radius:6px; color:var(--text-muted);">
                  <div>ETA: <strong style="color:#fff">ARRIVED</strong></div>
                  <div>KIT: <strong style="color:#fff">TRAUMA</strong></div>
                </div>
                <div style="display:flex; gap:5px; width:100%;">
                   <button class="twin-control-btn" style="flex:1; font-size:10px; padding:6px;">Open Tele-Med Link</button>
                </div>
              </div>
              
            </div>
          </div>
        </div>
      </div><!-- /teams -->

    </main>

  </div><!-- /app -->
  
  <!-- FLoating Copilot Agent -->
  <div class="floating-copilot" id="floating-copilot">
    <div class="floating-copilot__header" id="copilot-toggle">
       <span>🤖 AI Stadium Agent</span>
       <span id="copilot-caret">▼</span>
    </div>
    <div class="floating-copilot__body">
       <div class="copilot-panel">
         <div class="copilot-messages" id="copilot-messages" style="height:250px;"></div>
         <div style="display:flex; gap:5px; margin-bottom:5px; overflow-x:auto; padding-bottom:5px; white-space:nowrap;" class="copilot-chips">
            <button class="twin-control-btn" style="padding:4px 8px; font-size:10px;" onclick="document.getElementById('copilot-input').value='Show busiest gate';document.getElementById('copilot-send').click();">"Busiest Gate"</button>
            <button class="twin-control-btn" style="padding:4px 8px; font-size:10px;" onclick="document.getElementById('copilot-input').value='Evac plan for Sec B';document.getElementById('copilot-send').click();">"Evac Plan"</button>
            <button class="twin-control-btn" style="padding:4px 8px; font-size:10px;" onclick="document.getElementById('copilot-input').value='Predict wait times at half time';document.getElementById('copilot-send').click();">"Wait Predict"</button>
         </div>
         <div class="copilot-input">
           <input type="text" class="copilot-input__field" id="copilot-input" placeholder="Ask anything..." autocomplete="off">
           <button class="copilot-input__send" id="copilot-send">➤</button>
         </div>
       </div>
    </div>
  </div>

  <!-- Scripts (order matters) -->
  <script src="js/particles.js"></script>
  <script src="js/heatmap.js"></script>
  <script src="js/queue-manager.js"></script>
  <script src="js/emergency.js"></script>
  <script src="js/analytics.js"></script>
  <script src="js/ai-copilot.js"></script>
  <script src="js/digital-twin.js"></script>
  <script src="js/navigation.js"></script>
  <script src="js/app.js"></script>

</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("index.html completely rewritten with V2 enhancements.")
