import numpy as np
from .base_airfoil import BaseAirfoil

class GougeFlap(BaseAirfoil):
    def __init__(self, chord=200, thickness=30):
        super().__init__(chord, thickness)
        self.flap_chord = chord * 0.35
        self.extension = chord * 0.2
        self.gap = thickness * 0.1

    def get_flap_geometry(self, center_x, center_y, flap_angle):
        """Generate Gouge flap geometry"""
        base_points = self.get_profile_points(center_x, center_y)
        
        # Create Gouge flap (similar to Fowler but with different deployment path)
        flap = BaseAirfoil(self.flap_chord, self.thickness * 0.85)
        
        # Special deployment characteristics
        deploy_x = center_x + self.chord * 0.15 + self.extension
        deploy_y = center_y + self.gap * (1 + np.sin(flap_angle))
        
        flap_points = flap.get_profile_points(deploy_x, deploy_y)
        rotated_flap = self.rotate_points(flap_points, 
                                        np.array([deploy_x, deploy_y]), 
                                        flap_angle * 1.1)
        
        return np.vstack((base_points[:-12], rotated_flap)) 