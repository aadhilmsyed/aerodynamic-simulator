import numpy as np
from .base_airfoil import BaseAirfoil

class SlottedFlap(BaseAirfoil):
    def __init__(self, chord=200, thickness=30):
        super().__init__(chord, thickness)
        self.slot_gap = thickness * 0.1
        self.flap_chord = chord * 0.3

    def get_flap_geometry(self, center_x, center_y, flap_angle):
        """Generate slotted flap geometry"""
        # Main airfoil
        base_points = self.get_profile_points(center_x, center_y)
        
        # Flap element
        flap = BaseAirfoil(self.flap_chord, self.thickness * 0.8)
        hinge_x = center_x + self.chord * 0.2
        hinge_y = center_y + self.slot_gap
        flap_points = flap.get_profile_points(hinge_x, hinge_y)
        rotated_flap = self.rotate_points(flap_points, 
                                        np.array([hinge_x, hinge_y]), 
                                        flap_angle)
        
        return np.vstack((base_points[:-10], rotated_flap))