import pygame
import os

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
    # Try to use sprites if available
    sprite_key = player.element.lower()
    if player.is_casting:
        sprite_key += "_casting"
    
    x, y = player.position
    
    if sprite_key in wizard_sprites:
        # If we have sprites, use them
        screen.blit(wizard_sprites[sprite_key], (x, y - 20))  # Adjust for hat height
    else:
        # Draw a more wizard-like shape instead of just a square
        wizard_size = 50
        color = player.get_display_color()
        
        # Draw wizard body (slightly rounded rectangle)
        body_rect = pygame.Rect(x, y, wizard_size, wizard_size)
        pygame.draw.rect(screen, color, body_rect, border_radius=5)
        
        # Draw wizard hat (triangle on top)
        hat_color = (min(color[0] + 20, 255), min(color[1] + 20, 255), min(color[2] + 20, 255))
        hat_points = [(x + wizard_size // 2, y - 20), (x + 10, y), (x + wizard_size - 10, y)]
        pygame.draw.polygon(screen, hat_color, hat_points)
        
        # Draw staff (if casting)
        if player.is_casting:
            # Staff position
            staff_start = (x + wizard_size - 10, y + wizard_size - 10)
            staff_end = (x + wizard_size + 15, y + wizard_size - 25)
            
            # Draw staff (brown)
            pygame.draw.line(screen, (139, 69, 19), staff_start, staff_end, 3)
            
            # Draw glowing tip
            tip_color = player.color
            pygame.draw.circle(screen, tip_color, staff_end, 5)
            
            # Draw glow around tip
            glow_radius = 8 + (player.cast_time % 5)
            glow_color = (tip_color[0], tip_color[1], tip_color[2], 150)  # Semi-transparent
            
            # Create a surface for the glow effect
            glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
            
            # Blit the glow to the screen
            screen.blit(glow_surface, (staff_end[0] - glow_radius, staff_end[1] - glow_radius), special_flags=pygame.BLEND_ALPHA_SDL2)

def draw_spell_circle(screen, spell_circle):
    """
    Draw the spell circle showing active elements and timer.
    
    Args:
        screen: Pygame surface to draw on
        spell_circle: SpellCircle object containing elements and timer info
    """
    # Draw the main circle
    center_x, center_y = screen.get_width() // 2, screen.get_height() - 100
    circle_radius = 50
    
    # Draw the base circle (gray when empty, white when elements present)
    circle_color = (200, 200, 200) if spell_circle.elements else (100, 100, 100)
    pygame.draw.circle(screen, circle_color, (center_x, center_y), circle_radius)
    
    # If there are elements in the circle, draw colored segments
    if spell_circle.elements:
        # Element colors
        element_colors = {
            "Fire": (255, 0, 0),    # Red
            "Water": (0, 0, 255),   # Blue
            "Earth": (0, 255, 0)    # Green
        }
        
        # Draw a colored arc for each element
        num_elements = len(spell_circle.elements)
        for i, element in enumerate(spell_circle.elements):
            # Calculate the arc angles for this element
            start_angle = i * (360 / num_elements)
            end_angle = (i + 1) * (360 / num_elements)
            
            # Draw a colored circle segment (simplified as a smaller circle)
            color = element_colors[element]
            # For simplicity, we'll just draw smaller circles at positions around the main circle
            angle_rad = pygame.math.Vector2(0, -1).angle_to(pygame.math.Vector2(1, 0)) + start_angle
            offset_x = circle_radius * 0.6 * pygame.math.Vector2(1, 0).rotate(angle_rad).x
            offset_y = circle_radius * 0.6 * pygame.math.Vector2(1, 0).rotate(angle_rad).y
            pygame.draw.circle(screen, color, (center_x + offset_x, center_y + offset_y), 15)
    
    # Draw timer indicator if active
    if spell_circle.activation_timer > 0:
        # Draw a shrinking white circle to indicate time remaining
        timer_radius = circle_radius * (spell_circle.activation_timer / 120)  # 120 is max timer value
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), timer_radius, 2)
    
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
    screen_width, screen_height = screen.get_width(), screen.get_height()
    
    # Create a transparent surface for the effect
    effect_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    
    if spell == "Steam":
        # Steam creates a light blue haze
        pygame.draw.rect(effect_surface, (100, 100, 255, 100), (0, 0, screen_width, screen_height))
        
    elif spell == "Lava":
        # Lava creates an orange-red glow
        pygame.draw.rect(effect_surface, (255, 100, 0, 100), (0, 0, screen_width, screen_height))
        
    elif spell == "Mud":
        # Mud creates a brown effect at the bottom
        pygame.draw.rect(effect_surface, (139, 69, 19, 100), (0, screen_height//2, screen_width, screen_height//2))
        
    elif spell == "Storm":
        # Storm creates lightning-like effects
        for _ in range(5):
            start_x = pygame.time.get_ticks() % screen_width
            pygame.draw.line(effect_surface, (255, 255, 255, 200), 
                            (start_x, 0), 
                            (start_x + pygame.time.get_ticks() % 100 - 50, screen_height),
                            3)
    
    # Blend the effect onto the main screen
    screen.blit(effect_surface, (0, 0))
    
    # Draw spell name
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Spell: {spell_circle.active_spell}", True, (255, 255, 255))
    screen.blit(text, (screen_width//2 - text.get_width()//2, 50))

def draw_level(screen, level):
    """
    Draw all elements of the current level.
    
    Args:
        screen: Pygame surface to draw on
        level: Level object containing level elements
    """
    # Draw different elements based on their type
    for elem in level.elements:
        if elem['type'] == 'gap':
            # Draw a gap as a black rectangle
            pygame.draw.rect(screen, (0, 0, 0), 
                            (elem['position'][0], elem['position'][1], 
                             elem['size'][0], elem['size'][1]))
        
        elif elem['type'] == 'enemy':
            # Draw an enemy as a white square with health bar
            enemy_size = 40
            enemy_pos = (int(elem['position'][0]), int(elem['position'][1]))
            
            # Draw the enemy
            pygame.draw.rect(screen, (255, 255, 255), 
                            (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
            
            # Draw health bar
            health_width = enemy_size * (elem['health'] / 100)
            pygame.draw.rect(screen, (255, 0, 0), 
                            (enemy_pos[0], enemy_pos[1] - 10, health_width, 5))

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
    instruction_font = pygame.font.SysFont(None, 28)
    instructions = [
        "Use UP/DOWN arrows to select",
        "Press ENTER to confirm",
        "Press W, T, I to cast spells in-game"
    ]
    
    for i, instruction in enumerate(instructions):
        instr_text = instruction_font.render(instruction, True, (150, 150, 150))
        screen.blit(instr_text, (screen_width//2 - instr_text.get_width()//2, 450 + i * 30))

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
