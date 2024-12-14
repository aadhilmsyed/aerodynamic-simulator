import numpy as np
from .base_airfoil import BaseAirfoil

class TripleSlottedFlap(BaseAirfoil):
    def __init__(self, chord=200, thickness=30):
        super().__init__(chord, thickness)
        self.gaps = [thickness * 0.1, thickness * 0.12, thickness * 0.15]
        self.flap_chords = [chord * 0.25, chord * 0.20, chord * 0.15]

    def get_flap_geometry(self, center_x, center_y, flap_angle):
        """Generate triple-slotted flap geometry"""
        base_points = self.get_profile_points(center_x, center_y)
        flap_points = []
        
        # Generate three flap elements
        for i in range(3):
            flap = BaseAirfoil(self.flap_chords[i], self.thickness * (0.8 - i * 0.1))
            hinge_x = center_x + self.chord * (0.2 + i * 0.2)
            hinge_y = center_y + self.gaps[i]
            points = flap.get_profile_points(hinge_x, hinge_y)
            # Each subsequent flap deflects more
            deflection = flap_angle * (0.6 + i * 0.2)
            rotated = self.rotate_points(points, 
                                       np.array([hinge_x, hinge_y]), 
                                       deflection)
            flap_points.append(rotated)
        
        return np.vstack([base_points[:-10]] + flap_points) 