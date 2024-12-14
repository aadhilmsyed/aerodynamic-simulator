import numpy as np
import matplotlib.pyplot as plt
import pygame
from wing_model import WingModel
from data_processor import DataProcessor
from visualization import AerodynamicVisualizer
from pathlib import Path
import csv
from airfoils import (
    PlainFlap, SplitFlap, SlottedFlap, FowlerFlap,
    DoubleSlottedFlap, TripleSlottedFlap, KruegerFlap,
    LeadingEdgeSlat, ZapFlap, GougeFlap
)

class AerodynamicSimulator:
    def __init__(self):
        self.wing_model = WingModel()
        self.data_processor = DataProcessor()
        self.visualizer = AerodynamicVisualizer()
        
        # Flap configurations
        self.flap_types = {
            'Plain Flap': PlainFlap(),
            'Split Flap': SplitFlap(),
            'Slotted Flap': SlottedFlap(),
            'Fowler Flap': FowlerFlap(),
            'Double-Slotted Flap': DoubleSlottedFlap(),
            'Triple-Slotted Flap': TripleSlottedFlap(),
            'Krueger Flap': KruegerFlap(),
            'Leading-Edge Slat': LeadingEdgeSlat(),
            'Zap Flap': ZapFlap(),
            'Gouge Flap': GougeFlap()
        }
        
        # Simulation parameters
        self.angles_of_attack = np.arange(-5, 20, 0.5)  # -5° to 20° in 0.5° steps
        
        # Create output directories
        self.output_dir = Path("output")
        self.plots_dir = self.output_dir / "plots"
        self.data_dir = self.output_dir / "data"
        
        for dir_path in [self.plots_dir, self.data_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def run_simulation(self, flap_type, reynolds_number=1e6):
        """Run aerodynamic simulation for given flap configuration"""
        lift_coefficients = []
        drag_coefficients = []
        
        for angle in self.angles_of_attack:
            lift, drag = self.wing_model.calculate_forces(
                angle, 
                flap_type,
                reynolds_number
            )
            lift_coefficients.append(lift)
            drag_coefficients.append(drag)
            
        return np.array(lift_coefficients), np.array(drag_coefficients)
    
    def save_results(self, results_dict):
        """Save simulation results to CSV files"""
        for flap_type, (lift, drag) in results_dict.items():
            data = {
                'angle': self.angles_of_attack,
                'lift': lift,
                'drag': drag,
                'lift_to_drag': lift/drag
            }
            
            # Save to CSV
            csv_path = self.data_dir / f"{flap_type.replace(' ', '_').lower()}_results.csv"
            with open(csv_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                writer.writeheader()
                writer.writerows(
                    {key: data[key][i] for key in data.keys()}
                    for i in range(len(self.angles_of_attack))
                )
    
    def plot_results(self, results_dict):
        """Plot and save lift-to-drag ratios for different flap configurations"""
        plt.figure(figsize=(12, 8))
        
        for flap_type, (lift, drag) in results_dict.items():
            lift_drag_ratio = lift / drag
            plt.plot(self.angles_of_attack, lift_drag_ratio, label=flap_type)
        
        plt.xlabel('Angle of Attack (degrees)')
        plt.ylabel('Lift-to-Drag Ratio')
        plt.title('Aerodynamic Efficiency vs Angle of Attack')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        
        # Save plot
        plt.savefig(self.plots_dir / 'lift_to_drag_comparison.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()

    def main(self):
        # Run simulations for different flap configurations
        results = {}
        for flap_type in self.flap_types:
            lift, drag = self.run_simulation(flap_type)
            results[flap_type] = (lift, drag)
        
        # Process and analyze data
        optimal_configs = self.data_processor.analyze_results(results)
        
        # Save results and plots
        self.save_results(results)
        self.plot_results(results)
        
        # Save optimal configurations
        optimal_configs.to_csv(self.data_dir / 'optimal_configurations.csv')
        
        # Launch interactive visualization
        self.visualizer.run_visualization(self.flap_types)

if __name__ == "__main__":
    simulator = AerodynamicSimulator()
    simulator.main() 