import numpy as np
from .base_airfoil import BaseAirfoil

class FlapConfigurations:
    def __init__(self, chord=200, thickness=30):
        self.base_airfoil = BaseAirfoil(chord, thickness)
        self.chord = chord
        self.thickness = thickness
        
    def rotate_points(self, points, pivot, angle):
        """Rotate points around a pivot point"""
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        
        translated = points - pivot
        rotated = np.zeros_like(points)
        rotated[:, 0] = translated[:, 0] * cos_theta - translated[:, 1] * sin_theta
        rotated[:, 1] = translated[:, 0] * sin_theta + translated[:, 1] * cos_theta
        
        return rotated + pivot

    def plain_flap(self, center_x, center_y, flap_angle):
        """Generate plain flap configuration"""
        base_points = self.base_airfoil.get_profile_points(center_x, center_y)
        hinge_x = center_x + self.chord * 0.2
        hinge_point = np.array([hinge_x, center_y])
        flap_points = self.rotate_points(base_points[-20:], hinge_point, flap_angle)
        return np.vstack((base_points[:-20], flap_points))

    def split_flap(self, center_x, center_y, flap_angle):
        """Generate split flap configuration"""
        base_points = self.base_airfoil.get_profile_points(center_x, center_y)
        mid_point = len(base_points) // 2
        hinge_x = center_x + self.chord * 0.2
        hinge_point = np.array([hinge_x, center_y])
        
        lower_points = base_points[mid_point:]
        flap_points = self.rotate_points(lower_points[-15:], hinge_point, flap_angle)
        return np.vstack((base_points[:-15], flap_points))

    def slotted_flap(self, center_x, center_y, flap_angle):
        """Generate slotted flap configuration"""
        gap = self.thickness * 0.1
        flap_chord = self.chord * 0.3
        
        # Main airfoil
        base_points = self.base_airfoil.get_profile_points(center_x, center_y)
        
        # Flap
        flap = BaseAirfoil(flap_chord, self.thickness * 0.8)
        hinge_x = center_x + self.chord * 0.7
        hinge_y = center_y + gap
        flap_points = flap.get_profile_points(hinge_x, hinge_y)
        flap_points = self.rotate_points(flap_points, 
                                       np.array([hinge_x, hinge_y]), 
                                       flap_angle)
        
        return np.vstack((base_points[:-10], flap_points))

    # Add other flap configurations similarly... 