"""
StadiumOS Antigravity — Queue Optimization Engine
===================================================
Intelligent queue management with dynamic resource
allocation and wait-time prediction.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import math


class QueueOptimizer:
    """AI-driven queue optimization engine.
    
    Features:
    - M/M/c queueing model for wait-time estimation
    - Dynamic counter allocation based on demand
    - Priority queue management
    - Overflow detection and rerouting
    """

    def __init__(self):
        self.queues: Dict[str, Dict] = {}
        self._init_queues()

    def _init_queues(self):
        """Initialize queue configurations."""
        configs = [
            {'id': 'food-n', 'name': 'Food Court North', 'type': 'food',
             'counters_total': 8, 'counters_open': 6, 'service_rate': 2.5,
             'people': 45, 'max_queue': 80},
            {'id': 'food-s', 'name': 'Food Court South', 'type': 'food',
             'counters_total': 8, 'counters_open': 5, 'service_rate': 2.5,
             'people': 62, 'max_queue': 80},
            {'id': 'merch', 'name': 'Merchandise Store', 'type': 'retail',
             'counters_total': 4, 'counters_open': 3, 'service_rate': 3.0,
             'people': 28, 'max_queue': 50},
            {'id': 'restroom-ne', 'name': 'Restroom NE', 'type': 'facility',
             'counters_total': 12, 'counters_open': 10, 'service_rate': 4.0,
             'people': 15, 'max_queue': 30},
            {'id': 'restroom-sw', 'name': 'Restroom SW', 'type': 'facility',
             'counters_total': 12, 'counters_open': 8, 'service_rate': 4.0,
             'people': 22, 'max_queue': 30},
            {'id': 'vip-entry', 'name': 'VIP Entry', 'type': 'entry',
             'counters_total': 4, 'counters_open': 4, 'service_rate': 5.0,
             'people': 8, 'max_queue': 40},
        ]
        for cfg in configs:
            self.queues[cfg['id']] = cfg

    def estimate_wait_time(self, queue_id: str) -> Dict:
        """Estimate wait time using M/M/c queueing theory.
        
        M/M/c model assumptions:
        - Poisson arrival process
        - Exponential service times
        - c identical servers (counters)
        
        Returns:
            Dict with wait time estimates and utilization metrics
        """
        q = self.queues.get(queue_id)
        if not q:
            return {'error': f'Queue {queue_id} not found'}

        n = q['people']         # People in queue
        c = q['counters_open']  # Open counters
        mu = q['service_rate']  # Service rate per counter (people/min)
        
        if c <= 0:
            return {'queue_id': queue_id, 'wait_min': 999, 'status': 'closed'}

        # Utilization (rho)
        lambda_arrival = n * 0.3  # Estimated arrival rate
        rho = lambda_arrival / (c * mu) if c * mu > 0 else 1

        # Approximate wait time
        if rho >= 1:
            # Overloaded — estimate based on queue length
            wait = n / (c * mu) if c * mu > 0 else 30
        else:
            # M/M/c formula approximation
            wait = (n / (c * mu)) * (1 / (1 - min(rho, 0.99)))

        wait = max(0.5, min(wait, 60))  # Clamp to 0.5-60 minutes

        # Status determination
        ratio = n / q['max_queue']
        if ratio < 0.4:
            status = 'normal'
        elif ratio < 0.65:
            status = 'moderate'
        elif ratio < 0.85:
            status = 'busy'
        else:
            status = 'critical'

        return {
            'queue_id': queue_id,
            'name': q['name'],
            'people': n,
            'max_capacity': q['max_queue'],
            'counters_open': c,
            'counters_total': q['counters_total'],
            'utilization': round(min(rho, 1.0), 3),
            'wait_min': round(wait, 1),
            'status': status,
            'fill_ratio': round(ratio, 3),
        }

    def optimize_counters(self, queue_id: str) -> Dict:
        """Calculate optimal number of counters based on demand.
        
        Returns recommendation to open/close counters.
        """
        q = self.queues.get(queue_id)
        if not q:
            return {'error': 'Queue not found'}

        n = q['people']
        current_open = q['counters_open']
        total = q['counters_total']
        mu = q['service_rate']
        max_q = q['max_queue']
        ratio = n / max_q

        # Target: keep wait under 5 minutes
        target_wait = 5.0
        required_counters = max(1, math.ceil(n / (mu * target_wait * 0.8)))
        optimal = min(required_counters, total)

        action = 'none'
        reason = ''
        if optimal > current_open:
            action = 'open_more'
            reason = f'Open {optimal - current_open} more counter(s) to reduce wait time below {target_wait} min.'
        elif optimal < current_open and ratio < 0.3:
            action = 'close_some'
            reason = f'Queue is light. Can close {current_open - optimal} counter(s) to optimize staffing.'
        else:
            reason = 'Counter allocation is optimal for current demand.'

        return {
            'queue_id': queue_id,
            'name': q['name'],
            'current_counters': current_open,
            'recommended_counters': optimal,
            'total_available': total,
            'action': action,
            'reason': reason,
            'estimated_wait_after': round(n / (optimal * mu), 1) if optimal * mu > 0 else 0,
            'current_wait': round(n / (current_open * mu), 1) if current_open * mu > 0 else 30,
        }

    def get_reroute_suggestions(self) -> List[Dict]:
        """Suggest queue rerouting for overloaded queues."""
        suggestions = []
        estimates = {qid: self.estimate_wait_time(qid) for qid in self.queues}
        
        for qid, est in estimates.items():
            if est.get('status') in ('busy', 'critical'):
                # Find similar queues with lower load
                q = self.queues[qid]
                alternatives = [
                    (aid, aest) for aid, aest in estimates.items()
                    if aid != qid 
                    and self.queues[aid]['type'] == q['type']
                    and aest.get('fill_ratio', 1) < 0.5
                ]
                if alternatives:
                    best = min(alternatives, key=lambda x: x[1].get('wait_min', 999))
                    suggestions.append({
                        'overloaded': qid,
                        'overloaded_name': q['name'],
                        'overloaded_wait': est.get('wait_min', 0),
                        'alternative': best[0],
                        'alternative_name': self.queues[best[0]]['name'],
                        'alternative_wait': best[1].get('wait_min', 0),
                        'time_saved': round(est.get('wait_min', 0) - best[1].get('wait_min', 0), 1),
                    })
        
        return suggestions

    def simulate_step(self):
        """Advance queue simulation by one step."""
        for qid, q in self.queues.items():
            # Random arrivals and departures
            arrivals = np.random.poisson(3)
            departures = min(q['people'], np.random.poisson(q['counters_open'] * q['service_rate'] * 0.3))
            
            q['people'] = max(0, min(q['max_queue'], q['people'] + arrivals - departures))
            
            # Auto-scale counters based on demand
            ratio = q['people'] / q['max_queue']
            if ratio > 0.75 and q['counters_open'] < q['counters_total']:
                q['counters_open'] = min(q['counters_total'], q['counters_open'] + 1)
            elif ratio < 0.2 and q['counters_open'] > 1:
                q['counters_open'] = max(1, q['counters_open'] - 1)

    def get_all_status(self) -> List[Dict]:
        """Get status of all queues."""
        return [self.estimate_wait_time(qid) for qid in self.queues]


# Standalone test
if __name__ == '__main__':
    optimizer = QueueOptimizer()
    
    print("=" * 60)
    print("StadiumOS Antigravity — Queue Optimization Engine")
    print("=" * 60)
    
    # Show all queue statuses
    print(f"\n{'Queue':<25} {'People':>7} {'Wait':>6} {'Counters':>10} {'Status':>10}")
    print("-" * 60)
    for status in optimizer.get_all_status():
        print(f"{status['name']:<25} {status['people']:>5}/{status['max_capacity']:<3} "
              f"{status['wait_min']:>5.1f}m {status['counters_open']}/{status['counters_total']:>3}    "
              f"{status['status']:>10}")
    
    # Counter optimization
    print("\n📊 Counter Optimization Recommendations:")
    for qid in optimizer.queues:
        rec = optimizer.optimize_counters(qid)
        if rec['action'] != 'none':
            print(f"  {'🟢' if rec['action'] == 'close_some' else '🔴'} {rec['name']}: {rec['reason']}")
    
    # Reroute suggestions
    suggestions = optimizer.get_reroute_suggestions()
    if suggestions:
        print("\n🔄 Rerouting Suggestions:")
        for s in suggestions:
            print(f"  ➡️  {s['overloaded_name']} ({s['overloaded_wait']}m) → {s['alternative_name']} ({s['alternative_wait']}m) | Save {s['time_saved']}m")
