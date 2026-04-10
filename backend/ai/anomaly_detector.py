"""
StadiumOS Antigravity — Anomaly Detection Module
=================================================
Statistical anomaly detection for crowd behavior,
security events, and operational irregularities.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import math


class AnomalyDetector:
    """Real-time anomaly detection engine for stadium events.
    
    Detection methods:
    - Z-score based statistical anomaly detection
    - Rate-of-change spike detection
    - Pattern deviation (expected vs actual)
    - Multi-zone correlation analysis
    """

    def __init__(self):
        self.history: Dict[str, List[float]] = {}
        self.window_size = 30  # Rolling window for stats
        self.z_threshold = 2.5  # Z-score threshold for anomalies
        self.spike_threshold = 0.15  # Rate of change threshold (15%)
        self.active_anomalies: List[Dict] = []
        self.anomaly_log: List[Dict] = []

    def update(self, zone_id: str, density: float) -> Optional[Dict]:
        """Update zone data and check for anomalies.
        
        Args:
            zone_id: Zone identifier
            density: Current density (0-1 scale)
            
        Returns:
            Anomaly dict if detected, None otherwise
        """
        if zone_id not in self.history:
            self.history[zone_id] = []
        
        self.history[zone_id].append(density)
        
        # Keep only recent history
        if len(self.history[zone_id]) > self.window_size * 2:
            self.history[zone_id] = self.history[zone_id][-self.window_size:]
        
        # Need minimum samples for detection
        if len(self.history[zone_id]) < 5:
            return None
        
        anomaly = None
        
        # Check 1: Z-score anomaly
        z_result = self._check_zscore(zone_id, density)
        if z_result:
            anomaly = z_result
        
        # Check 2: Spike detection
        spike_result = self._check_spike(zone_id, density)
        if spike_result and (not anomaly or spike_result['severity'] > anomaly.get('severity_score', 0)):
            anomaly = spike_result
        
        if anomaly:
            anomaly['timestamp'] = datetime.now().isoformat()
            self.anomaly_log.append(anomaly)
            if len(self.anomaly_log) > 500:
                self.anomaly_log = self.anomaly_log[-250:]
        
        return anomaly

    def _check_zscore(self, zone_id: str, value: float) -> Optional[Dict]:
        """Statistical z-score anomaly detection."""
        data = np.array(self.history[zone_id][-self.window_size:])
        mean = np.mean(data)
        std = np.std(data)
        
        if std < 0.001:  # Avoid division by near-zero
            return None
        
        z_score = abs((value - mean) / std)
        
        if z_score > self.z_threshold:
            severity = 'critical' if z_score > 4.0 else 'high' if z_score > 3.0 else 'medium'
            return {
                'type': 'statistical_anomaly',
                'zone_id': zone_id,
                'description': f'Unusual density pattern in {zone_id}. Current: {value:.1%}, Expected range: {mean - 2*std:.1%} to {mean + 2*std:.1%}',
                'z_score': round(z_score, 2),
                'severity': severity,
                'severity_score': z_score,
                'current_value': round(value, 3),
                'expected_mean': round(mean, 3),
                'recommendation': self._get_recommendation(zone_id, value, mean, 'zscore'),
            }
        return None

    def _check_spike(self, zone_id: str, value: float) -> Optional[Dict]:
        """Rapid rate-of-change spike detection."""
        history = self.history[zone_id]
        if len(history) < 2:
            return None
        
        prev = history[-2]
        rate = abs(value - prev)
        
        if rate > self.spike_threshold:
            direction = 'surge' if value > prev else 'drop'
            severity = 'critical' if rate > 0.3 else 'high' if rate > 0.2 else 'medium'
            return {
                'type': 'density_spike',
                'zone_id': zone_id,
                'description': f'Rapid crowd {direction} in {zone_id}. Changed {rate:.1%} in one interval.',
                'rate_of_change': round(rate, 3),
                'direction': direction,
                'severity': severity,
                'severity_score': rate * 10,
                'current_value': round(value, 3),
                'previous_value': round(prev, 3),
                'recommendation': self._get_recommendation(zone_id, value, prev, direction),
            }
        return None

    def detect_multi_zone_correlation(self, densities: Dict[str, float]) -> List[Dict]:
        """Detect correlated anomalies across multiple zones.
        
        Looks for patterns like:
        - Simultaneous density increases (mass movement)
        - Gate surge + stand emptying (emergency exit pattern)
        """
        alerts = []
        
        gate_zones = ['gate-a', 'gate-b', 'gate-c', 'gate-d']
        stand_zones = ['north-stand', 'south-stand', 'east-stand', 'west-stand']
        
        gate_densities = [densities.get(z, 0) for z in gate_zones if z in densities]
        stand_densities = [densities.get(z, 0) for z in stand_zones if z in densities]
        
        # Pattern: All gates surging simultaneously (potential emergency)
        if gate_densities and np.mean(gate_densities) > 0.8:
            alerts.append({
                'type': 'multi_zone_correlation',
                'pattern': 'simultaneous_gate_surge',
                'description': 'All gates showing high density simultaneously. Possible emergency evacuation pattern.',
                'severity': 'critical',
                'affected_zones': gate_zones,
                'avg_density': round(np.mean(gate_densities), 3),
                'recommendation': 'Verify if evacuation is in progress. Contact security teams immediately.',
            })
        
        # Pattern: Stands emptying + food areas surging (halftime)
        if stand_densities and gate_densities:
            if np.mean(stand_densities) < 0.3 and np.mean(gate_densities) < 0.3:
                food_zones = ['food-n', 'food-s']
                food_densities = [densities.get(z, 0) for z in food_zones if z in densities]
                if food_densities and np.mean(food_densities) > 0.7:
                    alerts.append({
                        'type': 'multi_zone_correlation',
                        'pattern': 'halftime_rush',
                        'description': 'Halftime pattern detected: stands emptying, concessions surging.',
                        'severity': 'medium',
                        'recommendation': 'Deploy additional concession staff. Open overflow food counters.',
                    })
        
        return alerts

    def _get_recommendation(self, zone_id: str, current: float, reference: float, anomaly_type: str) -> str:
        """Generate context-aware recommendation."""
        if anomaly_type == 'surge':
            if current > 0.85:
                return f'CRITICAL: Activate overflow protocols for {zone_id}. Deploy crowd management team immediately.'
            return f'Monitor {zone_id} closely. Consider pre-emptive staff deployment.'
        elif anomaly_type == 'drop':
            return f'Investigate sudden drop in {zone_id}. Check sensors for malfunction. Verify with cameras.'
        else:
            if current > reference:
                return f'Unexpected density increase in {zone_id}. Investigate cause and prepare contingency.'
            return f'Unusual low density in {zone_id}. Cross-reference with adjacent zone data.'

    def get_active_anomaly_count(self) -> int:
        """Return count of recent anomalies (last 5 minutes)."""
        now = datetime.now()
        recent = [a for a in self.anomaly_log 
                  if 'timestamp' in a and 
                  (now - datetime.fromisoformat(a['timestamp'])).seconds < 300]
        return len(recent)

    def get_risk_score(self) -> float:
        """Calculate overall stadium risk score (0-100)."""
        if not self.anomaly_log:
            return 5.0  # Base risk
        
        recent = self.anomaly_log[-20:]
        severity_map = {'critical': 25, 'high': 15, 'medium': 8, 'low': 3}
        total_risk = sum(severity_map.get(a.get('severity', 'low'), 3) for a in recent)
        return min(100, total_risk)


# Standalone test
if __name__ == '__main__':
    detector = AnomalyDetector()
    
    print("=" * 60)
    print("StadiumOS Antigravity — Anomaly Detection Engine")
    print("=" * 60)
    
    # Simulate normal data then inject anomaly
    print("\nSimulating normal zone data...")
    for i in range(20):
        density = 0.5 + np.random.normal(0, 0.03)
        result = detector.update('gate-a', density)
        if result:
            print(f"  🚨 Anomaly detected: {result['description']}")
    
    # Inject spike
    print("\nInjecting density spike (0.5 → 0.9)...")
    result = detector.update('gate-a', 0.9)
    if result:
        print(f"  🚨 {result['severity'].upper()}: {result['description']}")
        print(f"  💡 {result['recommendation']}")
    
    # Multi-zone test
    print("\nChecking multi-zone correlations...")
    densities = {
        'gate-a': 0.85, 'gate-b': 0.82, 'gate-c': 0.88, 'gate-d': 0.80,
        'north-stand': 0.4, 'south-stand': 0.3,
    }
    correlations = detector.detect_multi_zone_correlation(densities)
    for alert in correlations:
        print(f"  ⚠️  {alert['pattern']}: {alert['description']}")
    
    print(f"\nOverall Risk Score: {detector.get_risk_score():.1f}/100")
