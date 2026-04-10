"""
StadiumOS Antigravity — Backend API Server
=============================================
Flask + WebSocket server providing real-time
stadium telemetry and AI services.
"""

import json
import os
import random
import threading
import time
from datetime import datetime

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Import AI modules
from ai.crowd_predictor import CrowdPredictor
from ai.anomaly_detector import AnomalyDetector
from ai.queue_optimizer import QueueOptimizer

# ─── App Setup ───────────────────────────────────────────────
app = Flask(__name__, static_folder='../') 
CORS(app)

# Load stadium config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'data', 'stadium_config.json')
with open(CONFIG_PATH, 'r') as f:
    STADIUM_CONFIG = json.load(f)

# Initialize AI engines
crowd_predictor = CrowdPredictor(total_capacity=52000)
anomaly_detector = AnomalyDetector()
queue_optimizer = QueueOptimizer()

# Simulation state
simulation_state = {
    'is_running': True,
    'tick': 0,
    'phase': 'first-half',
    'total_attendance': 47832,
    'alerts': [],
}


# ─── Static File Serving ─────────────────────────────────────
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.static_folder, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.static_folder, 'js'), filename)


# ─── API: Stadium Config ─────────────────────────────────────
@app.route('/api/config')
def get_config():
    """Return stadium configuration."""
    return jsonify(STADIUM_CONFIG)


# ─── API: Live Dashboard Data ────────────────────────────────
@app.route('/api/dashboard')
def get_dashboard():
    """Return aggregated dashboard data."""
    occupancy = crowd_predictor.current_occupancy
    total = sum(occupancy.values())
    
    queue_status = queue_optimizer.get_all_status()
    avg_wait = sum(q['wait_min'] for q in queue_status) / len(queue_status)
    
    hotspots = crowd_predictor.get_congestion_hotspots()
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'phase': simulation_state['phase'],
        'kpis': {
            'total_attendance': total,
            'capacity': 52000,
            'fill_rate': round(total / 52000 * 100, 1),
            'avg_wait_min': round(avg_wait, 1),
            'active_incidents': len([a for a in simulation_state['alerts'] if a.get('status') == 'active']),
            'satisfaction_score': max(60, min(99, 87 + random.randint(-3, 3))),
            'ai_interventions': 23 + simulation_state['tick'] // 10,
        },
        'zone_densities': {
            zone: round(count / crowd_predictor.zone_capacities.get(zone, 1) * 100, 1)
            for zone, count in occupancy.items()
        },
        'hotspots': hotspots,
        'queue_summary': queue_status,
        'risk_score': anomaly_detector.get_risk_score(),
    })


# ─── API: Crowd Prediction ───────────────────────────────────
@app.route('/api/predict/zone/<zone_id>')
def predict_zone(zone_id):
    """Get crowd prediction for a specific zone."""
    minutes = request.args.get('minutes', 15, type=int)
    sims = request.args.get('simulations', 500, type=int)
    result = crowd_predictor.monte_carlo_predict(zone_id, minutes, sims)
    return jsonify(result)

@app.route('/api/predict/all')
def predict_all():
    """Get crowd predictions for all zones."""
    minutes = request.args.get('minutes', 15, type=int)
    results = crowd_predictor.predict_all_zones(minutes)
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'prediction_horizon_minutes': minutes,
        'predictions': results,
    })


# ─── API: Queue Management ───────────────────────────────────
@app.route('/api/queues')
def get_queues():
    """Get all queue statuses."""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'queues': queue_optimizer.get_all_status(),
    })

@app.route('/api/queues/optimize/<queue_id>')
def optimize_queue(queue_id):
    """Get optimization recommendation for a queue."""
    result = queue_optimizer.optimize_counters(queue_id)
    return jsonify(result)

@app.route('/api/queues/reroute')
def reroute_queues():
    """Get rerouting suggestions."""
    return jsonify({
        'suggestions': queue_optimizer.get_reroute_suggestions(),
    })


# ─── API: Anomaly Detection ──────────────────────────────────
@app.route('/api/anomalies')
def get_anomalies():
    """Get recent anomalies."""
    return jsonify({
        'total_detected': len(anomaly_detector.anomaly_log),
        'recent': anomaly_detector.anomaly_log[-20:],
        'risk_score': anomaly_detector.get_risk_score(),
    })


# ─── API: Emergency Actions ──────────────────────────────────
@app.route('/api/emergency/lockdown', methods=['POST'])
def trigger_lockdown():
    """Trigger stadium lockdown."""
    simulation_state['alerts'].append({
        'type': 'critical',
        'title': 'LOCKDOWN INITIATED',
        'description': 'All gates sealed. Security deployed.',
        'timestamp': datetime.now().isoformat(),
        'status': 'active',
    })
    return jsonify({'status': 'lockdown_activated', 'timestamp': datetime.now().isoformat()})

@app.route('/api/emergency/dispatch', methods=['POST'])
def dispatch_team():
    """Dispatch a response team."""
    data = request.get_json() or {}
    team_id = data.get('team_id', 'alpha')
    zone = data.get('zone', 'gate-a')
    
    return jsonify({
        'status': 'dispatched',
        'team': team_id,
        'zone': zone,
        'estimated_arrival': '2 minutes',
        'timestamp': datetime.now().isoformat(),
    })

@app.route('/api/emergency/broadcast', methods=['POST'])
def pa_broadcast():
    """Send PA broadcast."""
    data = request.get_json() or {}
    message = data.get('message', 'Attention: Please follow staff directions.')
    zones = data.get('zones', ['all'])
    
    return jsonify({
        'status': 'broadcast_sent',
        'message': message,
        'zones': zones,
        'timestamp': datetime.now().isoformat(),
    })


# ─── API: Teams ──────────────────────────────────────────────
@app.route('/api/teams')
def get_teams():
    """Get team status."""
    return jsonify({
        'teams': STADIUM_CONFIG['stadium']['teams'],
        'timestamp': datetime.now().isoformat(),
    })


# ─── API: AI Copilot ─────────────────────────────────────────
@app.route('/api/copilot/query', methods=['POST'])
def copilot_query():
    """Process natural language query from AI copilot."""
    data = request.get_json() or {}
    query = data.get('query', '').lower()
    
    # Simple NLP-like query routing
    occupancy = crowd_predictor.current_occupancy
    if any(w in query for w in ['busy', 'crowd', 'density', 'congestion']):
        hotspots = crowd_predictor.get_congestion_hotspots()
        return jsonify({
            'response_type': 'crowd_analysis',
            'data': {
                'hotspots': hotspots,
                'total_occupancy': sum(occupancy.values()),
                'capacity': 52000,
            },
            'summary': f"Currently tracking {sum(occupancy.values()):,} attendees. "
                       f"{'No congestion hotspots.' if not hotspots else f'{len(hotspots)} hotspot(s) detected.'}",
        })
    
    elif any(w in query for w in ['queue', 'wait', 'line', 'food']):
        queues = queue_optimizer.get_all_status()
        return jsonify({
            'response_type': 'queue_status',
            'data': queues,
            'summary': f"Monitoring {len(queues)} queue points. "
                       f"Average wait: {sum(q['wait_min'] for q in queues)/len(queues):.1f} minutes.",
        })
    
    elif any(w in query for w in ['predict', 'forecast', 'expect']):
        predictions = crowd_predictor.predict_all_zones(15)
        return jsonify({
            'response_type': 'predictions',
            'data': predictions[:5],
            'summary': f"Top prediction: {predictions[0]['zone_id']} at {predictions[0]['predicted_density']}% "
                       f"(risk: {predictions[0]['risk_level']}).",
        })
    
    else:
        return jsonify({
            'response_type': 'general',
            'summary': f"Stadium is at {sum(occupancy.values())/52000*100:.1f}% capacity. "
                       f"Risk score: {anomaly_detector.get_risk_score():.0f}/100. "
                       f"All systems operational.",
        })


# ─── API: System Health ──────────────────────────────────────
@app.route('/api/health')
def health_check():
    """System health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'uptime_seconds': simulation_state['tick'] * 3,
        'modules': {
            'crowd_predictor': 'active',
            'anomaly_detector': 'active',
            'queue_optimizer': 'active',
        },
        'timestamp': datetime.now().isoformat(),
    })


# ─── Background Simulation Thread ────────────────────────────
def simulation_loop():
    """Background thread that simulates real-time stadium data."""
    while simulation_state['is_running']:
        simulation_state['tick'] += 1
        
        # Advance crowd simulation
        crowd_predictor.simulate_step(phase=simulation_state['phase'])
        
        # Advance queue simulation  
        queue_optimizer.simulate_step()
        
        # Run anomaly detection on all zones
        for zone_id, count in crowd_predictor.current_occupancy.items():
            cap = crowd_predictor.zone_capacities.get(zone_id, 1)
            density = count / cap
            anomaly = anomaly_detector.update(zone_id, density)
            if anomaly:
                simulation_state['alerts'].append(anomaly)
        
        # Keep alerts manageable
        if len(simulation_state['alerts']) > 100:
            simulation_state['alerts'] = simulation_state['alerts'][-50:]
        
        time.sleep(3)  # Update every 3 seconds


# ─── Main Entry Point ────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("🏟️  StadiumOS Antigravity — Backend Server")
    print("=" * 60)
    print(f"Stadium: {STADIUM_CONFIG['stadium']['name']}")
    print(f"Event:   {STADIUM_CONFIG['stadium']['event']}")
    print(f"Zones:   {len(STADIUM_CONFIG['stadium']['zones'])}")
    print(f"Sensors: {len(STADIUM_CONFIG['stadium']['iot_sensors'])}")
    print(f"Teams:   {len(STADIUM_CONFIG['stadium']['teams'])}")
    print("-" * 60)
    
    # Start background simulation
    sim_thread = threading.Thread(target=simulation_loop, daemon=True)
    sim_thread.start()
    print("✅ Simulation engine started")
    print("✅ AI modules loaded (crowd predictor, anomaly detector, queue optimizer)")
    print(f"\n🌐 Server running at http://localhost:5000")
    print("-" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
