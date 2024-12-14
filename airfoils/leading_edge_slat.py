import numpy as np
from .base_airfoil import BaseAirfoil

class LeadingEdgeSlat(BaseAirfoil):
    def __init__(self, chord=200, thickness=30):
        super().__init__(chord, thickness)
        self.slat_chord = chord * 0.15
        self.slat_gap = thickness * 0.08
        self.slat_overlap = chord * 0.01

    def get_flap_geometry(self, center_x, center_y, flap_angle):
        """Generate leading-edge slat geometry"""
        base_points = self.get_profile_points(center_x, center_y)
        
        # Create slat element
        slat = BaseAirfoil(self.slat_chord, self.thickness * 0.6)
        # Position forward and slightly below leading edge
        slat_x = center_x - self.chord * 0.5 - self.slat_overlap
        slat_y = center_y - self.slat_gap
        
        slat_points = slat.get_profile_points(slat_x, slat_y)
        rotated_slat = self.rotate_points(slat_points, 
                                        np.array([slat_x + self.slat_chord/2, slat_y]), 
                                        -flap_angle * 0.3)  # Smaller angle for slat
        
        return np.vstack((rotated_slat, base_points)) 