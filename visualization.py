import pygame
import numpy as np
from pathlib import Path
import pygame.gfxdraw
import colorsys

class AerodynamicVisualizer:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Airfoil and Flap Configuration Visualization")
        
        # Colors
        self.BACKGROUND = (20, 20, 30)
        self.WING_COLOR = (200, 200, 200)
        self.TEXT_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (60, 60, 80)
        self.BUTTON_HOVER = (80, 80, 100)
        
        # Airflow parameters
        self.AIRSPEED = 180  # knots
        self.AIRSPEED_PIXELS = 5  # pixels per frame
        self.TEMPERATURE_RANGE = (15, 35)  # Celsius
        
        # UI elements
        self.button_height = 40
        self.button_width = 150
        
        # Simulation state
        self.current_flap = None
        self.angle = 0
        self.flap_angle = 0
        self.time = 0
        
        # Initialize other attributes
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Airflow visualization
        self.particles = self.create_particles()
        
        # Speed control parameters
        self.speed_button_width = 30
        self.speed_button_height = 30
        self.speed_min = 0
        self.speed_max = 500
        self.speed_increment = 10
        
        # Create speed control buttons
        self.speed_buttons = {
            'decrease': pygame.Rect(
                180, self.height - 45,  # Position next to speed display
                self.speed_button_width, self.speed_button_height
            ),
            'increase': pygame.Rect(
                220, self.height - 45,
                self.speed_button_width, self.speed_button_height
            )
        }

    def create_particles(self):
        """Create particles for airflow visualization"""
        particles = []
        spacing = 40
        rows = self.height // spacing
        cols = (self.width // spacing) + 2  # Extra columns for continuous flow
        
        for i in range(rows):
            for j in range(cols):
                particles.append({
                    'pos': np.array([j * spacing - spacing, i * spacing + 100], dtype=float),
                    'velocity': np.array([self.AIRSPEED_PIXELS, 0], dtype=float),
                    'temperature': float(self.TEMPERATURE_RANGE[0]),
                    'pressure': 1.0
                })
        return particles

    def update_particles(self, wing_points):
        """Update particle positions and properties"""
        wing_center = np.mean(wing_points, axis=0)
        
        for particle in self.particles:
            # Update position based on velocity
            particle['pos'] += particle['velocity']
            
            # Reset particles that move off screen
            if particle['pos'][0] > self.width:
                particle['pos'][0] = -40
                particle['temperature'] = self.TEMPERATURE_RANGE[0]
                particle['pressure'] = 1.0
                particle['velocity'] = np.array([self.AIRSPEED_PIXELS, 0], dtype=float)
            
            # Calculate interaction with wing
            dx = particle['pos'][0] - wing_center[0]
            dy = particle['pos'][1] - wing_center[1]
            distance = np.sqrt(dx**2 + dy**2)
            
            if distance < 150:  # Influence radius
                # Calculate deflection
                deflection = self.calculate_deflection(particle['pos'], wing_points)
                angle_rad = np.radians(deflection)
                
                # Update velocity
                particle['velocity'] = np.array([
                    self.AIRSPEED_PIXELS * np.cos(angle_rad),
                    self.AIRSPEED_PIXELS * np.sin(angle_rad)
                ], dtype=float)
                
                # Update temperature and pressure
                rel_pos = particle['pos'][1] - wing_center[1]
                if rel_pos < 0:  # Upper surface (lower pressure, lower temperature)
                    particle['temperature'] = self.TEMPERATURE_RANGE[0] - 5
                    particle['pressure'] = 0.8
                else:  # Lower surface (higher pressure, higher temperature)
                    particle['temperature'] = self.TEMPERATURE_RANGE[1]
                    particle['pressure'] = 1.2

    def get_particle_color(self, temperature, pressure):
        """Get color based on temperature and pressure"""
        # Ensure temperature is within range
        temp = max(min(temperature, self.TEMPERATURE_RANGE[1]), self.TEMPERATURE_RANGE[0])
        
        # Normalize temperature to 0-1 range
        t_norm = (temp - self.TEMPERATURE_RANGE[0]) / (self.TEMPERATURE_RANGE[1] - self.TEMPERATURE_RANGE[0])
        
        # Use HSV color space: blue (cold) to red (hot)
        hue = (1 - t_norm) * 0.7  # 0.7 = blue, 0 = red
        saturation = 1.0
        value = min(max(0.8 + 0.2 * pressure, 0), 1)  # Ensure value is between 0 and 1
        
        # Convert HSV to RGB
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        return tuple(int(max(min(x * 255, 255), 0)) for x in rgb)

    def draw_airflow(self, wing_points):
        """Draw airflow patterns with thermal indicators"""
        self.update_particles(wing_points)
        
        for particle in self.particles:
            # Calculate end point based on velocity
            end_point = particle['pos'] + particle['velocity'] * 4
            
            # Get color based on temperature and pressure
            color = self.get_particle_color(particle['temperature'], particle['pressure'])
            
            # Convert numpy arrays to tuples for pygame
            start_pos = tuple(int(x) for x in particle['pos'])
            end_pos = tuple(int(x) for x in end_point)
            
            # Draw arrow
            self.draw_arrow(self.screen, start_pos, end_pos, color)

    def create_buttons(self, flap_types):
        """Create buttons for flap type selection"""
        buttons = {}
        x_start = 10
        y_start = 10
        spacing = 5
        
        for i, flap_type in enumerate(flap_types):
            x = x_start + (i % 5) * (self.button_width + spacing)
            y = y_start + (i // 5) * (self.button_height + spacing)
            buttons[flap_type] = pygame.Rect(x, y, self.button_width, self.button_height)
            
        return buttons

    def draw_arrow(self, surface, start, end, color, width=2):
        """Draw an arrow to show airflow direction"""
        # Ensure start and end are tuples of integers
        start = tuple(int(x) for x in start)
        end = tuple(int(x) for x in end)
        
        pygame.draw.line(surface, color, start, end, width)
        angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        arrow_size = 10
        
        arrow_points = [
            (int(end[0] - arrow_size * np.cos(angle - np.pi/6)),
             int(end[1] - arrow_size * np.sin(angle - np.pi/6))),
            end,
            (int(end[0] - arrow_size * np.cos(angle + np.pi/6)),
             int(end[1] - arrow_size * np.sin(angle + np.pi/6)))
        ]
        pygame.draw.polygon(surface, color, arrow_points)

    def calculate_deflection(self, point, wing_points):
        """Calculate airflow deflection based on wing geometry"""
        wing_center = np.mean(wing_points, axis=0)
        relative_pos = point[1] - wing_center[1]
        return 20 * np.sin(self.flap_angle) * np.exp(-abs(relative_pos)/100)

    def update_airspeed(self, increase=True):
        """Update airspeed based on button press"""
        if increase:
            self.AIRSPEED = min(self.AIRSPEED + self.speed_increment, self.speed_max)
        else:
            self.AIRSPEED = max(self.AIRSPEED - self.speed_increment, self.speed_min)
        
        # Update pixel speed (scale appropriately)
        self.AIRSPEED_PIXELS = self.AIRSPEED / 36  # Scale factor for visualization

    def draw_speed_controls(self):
        """Draw speed control buttons and display"""
        # Draw speed display
        font = pygame.font.Font(None, 36)
        speed_text = font.render(f"Airspeed: {self.AIRSPEED} kts", True, self.TEXT_COLOR)
        self.screen.blit(speed_text, (10, self.height - 40))
        
        # Draw decrease button (-)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.speed_buttons['decrease'], border_radius=5)
        pygame.draw.line(
            self.screen, self.TEXT_COLOR,
            (self.speed_buttons['decrease'].left + 8, self.speed_buttons['decrease'].centery),
            (self.speed_buttons['decrease'].right - 8, self.speed_buttons['decrease'].centery),
            3
        )
        
        # Draw increase button (+)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.speed_buttons['increase'], border_radius=5)
        # Horizontal line
        pygame.draw.line(
            self.screen, self.TEXT_COLOR,
            (self.speed_buttons['increase'].left + 8, self.speed_buttons['increase'].centery),
            (self.speed_buttons['increase'].right - 8, self.speed_buttons['increase'].centery),
            3
        )
        # Vertical line
        pygame.draw.line(
            self.screen, self.TEXT_COLOR,
            (self.speed_buttons['increase'].centerx, self.speed_buttons['increase'].top + 8),
            (self.speed_buttons['increase'].centerx, self.speed_buttons['increase'].bottom - 8),
            3
        )

    def run_visualization(self, flap_types):
        """Run the interactive visualization"""
        self.buttons = self.create_buttons(flap_types)
        self.current_flap = list(flap_types.values())[0]
        
        while self.running:
            self.handle_events(flap_types)
            self.screen.fill(self.BACKGROUND)
            
            # Draw UI elements
            self.draw_buttons()
            self.draw_speed_controls()  # Add speed controls
            
            # Update flap angle
            self.flap_angle = np.radians(20 * np.sin(np.radians(self.angle)))
            
            # Get and draw wing geometry
            wing_points = self.current_flap.get_flap_geometry(
                self.width//2, self.height//2, self.flap_angle
            )
            pygame.draw.polygon(self.screen, self.WING_COLOR, wing_points)
            
            # Draw airflow with thermal indicators
            self.draw_airflow(wing_points)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
            
            # Update animation
            self.angle = (self.angle + 1) % 360
            self.time += 1/60
            
        pygame.quit()

    def handle_events(self, flap_types):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_button_click(event.pos, flap_types)

    def reset_simulation(self):
        """Reset simulation parameters to default values"""
        self.AIRSPEED = 180  # Reset to default speed
        self.AIRSPEED_PIXELS = self.AIRSPEED / 36
        self.angle = 0
        self.flap_angle = 0
        self.time = 0
        self.particles = self.create_particles()  # Reset particle positions

    def handle_button_click(self, pos, flap_types):
        """Handle button clicks for flap type selection and speed control"""
        # Check flap type buttons
        for flap_type, button in self.buttons.items():
            if button.collidepoint(pos):
                self.current_flap = flap_types[flap_type]
                self.reset_simulation()  # Reset when new flap type is selected
                return
        
        # Check speed control buttons
        if self.speed_buttons['decrease'].collidepoint(pos):
            self.update_airspeed(increase=False)
        elif self.speed_buttons['increase'].collidepoint(pos):
            self.update_airspeed(increase=True)

    def draw_buttons(self):
        """Draw the flap type selection buttons"""
        mouse_pos = pygame.mouse.get_pos()
        
        for flap_type, button in self.buttons.items():
            color = self.BUTTON_HOVER if button.collidepoint(mouse_pos) else self.BUTTON_COLOR
            pygame.draw.rect(self.screen, color, button, border_radius=5)
            
            font = pygame.font.Font(None, 24)
            text = font.render(flap_type, True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=button.center)
            self.screen.blit(text, text_rect) 