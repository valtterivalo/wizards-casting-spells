import pygame
import os
import math  # Add import for Python's math module

# Load wizard sprites
def load_wizard_sprites():
    """Load all wizard sprite images."""
    sprites = {}
    
    # Get the path to the images directory
    sprites_dir = os.path.join(os.path.dirname(__file__), 'assets', 'images')
    
    # Try to load wizard sprites if they exist
    try:
        for element in ['fire', 'water', 'earth']:
            # Regular sprite
            sprite_path = os.path.join(sprites_dir, f"{element}_wizard.png")
            if os.path.exists(sprite_path):
                sprites[element] = pygame.image.load(sprite_path).convert_alpha()
                
            # Casting sprite
            casting_path = os.path.join(sprites_dir, f"{element}_wizard_casting.png")
            if os.path.exists(casting_path):
                sprites[f"{element}_casting"] = pygame.image.load(casting_path).convert_alpha()
    except Exception as e:
        print(f"Error loading wizard sprites: {e}")
        
    return sprites

# Initialize sprites dictionary
wizard_sprites = {}

def init_rendering():
    """Initialize rendering resources."""
    global wizard_sprites
    wizard_sprites = load_wizard_sprites()

def draw_wizard(screen, position, color):
    """
    Draw a wizard on the screen at the specified position with the given color.
    
    Args:
        screen: Pygame surface to draw on
        position: Tuple (x, y) for the top-left corner of the wizard
        color: RGB tuple representing the wizard's color
    """
    # For now, wizards are just colored squares
    wizard_size = 50
    pygame.draw.rect(screen, color, (position[0], position[1], wizard_size, wizard_size))

def draw_player(screen, player):
    """
    Draw a player wizard on the screen based on their current state.
    
    Args:
        screen: Pygame surface to draw on
        player: Player object containing position and color information
    """
    # Standard wizard size - define at the top so it's available for the charge bar
    wizard_size = 50
    
    # Try to use sprites if available
    sprite_key = player.element.lower()
    if player.is_casting:
        sprite_key += "_casting"
    elif player.is_attuned:
        sprite_key += "_attuned"
    
    x, y = player.position
    
    if sprite_key in wizard_sprites:
        # If we have sprites, use them
        screen.blit(wizard_sprites[sprite_key], (x, y - 20))  # Adjust for hat height
    else:
        # Draw a more wizard-like shape instead of just a square
        color = player.get_display_color()
        
        # Draw wizard body (slightly rounded rectangle)
        body_rect = pygame.Rect(x, y, wizard_size, wizard_size)
        pygame.draw.rect(screen, color, body_rect, border_radius=5)
        
        # Draw wizard hat (triangle on top)
        hat_color = (min(color[0] + 20, 255), min(color[1] + 20, 255), min(color[2] + 20, 255))
        hat_points = [(x + wizard_size // 2, y - 20), (x + 10, y), (x + wizard_size - 10, y)]
        pygame.draw.polygon(screen, hat_color, hat_points)
        
        # Draw attunement effect
        if player.is_attuned:
            # Create a pulsing attunement aura around the wizard
            aura_radius = wizard_size * 0.8
            aura_pulse = 0.2 + (math.sin(pygame.time.get_ticks() / 200) + 1) * 0.15  # 0.2-0.5 range
            
            # Create a semi-transparent attunement aura
            aura_surface = pygame.Surface((aura_radius*2, aura_radius*2), pygame.SRCALPHA)
            base_color = player.color
            aura_color = (base_color[0], base_color[1], base_color[2], int(100 * aura_pulse))
            
            pygame.draw.circle(aura_surface, aura_color, 
                              (int(aura_radius), int(aura_radius)), 
                              int(aura_radius * aura_pulse))
            
            # Draw the aura
            aura_pos = (x + wizard_size//2 - aura_radius, y + wizard_size//2 - aura_radius)
            screen.blit(aura_surface, aura_pos, special_flags=pygame.BLEND_ALPHA_SDL2)
            
            # Draw attunement connections to other wizards
            for wizard_id in player.attuned_wizards:
                # Find the attuned wizard by ID
                for other_player in player.attuned_wizards:
                    if id(other_player) == wizard_id:
                        # Draw a connection line between wizards
                        player_center = (x + wizard_size//2, y + wizard_size//2)
                        other_center = (other_player.position[0] + wizard_size//2, 
                                       other_player.position[1] + wizard_size//2)
                        
                        # Calculate a cool pulsing gradient color
                        p_color = player.color
                        o_color = other_player.color
                        
                        # Draw a pulsing beam connecting the two wizards
                        pulse_factor = (math.sin(pygame.time.get_ticks() / 150) + 1) / 2  # 0-1 range
                        
                        # Draw multiple transparent lines for a beam effect
                        for i in range(3):
                            alpha = 150 - i*40  # Fade out for each line
                            width = 4 - i*1  # Thinner for each line
                            
                            # Interpolate colors based on pulse
                            color = (
                                int(p_color[0] * pulse_factor + o_color[0] * (1-pulse_factor)),
                                int(p_color[1] * pulse_factor + o_color[1] * (1-pulse_factor)),
                                int(p_color[2] * pulse_factor + o_color[2] * (1-pulse_factor)),
                                alpha
                            )
                            
                            # Draw the beam
                            pygame.draw.line(screen, color, player_center, other_center, width)
                        break
        
        # Draw staff (if casting)
        if player.is_casting:
            # Staff position
            staff_start = (x + wizard_size - 10, y + wizard_size - 10)
            staff_end = (x + wizard_size + 15, y + wizard_size - 25)
            
            # Draw staff (brown)
            pygame.draw.line(screen, (139, 69, 19), staff_start, staff_end, 3)
            
            # Draw glowing tip
            tip_color = player.color
            if player.casting_element and player.casting_element != player.element:
                # Use the color of the element being cast if it's not the primary element
                if player.casting_element == "Fire":
                    tip_color = (255, 60, 60)
                elif player.casting_element == "Water":
                    tip_color = (60, 60, 255)
                elif player.casting_element == "Earth":
                    tip_color = (60, 255, 60)
                elif player.casting_element == "Air":
                    tip_color = (200, 200, 255)
            
            pygame.draw.circle(screen, tip_color, staff_end, 5)
            
            # Draw glow around tip
            glow_radius = 8 + (player.cast_time % 5)
            glow_color = (tip_color[0], tip_color[1], tip_color[2], 150)  # Semi-transparent
            
            # Create a surface for the glow effect
            glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
            
            # Blit the glow to the screen
            screen.blit(glow_surface, (staff_end[0] - glow_radius, staff_end[1] - glow_radius), special_flags=pygame.BLEND_ALPHA_SDL2)

    # Draw charge bar above the wizard when casting
    if player.is_casting or player.charge_level > 0:
        # Bar dimensions
        bar_width = wizard_size
        bar_height = 8
        bar_x = x
        bar_y = y - 30  # Place it above the wizard and hat
        
        # Draw background (gray)
        pygame.draw.rect(screen, (70, 70, 70), (bar_x, bar_y, bar_width, bar_height))
        
        # Draw charge level (colored based on element and charge)
        fill_width = int(bar_width * (player.charge_level / 100))
        
        if player.is_overcharged:
            # Use pulsing red for overcharge
            pulse = abs(((player.cast_time % 20) - 10) / 10)
            charge_color = (255, 50 + int(pulse * 50), 50)
        else:
            # Use element color with brightness based on charge
            if player.casting_element and player.casting_element != player.element:
                # If casting a non-primary element, use its color
                if player.casting_element == "Fire":
                    base_color = (255, 60, 60)
                elif player.casting_element == "Water":
                    base_color = (60, 60, 255)
                elif player.casting_element == "Earth":
                    base_color = (60, 255, 60)
                elif player.casting_element == "Air":
                    base_color = (200, 200, 255)
                else:
                    base_color = player.color
            else:
                base_color = player.color
                
            charge_color = tuple(min(c + int(player.charge_level/2), 255) for c in base_color)
        
        pygame.draw.rect(screen, charge_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Draw border
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Draw 100% marker
        marker_x = bar_x + bar_width - 2
        pygame.draw.line(screen, (255, 255, 255), (marker_x, bar_y), (marker_x, bar_y + bar_height), 1)
                
        # Also display the element being cast for tertiary elements
        if player.casting_element and player.casting_element != player.element:
            element_font = pygame.font.SysFont(None, 18)
            element_text = element_font.render(player.casting_element, True, charge_color)
            screen.blit(element_text, (bar_x, bar_y - 15))

def draw_spell_circle(screen, spell_circle):
    """
    Draw the spell circle showing active elements and timer.
    
    Args:
        screen: Pygame surface to draw on
        spell_circle: SpellCircle object containing elements and timer info
    """
    # Spell circle dimensions and position
    center_x, center_y = screen.get_width() // 2, screen.get_height() - 100
    circle_radius = 60
    inner_radius = 40
    
    # Create a semi-transparent background for the spell circle
    bg_surface = pygame.Surface((circle_radius*2 + 20, circle_radius*2 + 20), pygame.SRCALPHA)
    pygame.draw.circle(bg_surface, (0, 0, 0, 100), (circle_radius + 10, circle_radius + 10), circle_radius + 10)
    screen.blit(bg_surface, (center_x - circle_radius - 10, center_y - circle_radius - 10))
    
    # Draw the base circle (darker when empty, lighter when elements present)
    base_color = (100, 100, 120) if spell_circle.elements else (60, 60, 80)
    pygame.draw.circle(screen, base_color, (center_x, center_y), circle_radius)
    
    # Draw the inner circle (where the elements will appear)
    inner_color = (70, 70, 90) if spell_circle.elements else (40, 40, 60)
    pygame.draw.circle(screen, inner_color, (center_x, center_y), inner_radius)
    
    # Draw timer ring if active
    if spell_circle.activation_timer > 0:
        # Draw a circular timer that shrinks as time decreases
        timer_percentage = spell_circle.activation_timer / 120  # 120 is max timer
        timer_width = 4  # Width of the timer ring
        timer_radius = circle_radius + 6
        
        # Draw the timer as an arc that decreases
        # Convert to angle (0 degrees is right, going counterclockwise)
        angle = 360 * timer_percentage
        
        # Create a surface for the timer arc
        arc_surface = pygame.Surface((timer_radius*2, timer_radius*2), pygame.SRCALPHA)
        
        # Draw a full circle as background in darker color
        pygame.draw.circle(arc_surface, (100, 100, 100, 100), (timer_radius, timer_radius), timer_radius, timer_width)
        
        # Calculate start and end angles (pygame angles are in radians, counterclockwise from right)
        start_angle = 0  # Start from right (0 degrees)
        end_angle = -angle * 3.14159 / 180  # Convert to radians, negative for counterclockwise
        
        # Draw the arc segment as the timer
        if angle > 0:  # Only draw if there's time left
            # For the arc we need a rectangle that bounds the circle
            rect = pygame.Rect(0, 0, timer_radius*2, timer_radius*2)
            
            # Bright color for the timer
            timer_color = (220, 220, 250)
            
            # Draw the timer arc
            pygame.draw.arc(arc_surface, timer_color, rect, start_angle, end_angle, timer_width)
        
        # Blit the arc to the screen
        screen.blit(arc_surface, (center_x - timer_radius, center_y - timer_radius))
    
    # Element colors and names
    element_colors = {
        "Fire": (255, 60, 60),    # Red
        "Water": (60, 60, 255),   # Blue
        "Earth": (60, 255, 60),   # Green
        "Air": (200, 200, 255)    # Light blue/white
    }
    
    element_symbols = {
        "Fire": "🔥",    # Fire emoji
        "Water": "💧",   # Water drop emoji
        "Earth": "🌱",   # Seedling emoji (for earth)
        "Air": "💨"      # Wind/air emoji
    }
    
    # If there are elements in the circle, draw them
    if spell_circle.elements:
        num_elements = len(spell_circle.elements)
        
        # Draw each element as a symbol with charge indicator
        for i, element in enumerate(spell_circle.elements):
            # Calculate angle for this element's position (evenly distributed around the circle)
            angle_degrees = i * (360 / num_elements)
            angle_rad = angle_degrees * 3.14159 / 180
            
            # Calculate position (positioned around the inner circle)
            # The angle starts at right (0°) and goes counterclockwise
            distance = inner_radius * 0.7  # Distance from center
            x_offset = distance * math.cos(angle_rad)  # Use math.cos instead of pygame.math.cos
            y_offset = -distance * math.sin(angle_rad)  # Use math.sin instead of pygame.math.sin
            
            # Get the charge level
            charge_level = 100  # Default
            if hasattr(spell_circle, 'element_charges') and i < len(spell_circle.element_charges):
                charge_level = spell_circle.element_charges[i]
            
            # Draw a colored circle for this element
            element_radius = 14  # Base size of element indicator
            element_pos = (int(center_x + x_offset), int(center_y + y_offset))
            
            # Circle background with element color
            element_bg_color = element_colors.get(element, (200, 200, 200))
            pygame.draw.circle(screen, element_bg_color, element_pos, element_radius)
            
            # Add a highlight/shadow effect
            highlight_color = tuple(min(c + 50, 255) for c in element_bg_color)
            shadow_color = tuple(max(c - 50, 0) for c in element_bg_color)
            
            # Highlight (top-left)
            pygame.draw.arc(screen, highlight_color, 
                           pygame.Rect(element_pos[0] - element_radius, element_pos[1] - element_radius, 
                                      element_radius*2, element_radius*2),
                           3.14159/2, 3.14159*3/2, 2)
            
            # Shadow (bottom-right)
            pygame.draw.arc(screen, shadow_color, 
                           pygame.Rect(element_pos[0] - element_radius, element_pos[1] - element_radius, 
                                      element_radius*2, element_radius*2),
                           3.14159*3/2, 3.14159/2, 2)
            
            # Try to render emoji symbol if font supports it, otherwise use text
            try:
                symbol = element_symbols.get(element, "?")
                symbol_font = pygame.font.SysFont("segoeuisymbol", 18)
                symbol_text = symbol_font.render(symbol, True, (255, 255, 255))
                symbol_rect = symbol_text.get_rect(center=element_pos)
                screen.blit(symbol_text, symbol_rect)
            except:
                # Fallback to first letter if emoji doesn't work
                fallback_font = pygame.font.SysFont(None, 22)
                letter_text = fallback_font.render(element[0], True, (255, 255, 255))
                letter_rect = letter_text.get_rect(center=element_pos)
                screen.blit(letter_text, letter_rect)
            
            # Draw a small charge indicator bar below the element
            bar_width = element_radius * 2
            bar_height = 4
            bar_x = element_pos[0] - element_radius
            bar_y = element_pos[1] + element_radius + 2
            
            # Background bar (dark)
            pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
            
            # Filled bar based on charge
            fill_width = int(bar_width * (charge_level / 100))
            
            # Color based on charge level
            if charge_level < 40:
                charge_color = (200, 60, 60)  # Red for low charge
            elif charge_level < 70:
                charge_color = (200, 200, 60)  # Yellow for medium charge
            else:
                charge_color = (60, 200, 60)  # Green for high charge
                
            pygame.draw.rect(screen, charge_color, (bar_x, bar_y, fill_width, bar_height))
    
    # Draw the current spell name if active
    if spell_circle.active_spell:
        font = pygame.font.SysFont(None, 22)
        spell_text = font.render(spell_circle.active_spell, True, (255, 255, 255))
        text_rect = spell_text.get_rect(center=(center_x, center_y))
        screen.blit(spell_text, text_rect)

def draw_spell_effect(screen, spell_circle):
    """
    Draw the effect of an active spell.
    
    Args:
        screen: Pygame surface to draw on
        spell_circle: SpellCircle object containing active spell info
    """
    if not spell_circle.active_spell:
        return
    
    # Different effects for different spells
    spell = spell_circle.active_spell
    spell_power = getattr(spell_circle, 'active_spell_power', 100)  # Default to 100 if not available
    screen_width, screen_height = screen.get_width(), screen.get_height()
    
    # Create a transparent surface for the effect
    effect_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    
    # Scale effects based on power level
    alpha = int(min(180, 100 + spell_power / 2))  # 100-180 based on power
    size_scale = 0.5 + (spell_power / 100)  # 0.5-1.5 based on power
    
    # Spell color schemes
    spell_colors = {
        "Steam": {"primary": (100, 150, 255, alpha), "secondary": (200, 230, 255, alpha)},
        "Lava": {"primary": (255, 100, 0, alpha), "secondary": (255, 200, 0, alpha)},
        "Mud": {"primary": (139, 69, 19, alpha), "secondary": (160, 100, 50, alpha)},
        "Storm": {"primary": (100, 100, 255, alpha), "secondary": (255, 255, 255, alpha)},
        # New Air element combinations
        "Breeze": {"primary": (180, 180, 255, alpha), "secondary": (220, 220, 255, alpha)},
        "Sandstorm": {"primary": (180, 160, 100, alpha), "secondary": (210, 190, 130, alpha)},
        "Typhoon": {"primary": (70, 130, 200, alpha), "secondary": (150, 210, 255, alpha)},
        # Multi-cast spells
        "Fireball": {"primary": (255, 50, 0, alpha), "secondary": (255, 180, 0, alpha)},
        "Tidal Wave": {"primary": (0, 50, 200, alpha), "secondary": (100, 150, 255, alpha)},
        "Earthquake": {"primary": (100, 80, 0, alpha), "secondary": (150, 120, 40, alpha)},
        "Tornado": {"primary": (150, 150, 200, alpha), "secondary": (200, 200, 240, alpha)},
        # Three-element combinations
        "Inferno": {"primary": (255, 0, 0, alpha), "secondary": (255, 255, 0, alpha)},
        "Tsunami": {"primary": (0, 0, 180, alpha), "secondary": (100, 100, 255, alpha)},
        "Volcano": {"primary": (200, 0, 0, alpha), "secondary": (150, 75, 0, alpha)},
        # Ultimate spell
        "Cataclysm": {"primary": (100, 0, 100, alpha), "secondary": (255, 255, 255, alpha)},
        # New special effect spells
        "Teleport": {"primary": (255, 255, 255, alpha), "secondary": (180, 100, 255, alpha)},
        "Barrier": {"primary": (0, 150, 180, alpha), "secondary": (100, 255, 255, alpha)}
    }
    
    # Get colors for this spell
    colors = spell_colors.get(spell, {"primary": (200, 200, 200, alpha), "secondary": (255, 255, 255, alpha)})
    
    if spell == "Steam":
        # Steam creates a light blue haze - more intense with higher power
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Add some steam particles
        num_particles = int(15 * size_scale)
        for i in range(num_particles):
            particle_x = (pygame.time.get_ticks() // (i+5)) % screen_width
            particle_y = (pygame.time.get_ticks() // (i+3)) % screen_height
            particle_size = int(8 * size_scale)
            pygame.draw.circle(effect_surface, colors["secondary"], (particle_x, particle_y), particle_size)
        
    elif spell == "Lava":
        # Lava creates an orange-red glow - more intense with higher power
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Add lava bubbles for high-power casts
        if spell_power > 50:
            num_bubbles = int(12 * size_scale)
            for i in range(num_bubbles):
                bubble_x = (pygame.time.get_ticks() // (i+1)) % screen_width
                bubble_y = screen_height - ((pygame.time.get_ticks() // (i+2)) % 200)
                bubble_size = int(12 * size_scale)
                pygame.draw.circle(effect_surface, colors["secondary"], (bubble_x, bubble_y), bubble_size)
        
    elif spell == "Mud":
        # Mud creates a brown effect at the bottom - taller with higher power
        mud_height = int((screen_height // 3) * size_scale)
        pygame.draw.rect(effect_surface, colors["primary"], (0, screen_height - mud_height, screen_width, mud_height))
        
        # Add mud splatters for high-power casts
        if spell_power > 60:
            num_splatters = int(10 * size_scale)
            for i in range(num_splatters):
                splatter_x = (pygame.time.get_ticks() // (i+3)) % screen_width
                splatter_y = screen_height - mud_height - ((pygame.time.get_ticks() // (i+2)) % 120)
                splatter_size = int(10 * size_scale)
                pygame.draw.circle(effect_surface, colors["secondary"], (splatter_x, splatter_y), splatter_size)
        
    elif spell == "Storm":
        # Create a slight blue overlay for storm atmosphere
        pygame.draw.rect(effect_surface, (0, 0, 50, alpha // 3), (0, 0, screen_width, screen_height))
        
        # Storm creates lightning-like effects - more bolts and brighter with higher power
        num_bolts = int(3 + (spell_power / 20))  # 3-8 bolts based on power
        bolt_width = int(2 + (spell_power / 30))  # 2-5 pixels based on power
        
        for i in range(num_bolts):
            # Make timing more random
            time_offset = (pygame.time.get_ticks() + i * 121) % screen_width
            start_x = time_offset
            # Lightning effect gets more jagged with higher power
            zigzags = int(4 + (spell_power / 25))  # 4-8 zigzags
            last_x, last_y = start_x, 0
            
            # Generate points for the lightning bolt
            points = [(last_x, last_y)]
            for j in range(zigzags):
                next_y = int((j+1) * (screen_height / zigzags))
                next_x = last_x + int(((pygame.time.get_ticks() + i*37) // (j+10)) % int(120 * size_scale) - 60 * size_scale)
                points.append((next_x, next_y))
                last_x, last_y = next_x, next_y
            
            # Draw the main bolt
            pygame.draw.lines(effect_surface, colors["secondary"], False, points, bolt_width)
            
            # Draw a thinner "glow" around the bolt for effect
            glow_color = (colors["secondary"][0], colors["secondary"][1], colors["secondary"][2], colors["secondary"][3] // 2)
            pygame.draw.lines(effect_surface, glow_color, False, points, bolt_width + 3)
    
    elif spell == "Breeze":
        # Breeze creates gentle wind-like effects
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Add flowing air particles
        num_particles = int(20 * size_scale)
        for i in range(num_particles):
            wave_y = int(screen_height/2 + math.sin((pygame.time.get_ticks() + i*100)/200) * 50)
            particle_x = (pygame.time.get_ticks() // (7-i%7)) % screen_width
            particle_size = int(5 * size_scale)
            pygame.draw.circle(effect_surface, colors["secondary"], (particle_x, wave_y), particle_size)
            # Draw trail
            for j in range(3):
                trail_x = (particle_x - (j+1)*15) % screen_width
                trail_size = particle_size - j
                if trail_size > 0:
                    trail_alpha = alpha - j*40
                    if trail_alpha > 0:
                        trail_color = (colors["secondary"][0], colors["secondary"][1], colors["secondary"][2], trail_alpha)
                        pygame.draw.circle(effect_surface, trail_color, (trail_x, wave_y), trail_size)

    elif spell == "Sandstorm":
        # Sandstorm creates swirling sand particles
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Add sand particles
        num_particles = int(30 * size_scale)
        for i in range(num_particles):
            # Swirling pattern
            angle = (pygame.time.get_ticks()/1000 + i/10) % (2*math.pi)
            distance = 100 + (i % 5) * 30
            center_x, center_y = screen_width//2, screen_height//2
            particle_x = int(center_x + math.cos(angle) * distance)
            particle_y = int(center_y + math.sin(angle) * distance)
            particle_size = int(3 * size_scale)
            pygame.draw.circle(effect_surface, colors["secondary"], (particle_x, particle_y), particle_size)

    elif spell == "Typhoon":
        # Typhoon creates a swirling water effect
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Add swirling water effect
        center_x, center_y = screen_width//2, screen_height//2
        num_rings = int(5 * size_scale)
        max_radius = min(screen_width, screen_height) // 2
        
        for i in range(num_rings):
            radius = max_radius * (i+1)/num_rings
            thickness = int(3 * size_scale)
            start_angle = (pygame.time.get_ticks()/500 + i/2) % (2*math.pi)
            end_angle = start_angle + math.pi  # Half circle
            rect = (center_x - radius, center_y - radius, radius*2, radius*2)
            pygame.draw.arc(effect_surface, colors["secondary"], rect, start_angle, end_angle, thickness)

    elif spell == "Fireball":
        # Fireball creates an intense fire with expanding circles
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Center of the fireball effect
        center_x, center_y = screen_width//2, screen_height//2
        
        # Pulsating fireball
        pulse = (math.sin(pygame.time.get_ticks()/200) + 1) / 2  # 0 to 1
        radius = int(50 * size_scale * (1 + pulse * 0.3))
        
        # Draw multiple layers of the fireball
        for i in range(5):
            layer_radius = radius - i*8
            if layer_radius > 0:
                color_blend = i/5  # Blend factor between primary and secondary
                r = int(colors["primary"][0] * (1-color_blend) + colors["secondary"][0] * color_blend)
                g = int(colors["primary"][1] * (1-color_blend) + colors["secondary"][1] * color_blend)
                b = int(colors["primary"][2] * (1-color_blend) + colors["secondary"][2] * color_blend)
                a = alpha
                pygame.draw.circle(effect_surface, (r, g, b, a), (center_x, center_y), layer_radius)
        
        # Add fire sparks
        num_sparks = int(20 * size_scale)
        for i in range(num_sparks):
            angle = (pygame.time.get_ticks()/100 + i*20) % 360
            distance = radius + (math.sin(pygame.time.get_ticks()/200 + i) + 1) * 20
            spark_x = center_x + int(math.cos(math.radians(angle)) * distance)
            spark_y = center_y + int(math.sin(math.radians(angle)) * distance)
            spark_size = int(3 * size_scale)
            pygame.draw.circle(effect_surface, colors["secondary"], (spark_x, spark_y), spark_size)

    elif spell == "Tidal Wave":
        # Tidal Wave creates a sweeping water effect
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Wave height depends on time
        wave_height = int(screen_height * 0.4 * size_scale)
        wave_position = (pygame.time.get_ticks() // 20) % (screen_width * 2)
        
        # Draw the wave as a polygon
        points = [(0, screen_height)]  # Start at bottom left
        num_points = 20
        for i in range(num_points + 1):
            x = screen_width * i / num_points
            # Create a wave pattern
            y_offset = math.sin((x + wave_position) / 100) * 20 * size_scale
            y = screen_height - wave_height + y_offset
            points.append((x, y))
        points.append((screen_width, screen_height))  # End at bottom right
        
        pygame.draw.polygon(effect_surface, colors["secondary"], points)
        
        # Add water droplets above the wave
        num_droplets = int(15 * size_scale)
        for i in range(num_droplets):
            droplet_x = (pygame.time.get_ticks() // (i+5)) % screen_width
            droplet_y = screen_height - wave_height - ((pygame.time.get_ticks() // (i+3)) % 100)
            droplet_size = int(4 * size_scale)
            pygame.draw.circle(effect_surface, colors["secondary"], (droplet_x, droplet_y), droplet_size)

    elif spell == "Earthquake":
        # Earthquake creates a shaking effect and cracks in the ground
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Shake effect - offset the drawing slightly
        shake_amount = int(5 * size_scale)
        shake_x = (math.sin(pygame.time.get_ticks()/50) * shake_amount)
        shake_y = (math.cos(pygame.time.get_ticks()/40) * shake_amount)
        
        # Ground cracks
        num_cracks = int(6 * size_scale)
        ground_y = int(screen_height * 0.7)
        
        for i in range(num_cracks):
            crack_start_x = (screen_width * i / num_cracks) + shake_x
            crack_points = [(crack_start_x, ground_y + shake_y)]
            
            # Create a jagged line for each crack
            segments = 8
            for j in range(1, segments + 1):
                next_x = crack_start_x + (j * 20 * size_scale) * math.sin(j * 0.5 + pygame.time.get_ticks()/500)
                next_y = ground_y + (j * 20 * size_scale) + shake_y
                crack_points.append((next_x, next_y))
            
            pygame.draw.lines(effect_surface, colors["secondary"], False, crack_points, int(3 * size_scale))

    elif spell == "Tornado":
        # Tornado creates a spinning funnel
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Tornado funnel
        center_x = screen_width // 2
        top_y = int(screen_height * 0.2)
        bottom_y = screen_height
        
        # Draw the tornado as a series of ellipses
        num_segments = int(12 * size_scale)
        for i in range(num_segments):
            segment_y = top_y + (bottom_y - top_y) * i / num_segments
            # Width increases as we go down
            width = int(10 * size_scale + (50 * size_scale * i / num_segments))
            # Add some horizontal movement based on time
            offset_x = int(math.sin(pygame.time.get_ticks()/200 + i/2) * 10 * size_scale)
            
            pygame.draw.ellipse(effect_surface, colors["secondary"], 
                              (center_x - width/2 + offset_x, segment_y, width, 10))
        
        # Add debris particles
        num_particles = int(25 * size_scale)
        for i in range(num_particles):
            # Particles swirl around the tornado
            angle = (pygame.time.get_ticks()/50 + i*30) % 360
            height_factor = (i % num_segments) / num_segments
            y = top_y + (bottom_y - top_y) * height_factor
            radius = 10 + width * height_factor
            x = center_x + math.cos(math.radians(angle)) * radius
            
            particle_size = int(2 * size_scale)
            pygame.draw.circle(effect_surface, (220, 220, 220, alpha), (x, y), particle_size)

    elif spell == "Cataclysm":
        # Cataclysm combines elements of all spells
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Create a pulsating effect
        pulse = (math.sin(pygame.time.get_ticks()/100) + 1) / 2  # 0 to 1
        
        # Draw concentric circles from the center
        center_x, center_y = screen_width//2, screen_height//2
        num_circles = int(8 * size_scale)
        
        for i in range(num_circles):
            circle_radius = int((100 + i*30) * size_scale * (0.8 + pulse * 0.4))
            circle_width = int(5 * size_scale)
            
            # Cycle through element colors
            cycle = (pygame.time.get_ticks()//100 + i*20) % 400
            if cycle < 100:
                color = (255, 60, 60, alpha//2)  # Fire
            elif cycle < 200:
                color = (60, 60, 255, alpha//2)  # Water
            elif cycle < 300:
                color = (60, 255, 60, alpha//2)  # Earth
            else:
                color = (200, 200, 255, alpha//2)  # Air
            
            pygame.draw.circle(effect_surface, color, (center_x, center_y), circle_radius, circle_width)
        
        # Add elemental particles around the screen
        num_particles = int(40 * size_scale)
        for i in range(num_particles):
            # Randomize positions based on time
            x = (pygame.time.get_ticks() // (i+3)) % screen_width
            y = (pygame.time.get_ticks() // (i+5)) % screen_height
            
            # Vary particle color by position
            if x < screen_width/2 and y < screen_height/2:
                color = (255, 60, 60, alpha)  # Fire (top left)
            elif x >= screen_width/2 and y < screen_height/2:
                color = (60, 60, 255, alpha)  # Water (top right)
            elif x < screen_width/2 and y >= screen_height/2:
                color = (60, 255, 60, alpha)  # Earth (bottom left)
            else:
                color = (200, 200, 255, alpha)  # Air (bottom right)
            
            particle_size = int(4 * size_scale)
            pygame.draw.circle(effect_surface, color, (x, y), particle_size)
    
    elif spell == "Teleport":
        # Teleport creates a bright flash and portal-like effect
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Flash effect - increases and decreases based on time
        flash_time = pygame.time.get_ticks() % 500  # 0-500ms cycle
        flash_intensity = 0
        
        if flash_time < 100:  # Quick flash in the first 100ms
            flash_intensity = flash_time / 100
        elif flash_time < 200:  # Fade out in the next 100ms
            flash_intensity = (200 - flash_time) / 100
        
        if flash_intensity > 0:
            flash_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            flash_alpha = int(200 * flash_intensity * size_scale)
            flash_surface.fill((255, 255, 255, flash_alpha))
            effect_surface.blit(flash_surface, (0, 0))
        
        # Portal swirl effect at center of screen
        center_x, center_y = screen_width//2, screen_height//2
        radius = int(100 * size_scale)
        
        # Draw spiral portal
        num_spirals = int(12 * size_scale)
        for i in range(num_spirals):
            start_angle = (pygame.time.get_ticks()/200 + i*(360/num_spirals)) % 360
            end_angle = (start_angle + 20) % 360
            
            # Convert to radians
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Draw arc for spiral
            rect = (center_x - radius, center_y - radius, radius*2, radius*2)
            pygame.draw.arc(effect_surface, colors["secondary"], rect, start_rad, end_rad, int(5 * size_scale))
        
        # Add particles converging to center
        num_particles = int(30 * size_scale)
        for i in range(num_particles):
            # Particle angle and distance from center
            angle = (pygame.time.get_ticks()/100 + i*30) % 360
            angle_rad = math.radians(angle)
            
            # Distance pulses in and out
            base_distance = 200 * size_scale
            pulse = (math.sin(pygame.time.get_ticks()/200 + i/5) + 1) / 2  # 0-1
            distance = base_distance * (0.2 + 0.8 * pulse)
            
            x = center_x + math.cos(angle_rad) * distance
            y = center_y + math.sin(angle_rad) * distance
            
            # Particle size
            particle_size = int(3 * size_scale)
            pygame.draw.circle(effect_surface, colors["secondary"], (x, y), particle_size)
    
    elif spell == "Barrier":
        # Barrier creates a shimmering shield effect
        pygame.draw.rect(effect_surface, colors["primary"], (0, 0, screen_width, screen_height))
        
        # Find all players and draw shield around them
        from game import Player  # Import here to avoid circular imports
        
        # Get all the players from the game state
        players = []
        for obj in globals().values():
            if isinstance(obj, list):
                for item in obj:
                    if isinstance(item, Player):
                        players.append(item)
        
        # Draw shield effect around each player
        for player in players:
            # Shield size
            shield_size = int(100 * size_scale)
            shield_x = player.position[0] - shield_size//2
            shield_y = player.position[1] - shield_size//2
            
            # Shimmering effect
            shimmer = (math.sin(pygame.time.get_ticks()/100) + 1) / 2  # 0-1
            inner_size = shield_size * (0.8 + shimmer * 0.2)
            inner_x = player.position[0] - inner_size//2
            inner_y = player.position[1] - inner_size//2
            
            # Outer shield
            pygame.draw.ellipse(effect_surface, colors["primary"], 
                             (shield_x, shield_y, shield_size, shield_size))
            
            # Inner shield with shimmering effect
            pygame.draw.ellipse(effect_surface, colors["secondary"], 
                             (inner_x, inner_y, inner_size, inner_size), 
                             int(3 * size_scale))
            
            # Add small particles around the shield
            num_particles = int(12 * size_scale)
            for i in range(num_particles):
                angle = (pygame.time.get_ticks()/200 + i*30) % 360
                angle_rad = math.radians(angle)
                
                # Particles move around the shield
                x = player.position[0] + math.cos(angle_rad) * shield_size/2
                y = player.position[1] + math.sin(angle_rad) * shield_size/2
                
                particle_size = int(4 * size_scale)
                pygame.draw.circle(effect_surface, colors["secondary"], (x, y), particle_size)
    
    # Blend the effect onto the main screen
    screen.blit(effect_surface, (0, 0))
    
    # Draw spell info in a neat box at the top
    # Only show if not in main effect area (e.g., avoid mud)
    info_y = 70  # Position below the objective panel
    
    # Create info panel
    panel_width = 200
    panel_height = 40
    panel_x = screen_width // 2 - panel_width // 2
    
    info_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    pygame.draw.rect(info_panel, (0, 0, 0, 180), (0, 0, panel_width, panel_height), border_radius=10)
    
    # Add a slight border glow based on spell type
    border_color = colors["primary"][:3] + (150,)  # Use the spell's primary color
    pygame.draw.rect(info_panel, border_color, (0, 0, panel_width, panel_height), width=2, border_radius=10)
    
    # Draw spell name and power
    font = pygame.font.SysFont(None, 28)
    text = font.render(f"{spell_circle.active_spell}", True, (255, 255, 255))
    info_panel.blit(text, (panel_width//2 - text.get_width()//2, 8))
    
    # Power bar
    bar_width = 150
    bar_height = 8
    bar_x = panel_width//2 - bar_width//2
    bar_y = 28
    
    # Bar background
    pygame.draw.rect(info_panel, (70, 70, 70), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
    
    # Filled portion based on power
    fill_width = int(bar_width * (spell_power / 100))
    
    # Color based on power level
    if spell_power < 40:
        power_color = (200, 60, 60)  # Red for low power
    elif spell_power < 70:
        power_color = (200, 200, 60)  # Yellow for medium power
    else:
        power_color = (60, 200, 60)  # Green for high power
        
    pygame.draw.rect(info_panel, power_color, (bar_x, bar_y, fill_width, bar_height), border_radius=4)
    
    # Blit the info panel
    screen.blit(info_panel, (panel_x, info_y))

def draw_level(screen, level):
    """
    Draw the level elements such as walls, gaps, enemies, etc.
    
    Args:
        screen: Pygame surface to draw on
        level: Level object containing elements to draw
    """
    for element in level.elements:
        element_type = element.get('type', 'unknown')
        position = element.get('position', (0, 0))
        size = element.get('size', (50, 50))
        
        # Handle different element types
        if element_type == 'wall':
            # Walls are solid obstacles
            pygame.draw.rect(screen, (120, 100, 80), (*position, *size))
            # Add a subtle 3D effect
            pygame.draw.rect(screen, (150, 130, 110), (*position, *size), 1)
            pygame.draw.line(screen, (90, 70, 50), 
                            (position[0], position[1] + size[1]), 
                            (position[0] + size[0], position[1] + size[1]), 
                            2)
            
        elif element_type == 'gap':
            # Gaps are areas that need to be filled
            # Draw as a darker area with a dashed border
            pygame.draw.rect(screen, (40, 40, 60), (*position, *size))
            
            # Draw dashed border (using short lines)
            dash_length = 5
            dash_gap = 3
            x, y = position
            width, height = size
            
            # Top border
            for dx in range(0, width, dash_length + dash_gap):
                dash_end = min(dx + dash_length, width)
                pygame.draw.line(screen, (180, 180, 200), 
                                (x + dx, y), 
                                (x + dash_end, y), 
                                1)
            
            # Bottom border
            for dx in range(0, width, dash_length + dash_gap):
                dash_end = min(dx + dash_length, width)
                pygame.draw.line(screen, (180, 180, 200), 
                                (x + dx, y + height), 
                                (x + dash_end, y + height), 
                                1)
            
            # Left border
            for dy in range(0, height, dash_length + dash_gap):
                dash_end = min(dy + dash_length, height)
                pygame.draw.line(screen, (180, 180, 200), 
                                (x, y + dy), 
                                (x, y + dash_end), 
                                1)
            
            # Right border
            for dy in range(0, height, dash_length + dash_gap):
                dash_end = min(dy + dash_length, height)
                pygame.draw.line(screen, (180, 180, 200), 
                                (x + width, y + dy), 
                                (x + width, y + dash_end), 
                                1)
            
        elif element_type == 'enemy':
            # Enemies are represented as threatening shapes
            x, y = position
            enemy_color = (200, 60, 60)  # Reddish
            
            # If stunned, change the color
            if element.get('stunned', False):
                enemy_color = (100, 100, 200)  # Bluish when stunned
            
            # Draw enemy body (pentagon)
            radius = 25
            points = []
            for i in range(5):
                angle = 2 * math.pi * i / 5 - math.pi / 2  # Start from top
                px = x + radius * math.cos(angle)
                py = y + radius * math.sin(angle)
                points.append((px, py))
            
            pygame.draw.polygon(screen, enemy_color, points)
            
            # Draw health bar
            health = element.get('health', 100)
            bar_width = radius * 2
            bar_height = 5
            bar_x = x - radius
            bar_y = y - radius - 10
            
            # Background
            pygame.draw.rect(screen, (70, 70, 70), (bar_x, bar_y, bar_width, bar_height))
            
            # Health level
            health_percentage = max(0, health / 100)
            health_width = int(bar_width * health_percentage)
            
            # Color based on health level
            if health_percentage < 0.3:
                health_color = (200, 60, 60)  # Red
            elif health_percentage < 0.6:
                health_color = (200, 200, 60)  # Yellow
            else:
                health_color = (60, 200, 60)  # Green
                
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
            
            # Border
            pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 1)
            
        elif element_type == 'effect':
            # Handle different visual effects
            effect_type = element.get('effect_type', 'generic')
            position = element.get('position', (0, 0))
            color = element.get('color', (255, 255, 255))
            timer = element.get('timer', 0)
            radius = element.get('radius', 50)
            
            # Fade based on timer
            alpha = int(255 * (timer / 60))  # Fade out as timer goes down
            
            if effect_type == 'explosion':
                # Fireball explosion
                effect_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                
                # Draw gradient explosion
                for r in range(int(radius), 0, -5):
                    # Calculate fade-out based on radius
                    fade = r / radius
                    r_color = (color[0], color[1], color[2], int(alpha * fade))
                    
                    # Draw a circle with this radius and color
                    pygame.draw.circle(effect_surface, r_color, (radius, radius), r)
                
                # Draw some random "sparks"
                import random
                for _ in range(20):
                    # Create a spark at a random angle and distance
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(0, radius)
                    
                    # Convert polar to cartesian coordinates
                    spark_x = radius + distance * math.cos(angle)
                    spark_y = radius + distance * math.sin(angle)
                    
                    # Random size (bigger near center)
                    spark_size = int(3 + (radius - distance) / 10)
                    
                    # Draw the spark
                    pygame.draw.circle(effect_surface, 
                                     (255, 255, 220, alpha), 
                                     (int(spark_x), int(spark_y)), 
                                     spark_size)
                
                # Blit the effect to the screen
                screen.blit(effect_surface, 
                           (position[0] - radius, position[1] - radius), 
                           special_flags=pygame.BLEND_ALPHA_SDL2)
            
            elif effect_type == 'wave':
                # Tidal Wave expanding ring
                effect_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                
                # Draw concentric rings
                ring_width = 10
                for r in range(int(radius), max(0, int(radius) - ring_width*3), -ring_width):
                    # Calculate alpha for this ring
                    ring_alpha = int(alpha * (r / radius))
                    r_color = (color[0], color[1], color[2], ring_alpha)
                    
                    # Draw a ring with this radius and color
                    pygame.draw.circle(effect_surface, r_color, (radius, radius), r, ring_width - 1)
                
                # Add wave details (horizontal lines)
                wavelength = 15
                wave_amplitude = 3
                
                for y in range(0, int(radius*2), wavelength):
                    # Calculate wave alpha (fade from center)
                    distance = abs(y - radius) / radius
                    wave_alpha = int(alpha * (1 - distance))
                    wave_color = (220, 220, 255, wave_alpha)
                    
                    # Draw a wavy line
                    points = []
                    for x in range(0, int(radius*2), 5):
                        # Calculate distance from center
                        dx = x - radius
                        dy = y - radius
                        dist = math.sqrt(dx*dx + dy*dy)
                        
                        if dist < radius:
                            # Calculate wave offset
                            wave_y = y + wave_amplitude * math.sin(x / 5)
                            points.append((x, wave_y))
                    
                    # Draw the wave line
                    if len(points) > 1:
                        pygame.draw.lines(effect_surface, wave_color, False, points, 2)
                
                # Blit the effect to the screen
                screen.blit(effect_surface, 
                           (position[0] - radius, position[1] - radius), 
                           special_flags=pygame.BLEND_ALPHA_SDL2)
            
            elif effect_type == 'earthquake':
                # Earthquake effect (cracks in the ground)
                effect_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
                
                # Draw cracks radiating from center
                import random
                center_x, center_y = position
                
                # Number of cracks based on timer
                num_cracks = 20 
                
                for _ in range(num_cracks):
                    # Starting angle
                    angle = random.uniform(0, 2 * math.pi)
                    
                    # Create a random jagged line
                    points = [(center_x, center_y)]
                    
                    # Line length based on timer
                    line_length = random.uniform(50, 150) * (timer / 90)
                    segments = 8
                    
                    for i in range(1, segments+1):
                        # Each segment deviates slightly from the main angle
                        segment_angle = angle + random.uniform(-0.5, 0.5)
                        
                        # Distance for this segment
                        distance = line_length * (i / segments)
                        
                        # Calculate end point
                        end_x = center_x + distance * math.cos(segment_angle)
                        end_y = center_y + distance * math.sin(segment_angle)
                        
                        # Add to points list
                        points.append((end_x, end_y))
                    
                    # Calculate alpha based on timer
                    crack_alpha = int(alpha * random.uniform(0.7, 1.0))
                    crack_color = (color[0], color[1], color[2], crack_alpha)
                    
                    # Draw the crack
                    pygame.draw.lines(effect_surface, crack_color, False, points, 
                                     random.randint(1, 3))
                
                # Blit the effect to the screen
                screen.blit(effect_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
                
                # Add a screen shake effect during an earthquake
                shake_amount = int(5 * (timer / 90))
                if shake_amount > 0:
                    screen_offset = (random.randint(-shake_amount, shake_amount),
                                   random.randint(-shake_amount, shake_amount))
                    # Note: We'd need to modify the rendering system to truly implement screen shake
                    # For now, we just indicate it would happen here
            
        elif element_type == 'tornado':
            # Tornado effect (swirling vortex)
            position = element.get('position', (0, 0))
            radius = element.get('radius', 120)
            color = element.get('color', (200, 200, 200))
            timer = element.get('timer', 0)
            
            # Create a surface for the tornado
            effect_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            
            # Calculate alpha based on timer
            max_time = 180  # The initial timer value
            alpha_base = int(255 * (timer / max_time))
            
            # Draw the tornado as a series of ovals with rotation
            import random
            rotation = (pygame.time.get_ticks() / 20) % 360  # Base rotation
            
            # Number of ovals in the tornado
            num_ovals = 12
            
            for i in range(num_ovals):
                # Calculate size of this oval
                oval_height = radius * 0.8  # Height is consistent
                oval_width = radius * (0.5 + 0.5 * (i / num_ovals))  # Width increases toward the bottom
                
                # Calculate vertical position (ovals stack from bottom to top)
                y_offset = radius - (radius * 0.8 * (i / num_ovals))
                
                # Calculate alpha for this oval (more transparent at the top)
                oval_alpha = int(alpha_base * (0.4 + 0.6 * (i / num_ovals)))
                
                # Calculate rotation for this oval (increases toward the top)
                oval_rotation = rotation + (i * 30)  # 30 degrees offset per oval
                
                # Convert rotation to radians
                oval_rotation_rad = oval_rotation * math.pi / 180
                
                # Calculate center point with a slight wobble
                wobble = 5 * math.sin(pygame.time.get_ticks() / 100 + i)
                center_x = radius + wobble
                center_y = y_offset
                
                # Calculate points around the oval
                num_points = 20
                points = []
                
                for j in range(num_points):
                    angle = 2 * math.pi * j / num_points
                    # Oval parametric equation
                    x = oval_width/2 * math.cos(angle)
                    y = oval_height/2 * math.sin(angle)
                    
                    # Apply rotation
                    rotated_x = x * math.cos(oval_rotation_rad) - y * math.sin(oval_rotation_rad)
                    rotated_y = x * math.sin(oval_rotation_rad) + y * math.cos(oval_rotation_rad)
                    
                    # Translate to center
                    points.append((center_x + rotated_x, center_y + rotated_y))
                
                # Draw the oval
                oval_color = (color[0], color[1], color[2], oval_alpha)
                pygame.draw.polygon(effect_surface, oval_color, points)
            
            # Add some swirling debris particles
            num_particles = 30
            for _ in range(num_particles):
                # Random position along the radius
                dist = random.uniform(0, radius * 0.9)
                angle = random.uniform(0, 2 * math.pi)
                
                # Apply rotation based on current time
                time_factor = pygame.time.get_ticks() / 1000
                angle += time_factor * (2 - dist/radius)  # Faster rotation near center
                
                # Calculate position
                particle_x = radius + dist * math.cos(angle)
                particle_y = radius + dist * math.sin(angle)
                
                # Size and color vary based on distance from center
                particle_size = int(2 + 3 * (dist/radius))
                particle_alpha = int(alpha_base * (0.5 + 0.5 * (dist/radius)))
                
                # Random color variation
                r_offset = random.randint(-20, 20)
                g_offset = random.randint(-20, 20)
                b_offset = random.randint(-20, 20)
                
                particle_color = (
                    max(0, min(255, color[0] + r_offset)),
                    max(0, min(255, color[1] + g_offset)),
                    max(0, min(255, color[2] + b_offset)),
                    particle_alpha
                )
                
                # Draw the particle
                pygame.draw.circle(effect_surface, particle_color, 
                                  (int(particle_x), int(particle_y)), 
                                  particle_size)
            
            # Blit the tornado to the screen
            screen.blit(effect_surface, 
                       (position[0] - radius, position[1] - radius), 
                       special_flags=pygame.BLEND_ALPHA_SDL2)

def draw_level_text(screen, level):
    """
    Draw text information for the current level.
    
    Args:
        screen: Pygame surface to draw on
        level: Level object with text information
    """
    font = pygame.font.SysFont(None, 28)
    
    # Get all text items from the level
    text_items = level.get_display_text()
    
    # Draw each text item
    for text, position in text_items:
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, position)

def draw_level_transition(screen, level_num, total_levels):
    """
    Draw a level transition screen.
    
    Args:
        screen: Pygame surface to draw on
        level_num: Current level number (1-based)
        total_levels: Total number of levels
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()
    
    # Fill with a semi-transparent black
    transition_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    pygame.draw.rect(transition_surface, (0, 0, 0, 200), (0, 0, screen_width, screen_height))
    screen.blit(transition_surface, (0, 0))
    
    # Draw level text
    font_large = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    
    level_text = font_large.render(f"Level {level_num}", True, (255, 255, 255))
    screen.blit(level_text, (screen_width//2 - level_text.get_width()//2, screen_height//2 - 50))
    
    progress_text = font_small.render(f"{level_num} of {total_levels}", True, (200, 200, 200))
    screen.blit(progress_text, (screen_width//2 - progress_text.get_width()//2, screen_height//2 + 30))
    
    instruction_text = font_small.render("Press SPACE to start", True, (200, 200, 200))
    screen.blit(instruction_text, (screen_width//2 - instruction_text.get_width()//2, screen_height//2 + 80))

def draw_main_menu(screen, selected_option):
    """
    Draw the main menu with selectable options.
    
    Args:
        screen: Pygame surface to draw on
        selected_option: Index of the currently selected option
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()
    
    # Fill background with a gradient
    for i in range(screen_height):
        # Create a dark blue to black gradient
        color = (0, 0, max(50 - i // 8, 0))
        pygame.draw.line(screen, color, (0, i), (screen_width, i))
    
    # Draw game title
    title_font = pygame.font.SysFont(None, 90)
    title_text = title_font.render("Wizards Casting Spells", True, (255, 255, 255))
    screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, 100))
    
    # Menu options
    options = ["Start Game", "Exit"]
    option_font = pygame.font.SysFont(None, 50)
    option_y = 300
    
    # Draw each option
    for i, option in enumerate(options):
        # Highlight the selected option
        if i == selected_option:
            color = (255, 255, 0)  # Yellow for selected
            # Draw a wizard icon next to selected option
            wizard_colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0)]
            pygame.draw.rect(screen, wizard_colors[i % 3], 
                          (screen_width//2 - 150, option_y + i * 60, 30, 30))
        else:
            color = (200, 200, 200)  # Gray for unselected
            
        option_text = option_font.render(option, True, color)
        screen.blit(option_text, (screen_width//2 - option_text.get_width()//2, option_y + i * 60))
    
    # Draw instructions
    instruction_font = pygame.font.SysFont(None, 26)
    instructions = [
        "Use UP/DOWN arrows to select, ENTER to confirm",
        "Movement: Player 1 (Fire) - WASD",
        "          Player 2 (Water) - TFGH",
        "          Player 3 (Earth) - IJKL",
        "Casting: Press and HOLD 1, 4, or 7 to charge, release to cast"
    ]
    
    # Draw a semi-transparent box for instructions
    instruction_box = pygame.Surface((screen_width - 100, 140), pygame.SRCALPHA)
    pygame.draw.rect(instruction_box, (0, 0, 0, 150), instruction_box.get_rect())
    screen.blit(instruction_box, (50, 440))
    
    for i, instruction in enumerate(instructions):
        instr_text = instruction_font.render(instruction, True, (200, 200, 200))
        screen.blit(instr_text, (screen_width//2 - instr_text.get_width()//2, 450 + i * 25))

def draw_unlocked_spell(screen, spell_name):
    """
    Draw a notification about unlocking a new spell.
    
    Args:
        screen: Pygame surface to draw on
        spell_name: Name of the unlocked spell
    """
    screen_width, screen_height = screen.get_width(), screen.get_height()
    
    # Create a transparent overlay
    overlay = pygame.Surface((screen_width, 80), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 180), (0, 0, screen_width, 80))
    screen.blit(overlay, (0, screen_height - 80))
    
    # Draw the text
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"New spell unlocked: {spell_name}!", True, (255, 255, 0))
    screen.blit(text, (screen_width//2 - text.get_width()//2, screen_height - 60))

def draw_objective_panel(screen, level):
    """
    Draw a clean objective panel at the top of the screen.
    
    Args:
        screen: Pygame surface to draw on
        level: Level object with objective information
    """
    screen_width = screen.get_width()
    
    # Create a semi-transparent panel at the top
    panel_height = 50
    panel = pygame.Surface((screen_width, panel_height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (0, 0, 0, 150), (0, 0, screen_width, panel_height))
    screen.blit(panel, (0, 0))
    
    # Draw a subtle border at the bottom of the panel
    pygame.draw.line(screen, (100, 100, 100), (0, panel_height), (screen_width, panel_height), 1)
    
    # Draw level name and objective
    font = pygame.font.SysFont(None, 24)
    
    # Level name on the left
    level_text = font.render(f"Level: {level.name}", True, (255, 255, 255))
    screen.blit(level_text, (20, 15))
    
    # Objective in the center
    objective_text = font.render(f"Objective: {level.objective}", True, (220, 220, 220))
    objective_x = screen_width // 2 - objective_text.get_width() // 2
    screen.blit(objective_text, (objective_x, 15))
    
    # Additional info based on level type (right side)
    if level.level_type == 'survival':
        # Timer for survival levels
        seconds_left = level.timer // 60
        timer_text = font.render(f"Time: {seconds_left}s", True, (255, 255, 0))
        screen.blit(timer_text, (screen_width - timer_text.get_width() - 20, 15))
    elif level.level_type == 'combat':
        # Count enemies for combat levels
        enemies_left = sum(1 for elem in level.elements if elem['type'] == 'enemy')
        enemies_text = font.render(f"Enemies: {enemies_left}", True, (255, 100, 100))
        screen.blit(enemies_text, (screen_width - enemies_text.get_width() - 20, 15))
    
    # Completion status
    if level.is_completed:
        complete_font = pygame.font.SysFont(None, 26)
        complete_text = complete_font.render("COMPLETED!", True, (50, 255, 50))
        screen.blit(complete_text, (screen_width - complete_text.get_width() - 20, 15))
