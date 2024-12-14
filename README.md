# Aerodynamic Flap Configuration Simulator (PHYS1A Honors Project)

**Author:** Aadhil Mubarak Syed

**Mentor:** Dr. William Pezzaglia

**Course:** PHYS 1A - General Physics I (Mechanics)

**Term:** Fall 2022

An interactive aerodynamic simulation tool that visualizes airflow patterns and thermal distributions around different aircraft flap configurations. This project demonstrates the physics of flight and how various flap designs affect aerodynamic performance. This project was developed as part of an honors project for my PHYS 1A course under the mentorship of Dr. William Pezzaglia focusing on aerodynamics and forces of flight. This program demonstrates how different flap configurations affect aircraft performance and demonstrates fundamental principles of fluid dynamics and aerodynamics.

## Features

- Interactive visualization of 10 different flap configurations:
  - Plain Flap
  - Split Flap
  - Slotted Flap
  - Fowler Flap
  - Double-Slotted Flap
  - Triple-Slotted Flap
  - Krueger Flap
  - Leading-Edge Slat
  - Zap Flap
  - Gouge Flap

- Real-time visualization features:
  - Dynamic airflow patterns
  - Temperature distribution (color-coded)
  - Pressure visualization
  - Adjustable airspeed (0-500 knots)
  - Interactive flap animation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aadhilmsyed/aerodynamic-simulator.git
cd aerodynamic-simulator
```

2. Create and activate a virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulator:
```bash
python aerodynamic_simulator.py
```

### Controls
- Click flap type buttons at the top to switch configurations
- Use +/- buttons to adjust airspeed (180 kts default, range: 0-500 kts)
- Close window to exit simulation
- Each flap selection resets the simulation to default settings

## Project Structure
```
Aerodynamics/
├── aerodynamic_simulator.py  # Main simulation controller
├── visualization.py         # Pygame visualization
├── wing_model.py           # Aerodynamic calculations
├── data_processor.py       # Data analysis
├── airfoils/              # Flap configurations
│   ├── __init__.py
│   ├── base_airfoil.py
│   ├── plain_flap.py
│   ├── split_flap.py
│   └── ... (other flap configurations)
├── output/                # Generated data and plots
│   ├── data/
│   └── plots/
└── requirements.txt
```

## Technical Details

### Physics Concepts
- Bernoulli's Principle for lift generation
- Lift and Drag force calculations
- Pressure distribution visualization
- Temperature effects on airflow
- Reynolds number considerations in flow patterns
- Boundary layer behavior
- Flow separation characteristics

### Implementation
- NACA 0012 Airfoil Profile base implementation
- Real-time particle-based flow visualization
- Color-coded thermal distribution modeling
- Dynamic pressure coefficient calculation
- Interactive flap deployment animation
- Continuous flow simulation at variable speeds

## Data Output

The simulator generates:
- Lift-to-drag ratio plots for each configuration
- Optimal configuration analysis
- Performance comparison data
- CSV files containing:
  - Lift coefficients
  - Drag coefficients
  - L/D ratios
  - Pressure distributions

## Requirements

- Python 3.8+
- Pygame >= 2.6.1
- NumPy >= 1.24.0
- Matplotlib >= 3.7.0
- Pandas >= 2.0.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for discussion.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Physics principles based on standard aerodynamic theory and fluid dynamics
- Airfoil profiles based on NACA specifications
- Visualization inspired by computational fluid dynamics (CFD) simulations
- Special thanks to the physics department for project guidance

## Future Enhancements

Planned future improvements include:
- Additional flap configurations
- 3D visualization capabilities
- Enhanced data analysis tools
- Real-time performance metrics
- Comparison with experimental data
- Integration with real aircraft performance data
```
