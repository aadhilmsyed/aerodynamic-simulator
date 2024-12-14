import numpy as np
from .base_airfoil import BaseAirfoil

class KruegerFlap(BaseAirfoil):
    def __init__(self, chord=200, thickness=30):
        super().__init__(chord, thickness)
        self.flap_chord = chord * 0.15
        self.deployment_radius = chord * 0.1

    def get_flap_geometry(self, center_x, center_y, flap_angle):
        """Generate Krueger flap geometry"""
        base_points = self.get_profile_points(center_x, center_y)
        
        # Create Krueger flap (deploys from lower leading edge)
        flap = BaseAirfoil(self.flap_chord, self.thickness * 0.6)
        # Position at leading edge, lower surface
        hinge_x = center_x - self.chord * 0.45
        hinge_y = center_y + self.thickness * 0.3
        
        # Generate deployment path
        theta = flap_angle * 1.5  # Larger rotation for Krueger
        deploy_x = hinge_x - self.deployment_radius * np.sin(theta)
        deploy_y = hinge_y - self.deployment_radius * (1 - np.cos(theta))
        
        flap_points = flap.get_profile_points(deploy_x, deploy_y)
        rotated_flap = self.rotate_points(flap_points, 
                                        np.array([hinge_x, hinge_y]), 
                                        -theta)  # Negative angle for upward deployment
        
        return np.vstack((rotated_flap, base_points)) 