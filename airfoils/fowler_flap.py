import numpy as np
from .base_airfoil import BaseAirfoil

class FowlerFlap(BaseAirfoil):
    def __init__(self, chord=200, thickness=30):
        super().__init__(chord, thickness)
        self.extension = chord * 0.2
        self.gap = thickness * 0.15

    def get_flap_geometry(self, center_x, center_y, flap_angle):
        """Generate Fowler flap geometry"""
        base_points = self.get_profile_points(center_x, center_y)
        
        # Create translated and scaled flap
        flap = BaseAirfoil(self.chord * 0.3, self.thickness * 0.8)
        hinge_x = center_x + self.chord * 0.2 + self.extension
        hinge_y = center_y + self.gap
        flap_points = flap.get_profile_points(hinge_x, hinge_y)
        rotated_flap = self.rotate_points(flap_points, 
                                        np.array([hinge_x, hinge_y]), 
                                        flap_angle)
        
        return np.vstack((base_points, rotated_flap))