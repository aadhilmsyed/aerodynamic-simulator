import numpy as np
from .base_airfoil import BaseAirfoil

class PlainFlap(BaseAirfoil):
    def __init__(self, chord=200, thickness=30):
        super().__init__(chord, thickness)
        self.hinge_position = 0.7  # 70% chord

    def get_flap_geometry(self, center_x, center_y, flap_angle):
        """Generate plain flap geometry"""
        base_points = self.get_profile_points(center_x, center_y)
        hinge_x = center_x + self.chord * (self.hinge_position - 0.5)
        hinge_point = np.array([hinge_x, center_y])
        
        # Rotate the flap portion
        flap_points = base_points[-20:]
        rotated_flap = self.rotate_points(flap_points, hinge_point, flap_angle)
        
        return np.vstack((base_points[:-20], rotated_flap))

    def rotate_points(self, points, pivot, angle):
        """Rotate points around a pivot point"""
        translated = points - pivot
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        rotated = np.dot(translated, rotation_matrix.T)
        return rotated + pivot