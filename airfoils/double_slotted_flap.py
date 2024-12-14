import numpy as np
from .base_airfoil import BaseAirfoil

class DoubleSlottedFlap(BaseAirfoil):
    def __init__(self, chord=200, thickness=30):
        super().__init__(chord, thickness)
        self.gap1 = thickness * 0.1
        self.gap2 = thickness * 0.15
        self.flap1_chord = chord * 0.25
        self.flap2_chord = chord * 0.20

    def get_flap_geometry(self, center_x, center_y, flap_angle):
        """Generate double-slotted flap geometry"""
        base_points = self.get_profile_points(center_x, center_y)
        
        # First flap element
        flap1 = BaseAirfoil(self.flap1_chord, self.thickness * 0.8)
        hinge1_x = center_x + self.chord * 0.2
        hinge1_y = center_y + self.gap1
        flap1_points = flap1.get_profile_points(hinge1_x, hinge1_y)
        rotated_flap1 = self.rotate_points(flap1_points, 
                                         np.array([hinge1_x, hinge1_y]), 
                                         flap_angle * 0.7)  # First flap deflects less
        
        # Second flap element
        flap2 = BaseAirfoil(self.flap2_chord, self.thickness * 0.7)
        hinge2_x = center_x + self.chord * 0.4
        hinge2_y = center_y + self.gap2
        flap2_points = flap2.get_profile_points(hinge2_x, hinge2_y)
        rotated_flap2 = self.rotate_points(flap2_points, 
                                         np.array([hinge2_x, hinge2_y]), 
                                         flap_angle)
        
        return np.vstack((base_points[:-10], rotated_flap1, rotated_flap2)) 