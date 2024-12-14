import numpy as np
from .base_airfoil import BaseAirfoil

class SplitFlap(BaseAirfoil):
    def __init__(self, chord=200, thickness=30):
        super().__init__(chord, thickness)
        self.hinge_position = 0.7  # 70% chord

    def get_flap_geometry(self, center_x, center_y, flap_angle):
        """Generate split flap geometry"""
        base_points = self.get_profile_points(center_x, center_y)
        mid_point = len(base_points) // 2
        hinge_x = center_x + self.chord * (self.hinge_position - 0.5)
        hinge_point = np.array([hinge_x, center_y])
        
        # Only rotate lower surface
        lower_points = base_points[mid_point:][-15:]
        rotated_flap = self.rotate_points(lower_points, hinge_point, flap_angle)
        
        return np.vstack((base_points[:-15], rotated_flap))