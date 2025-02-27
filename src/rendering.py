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
    Draw any active spell effects on the screen.
    
    Args:
        screen (pygame.Surface): The screen to draw on
        spell_circle (SpellCircle): The spell circle to get effect information from
    """
    if spell_circle.active_spell:
        # Get the spell name and target position
        spell_name = spell_circle.active_spell
        spell_power = spell_circle.active_spell_power
        target_pos = spell_circle.target_position
        
        # Calculate the radius of the spell effect based on spell type and power
        radius = 0
        if spell_name in ['Lava', 'Steam', 'Mud']:
            radius = 100 * (0.5 + spell_power / 100)
        elif spell_name == 'Storm':
            radius = 200 * (0.5 + spell_power / 100)
        elif spell_name == 'Fireball':
            radius = 150 * (0.5 + spell_power / 100)
        elif spell_name == 'Teleport':
            radius = 40 * (0.5 + spell_power / 100)
        elif spell_name == 'Barrier':
            radius = 60 * (0.5 + spell_power / 100)
            
        # Draw a semi-transparent circle to represent the area of effect
        aoe_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        
        # Different colors for different spell types
        if 'Fire' in spell_name or 'Lava' in spell_name or spell_name == 'Fireball':
            color = (255, 100, 0, 100)  # Red-orange with alpha
        elif 'Water' in spell_name or 'Steam' in spell_name:
            color = (0, 100, 255, 100)  # Blue with alpha
        elif 'Earth' in spell_name or 'Mud' in spell_name:
            color = (139, 69, 19, 100)  # Brown with alpha
        elif 'Air' in spell_name or spell_name == 'Storm':
            color = (200, 200, 200, 100)  # Gray with alpha
        elif spell_name == 'Teleport':
            color = (255, 255, 0, 100)  # Yellow with alpha
        elif spell_name == 'Barrier':
            color = (0, 255, 0, 100)  # Green with alpha
        else:
            color = (255, 255, 255, 100)  # White with alpha
            
        # Draw the circle
        pygame.draw.circle(aoe_surface, color, (radius, radius), radius)
        
        # Calculate the position to draw the surface
        pos = (target_pos[0] - radius, target_pos[1] - radius)
        
        # Draw the effect
        screen.blit(aoe_surface, pos)
        
        # Draw a pulsing border around the AOE to make it more visible
        pulse = abs(((pygame.time.get_ticks() % 1000) - 500) / 500)  # 0-1 pulsing value
        border_color = tuple(c for c in color[:3]) + (int(200 * pulse),)  # Pulsing alpha
        pygame.draw.circle(aoe_surface, border_color, (radius, radius), radius, 3)
        screen.blit(aoe_surface, pos)
        
        # Draw the spell name above the effect
        font = pygame.font.SysFont(None, 24)
        text = font.render(spell_name, True, (255, 255, 255))
        screen.blit(text, (target_pos[0] - text.get_width()//2, target_pos[1] - radius - 30))

def draw_targeting_cursor(screen, position):
    """
    Draw a targeting cursor at the mouse position.
    
    Args:
        screen (pygame.Surface): The screen to draw on
        position (tuple): The (x, y) position to draw the cursor
    """
    # Draw crosshair
    cursor_size = 20
    cursor_color = (255, 255, 255)
    cursor_thickness = 2
    
    # Draw the crosshair lines
    pygame.draw.line(screen, cursor_color, 
                     (position[0] - cursor_size, position[1]),
                     (position[0] + cursor_size, position[1]), 
                     cursor_thickness)
    pygame.draw.line(screen, cursor_color, 
                     (position[0], position[1] - cursor_size),
                     (position[0], position[1] + cursor_size), 
                     cursor_thickness)
    
    # Draw a small circle in the center
    pygame.draw.circle(screen, cursor_color, position, 3, 0)

def draw_level(screen, level):
    """
    Draw the level elements such as walls, gaps, enemies, etc.
    
    Args:
        screen (pygame.Surface): The screen to draw on
        level (Level): The level to draw
    """
    # Draw level elements
    for element in level.elements:
        element_type = element.get('type', 'unknown')
        position = element.get('position', (0, 0))
        
        if element_type == 'gap':
            # Gaps are areas that need to be filled
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(position[0], position[1], 
                                                               element['size'][0], element['size'][1]))
            
            # Draw dashed lines around the gap
            dash_length = 5
            dash_gap = 5
            gap_rect = pygame.Rect(position[0], position[1], element['size'][0], element['size'][1])
            draw_dashed_rect(screen, (150, 150, 150), gap_rect, dash_length, dash_gap)
            
        elif element_type == 'wall':
            # Walls are solid obstacles
            wall_color = (139, 69, 19)  # Brown for walls
            
            # If it's a temporary wall (barrier), make it translucent green
            if element.get('temp', False):
                # Create a semi-transparent surface
                wall_surface = pygame.Surface((element['size'][0], element['size'][1]), pygame.SRCALPHA)
                wall_surface.fill((0, 255, 0, 150))  # Semi-transparent green
                screen.blit(wall_surface, position)
                
                # Draw a border
                pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(position[0], position[1], 
                                                                 element['size'][0], element['size'][1]), 2)
            else:
                pygame.draw.rect(screen, wall_color, pygame.Rect(position[0], position[1], 
                                                               element['size'][0], element['size'][1]))

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

def draw_dashed_rect(surface, color, rect, dash_length=10, gap_length=10):
    """
    Draw a dashed rectangle on the surface.
    
    Args:
        surface: Pygame surface to draw on
        color: RGB tuple color for the dashes
        rect: Pygame Rect object defining the rectangle
        dash_length: Length of each dash in pixels
        gap_length: Length of each gap in pixels
    """
    # Get the four edges of the rectangle
    top_edge = [(rect.left, rect.top), (rect.right, rect.top)]
    right_edge = [(rect.right, rect.top), (rect.right, rect.bottom)]
    bottom_edge = [(rect.right, rect.bottom), (rect.left, rect.bottom)]
    left_edge = [(rect.left, rect.bottom), (rect.left, rect.top)]
    
    # Draw dashed lines for each edge
    for edge in [top_edge, right_edge, bottom_edge, left_edge]:
        draw_dashed_line(surface, color, edge[0], edge[1], dash_length, gap_length)

def draw_dashed_line(surface, color, start_pos, end_pos, dash_length=10, gap_length=10):
    """
    Draw a dashed line from start_pos to end_pos.
    
    Args:
        surface: Pygame surface to draw on
        color: RGB tuple color for the dashes
        start_pos: Starting position (x, y)
        end_pos: Ending position (x, y)
        dash_length: Length of each dash in pixels
        gap_length: Length of each gap in pixels
    """
    # Calculate the total length of the line
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    line_length = max(abs(dx), abs(dy))
    
    # Calculate the unit vector
    if line_length > 0:
        unit_x = dx / line_length
        unit_y = dy / line_length
    else:
        unit_x, unit_y = 0, 0
    
    # Draw the dashed line
    segment_length = dash_length + gap_length
    num_segments = int(line_length / segment_length) + 1
    
    for i in range(num_segments):
        # Calculate segment start and end positions
        segment_start_x = start_pos[0] + unit_x * i * segment_length
        segment_start_y = start_pos[1] + unit_y * i * segment_length
        
        segment_end_x = min(segment_start_x + unit_x * dash_length, end_pos[0]) if dx >= 0 else max(segment_start_x + unit_x * dash_length, end_pos[0])
        segment_end_y = min(segment_start_y + unit_y * dash_length, end_pos[1]) if dy >= 0 else max(segment_start_y + unit_y * dash_length, end_pos[1])
        
        pygame.draw.line(surface, color, (segment_start_x, segment_start_y), (segment_end_x, segment_end_y), 1)
