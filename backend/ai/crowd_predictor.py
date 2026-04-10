"""
StadiumOS Antigravity — Crowd Flow Prediction AI Module
========================================================
Uses Monte Carlo simulation + time-series smoothing for
crowd density prediction across stadium zones.
"""

import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import math


class CrowdPredictor:
    """AI-powered crowd flow prediction engine.
    
    Uses a combination of:
    - Monte Carlo simulation for stochastic flow modeling
    - Exponential smoothing for time-series forecasting
    - Event-phase awareness (pre-game, game, halftime, post-game)
    """

    def __init__(self, total_capacity: int = 52000):
        self.total_capacity = total_capacity
        self.zone_capacities = {
            'gate-a': 5000, 'gate-b': 5000, 'gate-c': 5000, 'gate-d': 5000,
            'north-stand': 12000, 'south-stand': 12000,
            'east-stand': 10000, 'west-stand': 10000,
            'food-n': 800, 'food-s': 800,
            'vip-lounge': 500, 'merch': 500,
            'restroom-ne': 300, 'restroom-sw': 300,
            'medical': 50,
        }
        self.current_occupancy: Dict[str, int] = {}
        self.history: List[Dict] = []
        self.alpha = 0.3  # Exponential smoothing factor
        self._init_occupancy()

    def _init_occupancy(self):
        """Initialize with realistic pre-game occupancy."""
        base_ratios = {
            'gate-a': 0.70, 'gate-b': 0.50, 'gate-c': 0.60, 'gate-d': 0.40,
            'north-stand': 0.65, 'south-stand': 0.55,
            'east-stand': 0.50, 'west-stand': 0.45,
            'food-n': 0.80, 'food-s': 0.75,
            'vip-lounge': 0.30, 'merch': 0.60,
            'restroom-ne': 0.50, 'restroom-sw': 0.55,
            'medical': 0.10,
        }
        for zone, ratio in base_ratios.items():
            cap = self.zone_capacities[zone]
            noise = np.random.normal(0, 0.05)
            self.current_occupancy[zone] = int(cap * max(0, min(1, ratio + noise)))

    def get_event_phase(self, minutes_since_start: int = 60) -> str:
        """Determine current event phase."""
        if minutes_since_start < 0:
            return 'pre-game'
        elif minutes_since_start < 45:
            return 'first-half'
        elif minutes_since_start < 60:
            return 'halftime'
        elif minutes_since_start < 105:
            return 'second-half'
        else:
            return 'post-game'

    def get_phase_multipliers(self, phase: str) -> Dict[str, float]:
        """Zone-specific crowd density multipliers per event phase."""
        multipliers = {
            'pre-game': {
                'gate-a': 1.5, 'gate-b': 1.3, 'gate-c': 1.4, 'gate-d': 1.2,
                'food-n': 0.6, 'food-s': 0.6, 'north-stand': 0.4, 'south-stand': 0.4,
                'east-stand': 0.3, 'west-stand': 0.3, 'merch': 1.2,
                'restroom-ne': 0.5, 'restroom-sw': 0.5,
            },
            'first-half': {
                'gate-a': 0.3, 'gate-b': 0.3, 'gate-c': 0.3, 'gate-d': 0.3,
                'food-n': 0.4, 'food-s': 0.4, 'north-stand': 1.3, 'south-stand': 1.3,
                'east-stand': 1.2, 'west-stand': 1.2, 'merch': 0.3,
                'restroom-ne': 0.6, 'restroom-sw': 0.6,
            },
            'halftime': {
                'gate-a': 0.2, 'gate-b': 0.2, 'gate-c': 0.2, 'gate-d': 0.2,
                'food-n': 1.8, 'food-s': 1.8, 'north-stand': 0.6, 'south-stand': 0.6,
                'east-stand': 0.5, 'west-stand': 0.5, 'merch': 1.5,
                'restroom-ne': 1.6, 'restroom-sw': 1.6,
            },
            'second-half': {
                'gate-a': 0.2, 'gate-b': 0.2, 'gate-c': 0.4, 'gate-d': 0.3,
                'food-n': 0.5, 'food-s': 0.5, 'north-stand': 1.2, 'south-stand': 1.2,
                'east-stand': 1.1, 'west-stand': 1.1, 'merch': 0.2,
                'restroom-ne': 0.7, 'restroom-sw': 0.7,
            },
            'post-game': {
                'gate-a': 1.8, 'gate-b': 1.6, 'gate-c': 1.9, 'gate-d': 1.5,
                'food-n': 0.2, 'food-s': 0.2, 'north-stand': 0.3, 'south-stand': 0.3,
                'east-stand': 0.3, 'west-stand': 0.3, 'merch': 0.1,
                'restroom-ne': 0.8, 'restroom-sw': 0.8,
            },
        }
        return multipliers.get(phase, multipliers['first-half'])

    def monte_carlo_predict(
        self, 
        zone_id: str, 
        minutes_ahead: int = 15, 
        simulations: int = 1000
    ) -> Dict:
        """Run Monte Carlo simulation for crowd density prediction.
        
        Args:
            zone_id: Target zone identifier
            minutes_ahead: Prediction horizon in minutes
            simulations: Number of Monte Carlo simulations
            
        Returns:
            Dict with predicted density, confidence interval, and risk level
        """
        if zone_id not in self.zone_capacities:
            return {'error': f'Unknown zone: {zone_id}'}

        capacity = self.zone_capacities[zone_id]
        current = self.current_occupancy.get(zone_id, 0)
        current_ratio = current / capacity

        # Run simulations
        results = []
        for _ in range(simulations):
            predicted = current_ratio
            for t in range(minutes_ahead):
                # Flow dynamics: combination of drift + noise
                drift = np.random.normal(0, 0.02)  # Base random walk
                mean_reversion = -0.01 * (predicted - 0.5)  # Mean reversion
                seasonal = 0.005 * math.sin(t * 0.1)  # Periodic pattern
                
                predicted += drift + mean_reversion + seasonal
                predicted = max(0, min(1.0, predicted))
            
            results.append(predicted)

        results = np.array(results)
        mean_pred = float(np.mean(results))
        std_pred = float(np.std(results))
        p05 = float(np.percentile(results, 5))
        p95 = float(np.percentile(results, 95))

        # Risk assessment
        if mean_pred > 0.85:
            risk = 'critical'
        elif mean_pred > 0.70:
            risk = 'high'
        elif mean_pred > 0.50:
            risk = 'moderate'
        else:
            risk = 'low'

        return {
            'zone_id': zone_id,
            'current_density': round(current_ratio * 100, 1),
            'predicted_density': round(mean_pred * 100, 1),
            'confidence_interval': {
                'lower': round(p05 * 100, 1),
                'upper': round(p95 * 100, 1),
            },
            'std_deviation': round(std_pred * 100, 1),
            'risk_level': risk,
            'minutes_ahead': minutes_ahead,
            'simulations': simulations,
            'predicted_people': int(mean_pred * capacity),
            'recommendation': self._generate_recommendation(zone_id, mean_pred, current_ratio),
        }

    def predict_all_zones(self, minutes_ahead: int = 15) -> List[Dict]:
        """Predict crowd density for all zones."""
        predictions = []
        for zone_id in self.zone_capacities:
            pred = self.monte_carlo_predict(zone_id, minutes_ahead, simulations=500)
            predictions.append(pred)
        
        # Sort by predicted density (highest risk first)
        predictions.sort(key=lambda x: x.get('predicted_density', 0), reverse=True)
        return predictions

    def exponential_smooth(self, zone_id: str, new_value: float) -> float:
        """Apply exponential smoothing to a new observation."""
        current = self.current_occupancy.get(zone_id, 0)
        capacity = self.zone_capacities.get(zone_id, 1)
        current_ratio = current / capacity
        smoothed = self.alpha * new_value + (1 - self.alpha) * current_ratio
        self.current_occupancy[zone_id] = int(smoothed * capacity)
        return smoothed

    def _generate_recommendation(self, zone_id: str, predicted: float, current: float) -> str:
        """Generate AI recommendation based on prediction."""
        if predicted > 0.85:
            return f"URGENT: {zone_id} predicted to reach critical density. Activate overflow protocols and redirect traffic immediately."
        elif predicted > 0.70 and predicted > current:
            return f"WARNING: {zone_id} density rising. Deploy additional staff and prepare alternate routes."
        elif predicted < current * 0.7:
            return f"INFO: {zone_id} density expected to decrease. Consider reallocating resources."
        else:
            return f"OK: {zone_id} density within normal parameters. Continue monitoring."

    def simulate_step(self, phase: str = 'first-half') -> Dict[str, int]:
        """Advance simulation by one time step."""
        multipliers = self.get_phase_multipliers(phase)
        
        for zone_id, capacity in self.zone_capacities.items():
            current = self.current_occupancy.get(zone_id, 0)
            mult = multipliers.get(zone_id, 1.0)
            
            # Target based on phase
            target = capacity * 0.5 * mult
            
            # Move towards target with noise
            delta = (target - current) * 0.1 + np.random.normal(0, capacity * 0.02)
            new_val = max(0, min(capacity, current + delta))
            self.current_occupancy[zone_id] = int(new_val)
        
        # Record history
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'phase': phase,
            'occupancy': dict(self.current_occupancy),
            'total': sum(self.current_occupancy.values()),
        }
        self.history.append(snapshot)
        if len(self.history) > 1000:
            self.history = self.history[-500:]
        
        return self.current_occupancy

    def get_congestion_hotspots(self, threshold: float = 0.7) -> List[Dict]:
        """Identify zones exceeding congestion threshold."""
        hotspots = []
        for zone_id, capacity in self.zone_capacities.items():
            current = self.current_occupancy.get(zone_id, 0)
            density = current / capacity
            if density > threshold:
                hotspots.append({
                    'zone_id': zone_id,
                    'density': round(density * 100, 1),
                    'people': current,
                    'capacity': capacity,
                    'severity': 'critical' if density > 0.9 else 'high',
                })
        return sorted(hotspots, key=lambda x: x['density'], reverse=True)


# Standalone test
if __name__ == '__main__':
    predictor = CrowdPredictor()
    
    print("=" * 60)
    print("StadiumOS Antigravity — Crowd Prediction Engine")
    print("=" * 60)
    
    # Predict for all zones
    predictions = predictor.predict_all_zones(minutes_ahead=15)
    
    print(f"\n{'Zone':<20} {'Current':>8} {'Predicted':>10} {'CI (95%)':>15} {'Risk':>10}")
    print("-" * 65)
    for p in predictions:
        ci = f"{p['confidence_interval']['lower']}-{p['confidence_interval']['upper']}%"
        print(f"{p['zone_id']:<20} {p['current_density']:>7.1f}% {p['predicted_density']:>9.1f}% {ci:>15} {p['risk_level']:>10}")
    
    # Hotspots
    hotspots = predictor.get_congestion_hotspots()
    if hotspots:
        print(f"\n⚠️  Congestion Hotspots ({len(hotspots)}):")
        for h in hotspots:
            print(f"  🔴 {h['zone_id']}: {h['density']}% ({h['people']}/{h['capacity']} people)")
    
    # Simulate a few steps
    print("\n📈 Simulating 5 time steps (halftime)...")
    for i in range(5):
        occupancy = predictor.simulate_step(phase='halftime')
        total = sum(occupancy.values())
        print(f"  Step {i+1}: Total occupancy = {total:,}")
