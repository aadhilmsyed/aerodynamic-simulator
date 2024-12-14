import numpy as np
from .base_airfoil import BaseAirfoil

class ZapFlap(BaseAirfoil):
    def __init__(self, chord=200, thickness=30):
        super().__init__(chord, thickness)
        self.flap_chord = chord * 0.3
        self.extension = chord * 0.25
        self.gap = thickness * 0.12

    def get_flap_geometry(self, center_x, center_y, flap_angle):
        """Generate Zap flap geometry"""
        base_points = self.get_profile_points(center_x, center_y)
        
        # Create Zap flap with special deployment characteristics
        flap = BaseAirfoil(self.flap_chord, self.thickness * 0.8)
        
        # Calculate deployment position (extends back and down)
        deploy_x = center_x + self.chord * 0.2 + self.extension * np.cos(flap_angle)
        deploy_y = center_y + self.gap + self.extension * np.sin(flap_angle)
        
        flap_points = flap.get_profile_points(deploy_x, deploy_y)
        rotated_flap = self.rotate_points(flap_points, 
                                        np.array([deploy_x, deploy_y]), 
                                        flap_angle * 1.2)  # Increased deflection
        
        return np.vstack((base_points[:-15], rotated_flap)) 