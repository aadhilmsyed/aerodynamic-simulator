import numpy as np

class BaseAirfoil:
    def __init__(self, chord=200, thickness=30):
        self.chord = chord
        self.thickness = thickness
        
    def naca0012(self, x):
        """Generate NACA 0012 airfoil coordinates"""
        y = self.thickness * (0.2969 * np.sqrt(x/self.chord) - 
                            0.1260 * (x/self.chord) - 
                            0.3516 * (x/self.chord)**2 + 
                            0.2843 * (x/self.chord)**3 - 
                            0.1015 * (x/self.chord)**4)
        return y

    def get_profile_points(self, center_x, center_y):
        """Get base airfoil profile points"""
        x_coords = np.linspace(0, self.chord, 50)
        y_coords = self.naca0012(x_coords)
        
        points = []
        # Upper surface
        for i in range(len(x_coords)):
            x = center_x - self.chord/2 + x_coords[i]
            points.append([x, center_y - y_coords[i]])
        
        # Lower surface (reverse order)
        for i in range(len(x_coords)-1, -1, -1):
            x = center_x - self.chord/2 + x_coords[i]
            points.append([x, center_y + y_coords[i]])
            
        return np.array(points)

    def rotate_points(self, points, pivot, angle):
        """Rotate points around a pivot point"""
        if not isinstance(points, np.ndarray):
            points = np.array(points)
        if not isinstance(pivot, np.ndarray):
            pivot = np.array(pivot)
            
        translated = points - pivot
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        
        rotated = np.dot(translated, rotation_matrix.T)
        return rotated + pivot