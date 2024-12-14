import numpy as np

class WingModel:
    def __init__(self):
        # Wing geometry parameters
        self.chord_length = 2.0  # meters
        self.wingspan = 10.0     # meters
        self.thickness_ratio = 0.12
        
        # Flap effectiveness factors
        self.flap_effectiveness = {
            'Plain Flap': 0.9,
            'Split Flap': 1.0,
            'Slotted Flap': 1.3,
            'Fowler Flap': 1.6,
            'Double-Slotted Flap': 1.8,
            'Triple-Slotted Flap': 2.0,
            'Krueger Flap': 1.2,
            'Leading-Edge Slat': 1.4,
            'Zap Flap': 1.5,
            'Gouge Flap': 1.4
        }
        
    def calculate_forces(self, angle_of_attack, flap_type, reynolds_number):
        """Calculate lift and drag coefficients for given conditions"""
        # Convert angle to radians
        alpha = np.radians(angle_of_attack)
        
        # Basic lift coefficient calculation
        cl = 2 * np.pi * alpha
        
        # Apply flap effectiveness factor
        effectiveness = self.flap_effectiveness.get(flap_type, 1.0)
        cl *= effectiveness
        
        # Calculate induced drag
        aspect_ratio = self.get_aspect_ratio()
        cd_induced = cl**2 / (np.pi * aspect_ratio * effectiveness)
        
        # Calculate parasitic drag
        cd_parasitic = self.calculate_parasitic_drag(reynolds_number)
        if flap_type in ['Slotted Flap', 'Double-Slotted Flap', 'Triple-Slotted Flap']:
            cd_parasitic *= 1.1  # Additional drag due to slots
        
        # Total drag coefficient
        cd = cd_parasitic + cd_induced
        
        return cl, cd
    
    def get_aspect_ratio(self):
        """Calculate wing aspect ratio"""
        return self.wingspan / self.chord_length
    
    def calculate_parasitic_drag(self, reynolds_number):
        """Calculate parasitic drag coefficient using flat-plate friction correlation"""
        cf = 0.074 / reynolds_number**0.2  # Turbulent flow correlation
        return cf * (1 + 2 * self.thickness_ratio)