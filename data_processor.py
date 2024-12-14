import numpy as np
import pandas as pd

class DataProcessor:
    def analyze_results(self, results_dict):
        """Analyze simulation results to find optimal configurations"""
        optimal_configs = {}
        
        for wing_shape, (lift, drag) in results_dict.items():
            # Calculate lift-to-drag ratio
            lift_drag_ratio = lift / drag
            
            # Find optimal angle of attack
            optimal_idx = np.argmax(lift_drag_ratio)
            optimal_configs[wing_shape] = {
                'optimal_angle': optimal_idx,
                'max_lift_drag_ratio': lift_drag_ratio[optimal_idx],
                'lift_coefficient': lift[optimal_idx],
                'drag_coefficient': drag[optimal_idx]
            }
            
        # Convert to pandas DataFrame for easy analysis
        df = pd.DataFrame.from_dict(optimal_configs, orient='index')
        return df 