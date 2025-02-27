import pygame
import sys
import rendering  # Import our rendering module
from game import Player, SpellCircle, create_levels, GameProgress  # Import our game classes

# Initialize Pygame
pygame.init()

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wizards Casting Spells")

# Initialize rendering system (load sprites)
rendering.init_rendering()

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)     # Fire Wizard
BLUE = (0, 0, 255)    # Water Wizard
GREEN = (0, 255, 0)   # Earth Wizard

# Create game progress tracker
game_progress = GameProgress()

# Create players
player1 = Player("Fire", (100, 100), RED)     # Fire Wizard with key 1
player2 = Player("Water", (200, 100), BLUE)   # Water Wizard with key 4
player3 = Player("Earth", (300, 100), GREEN)  # Earth Wizard with key 7

# Create spell circle
spell_circle = SpellCircle(game_progress)

# Create levels
levels = create_levels()
current_level_index = 0
current_level = levels[current_level_index]

# Spell casting keys
FIRE_CAST_KEY = pygame.K_1    # Player 1 (Fire)
WATER_CAST_KEY = pygame.K_4   # Player 2 (Water)
EARTH_CAST_KEY = pygame.K_7   # Player 3 (Earth)
# Alternate Air casting keys
FIRE_AIR_KEY = pygame.K_2     # Player 1 alternate (Air)
WATER_AIR_KEY = pygame.K_5    # Player 2 alternate (Air)
EARTH_AIR_KEY = pygame.K_8    # Player 3 alternate (Air)
# Tertiary element casting keys
FIRE_WATER_KEY = pygame.K_3   # Player 1 tertiary (Water)
WATER_EARTH_KEY = pygame.K_6  # Player 2 tertiary (Earth)
EARTH_FIRE_KEY = pygame.K_9   # Player 3 tertiary (Fire)
# Attunement keys
FIRE_ATTUNE_KEY = pygame.K_e  # Player 1 attunement
WATER_ATTUNE_KEY = pygame.K_y # Player 2 attunement
EARTH_ATTUNE_KEY = pygame.K_o # Player 3 attunement

# Movement keys
# Player 1 (Fire): WASD
P1_UP = pygame.K_w
P1_DOWN = pygame.K_s
P1_LEFT = pygame.K_a
P1_RIGHT = pygame.K_d

# Player 2 (Water): TFGH
P2_UP = pygame.K_t
P2_DOWN = pygame.K_g
P2_LEFT = pygame.K_f
P2_RIGHT = pygame.K_h

# Player 3 (Earth): IJKL
P3_UP = pygame.K_i
P3_DOWN = pygame.K_k
P3_LEFT = pygame.K_j
P3_RIGHT = pygame.K_l

# Track keys currently held down
keys_held = {
    FIRE_CAST_KEY: False,
    WATER_CAST_KEY: False,
    EARTH_CAST_KEY: False,
    FIRE_AIR_KEY: False,
    WATER_AIR_KEY: False,
    EARTH_AIR_KEY: False,
    FIRE_WATER_KEY: False,
    WATER_EARTH_KEY: False,
    EARTH_FIRE_KEY: False,
    FIRE_ATTUNE_KEY: False,
    WATER_ATTUNE_KEY: False,
    EARTH_ATTUNE_KEY: False,
    # Movement keys for Player 1
    P1_UP: False,
    P1_DOWN: False,
    P1_LEFT: False,
    P1_RIGHT: False,
    # Movement keys for Player 2
    P2_UP: False,
    P2_DOWN: False,
    P2_LEFT: False,
    P2_RIGHT: False,
    # Movement keys for Player 3
    P3_UP: False,
    P3_DOWN: False,
    P3_LEFT: False,
    P3_RIGHT: False
}

# Game states
STATE_MAIN_MENU = 0
STATE_LEVEL_TRANSITION = 1
STATE_PLAYING = 2
STATE_LEVEL_COMPLETE = 3
current_state = STATE_MAIN_MENU

# Menu state
menu_selected_option = 0
unlock_notification_timer = 0
recently_unlocked_spell = None

# Try to load sound effects
try:
    # Initialize sound effect variables with None
    cast_sound = None
    spell_sound = None
    level_complete_sound = None
    basic_spell_sound = None
    advanced_spell_sound = None
    power_spell_sound = None
    menu_sound = None

    # Load sound files if available
    cast_sound = pygame.mixer.Sound("sounds/cast.wav")
    spell_sound = pygame.mixer.Sound("sounds/spell.wav")
    level_complete_sound = pygame.mixer.Sound("sounds/level_complete.wav")
    basic_spell_sound = pygame.mixer.Sound("sounds/basic_spell.wav")
    advanced_spell_sound = pygame.mixer.Sound("sounds/advanced_spell.wav")
    power_spell_sound = pygame.mixer.Sound("sounds/power_spell.wav")
    menu_sound = pygame.mixer.Sound("sounds/menu.wav")
except:
    print("Sound files not found, continuing without sound")

def play_sound(sound):
    """Play a sound effect if available."""
    if sound is not None and pygame.mixer.get_init():
        try:
            sound.play()
        except:
            pass  # Silently ignore sound errors

def is_valid_move(player, level):
    """Check if the current player position is valid (not colliding with walls)."""
    return not level.is_position_blocked(player.position, player.size)

def handle_movement_key(key, is_down, player, direction):
    """Handle a movement key press or release for a player."""
    keys_held[key] = is_down
    player.set_velocity(direction, is_down)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle key presses
        if event.type == pygame.KEYDOWN:
            # Main Menu state
            if current_state == STATE_MAIN_MENU:
                if event.key == pygame.K_UP:
                    menu_selected_option = (menu_selected_option - 1) % 2
                    play_sound(menu_sound)
                elif event.key == pygame.K_DOWN:
                    menu_selected_option = (menu_selected_option + 1) % 2
                    play_sound(menu_sound)
                elif event.key == pygame.K_RETURN:
                    if menu_selected_option == 0:  # Start Game
                        current_state = STATE_LEVEL_TRANSITION
                        play_sound(menu_sound)
                    elif menu_selected_option == 1:  # Exit
                        running = False
            
            # Level transition state
            elif current_state == STATE_LEVEL_TRANSITION and event.key == pygame.K_SPACE:
                current_state = STATE_PLAYING
                play_sound(menu_sound)
            
            # Level complete state
            elif current_state == STATE_LEVEL_COMPLETE and event.key == pygame.K_SPACE:
                # Go to next level
                current_level_index = (current_level_index + 1) % len(levels)
                current_level = levels[current_level_index]
                current_state = STATE_LEVEL_TRANSITION
                play_sound(menu_sound)
            
            # Playing state - wizard controls - key press starts charging
            elif current_state == STATE_PLAYING:
                # Primary casting keys
                if event.key == FIRE_CAST_KEY:  # 1 key for Player 1 (Fire)
                    player1.start_cast()
                    play_sound(cast_sound)
                    keys_held[FIRE_CAST_KEY] = True
                    print("Fire Wizard charging!")
                elif event.key == WATER_CAST_KEY:  # 4 key for Player 2 (Water)
                    player2.start_cast()
                    play_sound(cast_sound)
                    keys_held[WATER_CAST_KEY] = True
                    print("Water Wizard charging!")
                elif event.key == EARTH_CAST_KEY:  # 7 key for Player 3 (Earth)
                    player3.start_cast()
                    play_sound(cast_sound)
                    keys_held[EARTH_CAST_KEY] = True
                    print("Earth Wizard charging!")
                # Air casting keys (alternate)
                elif event.key == FIRE_AIR_KEY:  # 2 key for Player 1 (Air)
                    player1.start_cast()
                    play_sound(cast_sound)
                    keys_held[FIRE_AIR_KEY] = True
                    print("Fire Wizard charging Air!")
                elif event.key == WATER_AIR_KEY:  # 5 key for Player 2 (Air)
                    player2.start_cast()
                    play_sound(cast_sound)
                    keys_held[WATER_AIR_KEY] = True
                    print("Water Wizard charging Air!")
                elif event.key == EARTH_AIR_KEY:  # 8 key for Player 3 (Air)
                    player3.start_cast()
                    play_sound(cast_sound)
                    keys_held[EARTH_AIR_KEY] = True
                    print("Earth Wizard charging Air!")
                # Tertiary element casting keys
                elif event.key == FIRE_WATER_KEY:  # 3 key for Player 1 (Water)
                    player1.start_cast("Water")
                    play_sound(cast_sound)
                    keys_held[FIRE_WATER_KEY] = True
                    print("Fire Wizard charging Water!")
                elif event.key == WATER_EARTH_KEY:  # 6 key for Player 2 (Earth)
                    player2.start_cast("Earth")
                    play_sound(cast_sound)
                    keys_held[WATER_EARTH_KEY] = True
                    print("Water Wizard charging Earth!")
                elif event.key == EARTH_FIRE_KEY:  # 9 key for Player 3 (Fire)
                    player3.start_cast("Fire")
                    play_sound(cast_sound)
                    keys_held[EARTH_FIRE_KEY] = True
                    print("Earth Wizard charging Fire!")
                # Attunement keys
                elif event.key == FIRE_ATTUNE_KEY:  # E key for Player 1 attunement
                    player1.start_attunement()
                    keys_held[FIRE_ATTUNE_KEY] = True
                    print("Fire Wizard entering attunement state!")
                elif event.key == WATER_ATTUNE_KEY:  # Y key for Player 2 attunement
                    player2.start_attunement()
                    keys_held[WATER_ATTUNE_KEY] = True
                    print("Water Wizard entering attunement state!")
                elif event.key == EARTH_ATTUNE_KEY:  # O key for Player 3 attunement
                    player3.start_attunement()
                    keys_held[EARTH_ATTUNE_KEY] = True
                    print("Earth Wizard entering attunement state!")
                # Escape key to return to menu
                elif event.key == pygame.K_ESCAPE:
                    current_state = STATE_MAIN_MENU
                    menu_selected_option = 0
                
                # Player 1 (Fire) Movement
                elif event.key == P1_UP:
                    handle_movement_key(P1_UP, True, player1, 'up')
                elif event.key == P1_DOWN:
                    handle_movement_key(P1_DOWN, True, player1, 'down')
                elif event.key == P1_LEFT:
                    handle_movement_key(P1_LEFT, True, player1, 'left')
                elif event.key == P1_RIGHT:
                    handle_movement_key(P1_RIGHT, True, player1, 'right')
                
                # Player 2 (Water) Movement
                elif event.key == P2_UP:
                    handle_movement_key(P2_UP, True, player2, 'up')
                elif event.key == P2_DOWN:
                    handle_movement_key(P2_DOWN, True, player2, 'down')
                elif event.key == P2_LEFT:
                    handle_movement_key(P2_LEFT, True, player2, 'left')
                elif event.key == P2_RIGHT:
                    handle_movement_key(P2_RIGHT, True, player2, 'right')
                
                # Player 3 (Earth) Movement
                elif event.key == P3_UP:
                    handle_movement_key(P3_UP, True, player3, 'up')
                elif event.key == P3_DOWN:
                    handle_movement_key(P3_DOWN, True, player3, 'down')
                elif event.key == P3_LEFT:
                    handle_movement_key(P3_LEFT, True, player3, 'left')
                elif event.key == P3_RIGHT:
                    handle_movement_key(P3_RIGHT, True, player3, 'right')
        
        # Handle key releases - key release completes the cast or stops movement
        elif event.type == pygame.KEYUP:
            if current_state == STATE_PLAYING:
                # Casting key releases
                if event.key == FIRE_CAST_KEY and keys_held[FIRE_CAST_KEY]:
                    charge_level = player1.stop_cast()
                    spell_circle.add_element("Fire", charge_level)
                    keys_held[FIRE_CAST_KEY] = False
                    print(f"Fire Wizard cast! Charge level: {charge_level:.1f}%")
                elif event.key == WATER_CAST_KEY and keys_held[WATER_CAST_KEY]:
                    charge_level = player2.stop_cast()
                    spell_circle.add_element("Water", charge_level)
                    keys_held[WATER_CAST_KEY] = False
                    print(f"Water Wizard cast! Charge level: {charge_level:.1f}%")
                elif event.key == EARTH_CAST_KEY and keys_held[EARTH_CAST_KEY]:
                    charge_level = player3.stop_cast()
                    spell_circle.add_element("Earth", charge_level)
                    keys_held[EARTH_CAST_KEY] = False
                    print(f"Earth Wizard cast! Charge level: {charge_level:.1f}%")
                # Air element casting key releases
                elif event.key == FIRE_AIR_KEY and keys_held[FIRE_AIR_KEY]:
                    charge_level = player1.stop_cast()
                    spell_circle.add_element("Air", charge_level)
                    keys_held[FIRE_AIR_KEY] = False
                    print(f"Fire Wizard cast Air! Charge level: {charge_level:.1f}%")
                elif event.key == WATER_AIR_KEY and keys_held[WATER_AIR_KEY]:
                    charge_level = player2.stop_cast()
                    spell_circle.add_element("Air", charge_level)
                    keys_held[WATER_AIR_KEY] = False
                    print(f"Water Wizard cast Air! Charge level: {charge_level:.1f}%")
                elif event.key == EARTH_AIR_KEY and keys_held[EARTH_AIR_KEY]:
                    charge_level = player3.stop_cast()
                    spell_circle.add_element("Air", charge_level)
                    keys_held[EARTH_AIR_KEY] = False
                    print(f"Earth Wizard cast Air! Charge level: {charge_level:.1f}%")
                # Tertiary element casting key releases
                elif event.key == FIRE_WATER_KEY and keys_held[FIRE_WATER_KEY]:
                    charge_level = player1.stop_cast()
                    spell_circle.add_element("Water", charge_level, wizard_id=id(player1))
                    keys_held[FIRE_WATER_KEY] = False
                    print(f"Fire Wizard cast Water! Charge level: {charge_level:.1f}%")
                elif event.key == WATER_EARTH_KEY and keys_held[WATER_EARTH_KEY]:
                    charge_level = player2.stop_cast()
                    spell_circle.add_element("Earth", charge_level, wizard_id=id(player2))
                    keys_held[WATER_EARTH_KEY] = False
                    print(f"Water Wizard cast Earth! Charge level: {charge_level:.1f}%")
                elif event.key == EARTH_FIRE_KEY and keys_held[EARTH_FIRE_KEY]:
                    charge_level = player3.stop_cast()
                    spell_circle.add_element("Fire", charge_level, wizard_id=id(player3))
                    keys_held[EARTH_FIRE_KEY] = False
                    print(f"Earth Wizard cast Fire! Charge level: {charge_level:.1f}%")
                # Attunement key releases
                elif event.key == FIRE_ATTUNE_KEY and keys_held[FIRE_ATTUNE_KEY]:
                    player1.stop_attunement()
                    keys_held[FIRE_ATTUNE_KEY] = False
                    print(f"Fire Wizard ended attunement state")
                elif event.key == WATER_ATTUNE_KEY and keys_held[WATER_ATTUNE_KEY]:
                    player2.stop_attunement()
                    keys_held[WATER_ATTUNE_KEY] = False
                    print(f"Water Wizard ended attunement state")
                elif event.key == EARTH_ATTUNE_KEY and keys_held[EARTH_ATTUNE_KEY]:
                    player3.stop_attunement()
                    keys_held[EARTH_ATTUNE_KEY] = False
                    print(f"Earth Wizard ended attunement state")
                
                # Player 1 (Fire) Movement stops
                elif event.key == P1_UP:
                    handle_movement_key(P1_UP, False, player1, 'up')
                elif event.key == P1_DOWN:
                    handle_movement_key(P1_DOWN, False, player1, 'down')
                elif event.key == P1_LEFT:
                    handle_movement_key(P1_LEFT, False, player1, 'left')
                elif event.key == P1_RIGHT:
                    handle_movement_key(P1_RIGHT, False, player1, 'right')
                
                # Player 2 (Water) Movement stops
                elif event.key == P2_UP:
                    handle_movement_key(P2_UP, False, player2, 'up')
                elif event.key == P2_DOWN:
                    handle_movement_key(P2_DOWN, False, player2, 'down')
                elif event.key == P2_LEFT:
                    handle_movement_key(P2_LEFT, False, player2, 'left')
                elif event.key == P2_RIGHT:
                    handle_movement_key(P2_RIGHT, False, player2, 'right')
                
                # Player 3 (Earth) Movement stops
                elif event.key == P3_UP:
                    handle_movement_key(P3_UP, False, player3, 'up')
                elif event.key == P3_DOWN:
                    handle_movement_key(P3_DOWN, False, player3, 'down')
                elif event.key == P3_LEFT:
                    handle_movement_key(P3_LEFT, False, player3, 'left')
                elif event.key == P3_RIGHT:
                    handle_movement_key(P3_RIGHT, False, player3, 'right')

    # Update the game state
    if current_state == STATE_PLAYING:
        # Make sure players are assigned to the level
        current_level.players = [player1, player2, player3]
        
        # Check for attunement between wizards
        if keys_held[FIRE_ATTUNE_KEY] and keys_held[WATER_ATTUNE_KEY]:
            # Fire and Water attunement
            player1.attune_with(id(player2))
            player2.attune_with(id(player1))
            print("Fire and Water wizards are attuned!")
        
        if keys_held[WATER_ATTUNE_KEY] and keys_held[EARTH_ATTUNE_KEY]:
            # Water and Earth attunement
            player2.attune_with(id(player3))
            player3.attune_with(id(player2))
            print("Water and Earth wizards are attuned!")
        
        if keys_held[FIRE_ATTUNE_KEY] and keys_held[EARTH_ATTUNE_KEY]:
            # Fire and Earth attunement
            player1.attune_with(id(player3))
            player3.attune_with(id(player1))
            print("Fire and Earth wizards are attuned!")
        
        # Keep players within screen bounds
        player1.keep_in_bounds(SCREEN_WIDTH, SCREEN_HEIGHT)
        player2.keep_in_bounds(SCREEN_WIDTH, SCREEN_HEIGHT)
        player3.keep_in_bounds(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Update all game objects
        player1.update()
        player2.update()
        player3.update()
        
        # Update the spell circle
        spell_result = spell_circle.update()
        
        # If a spell was activated, update the level with the spell effect
        if spell_result:
            spell_name, spell_power = spell_result
            print(f"Spell activated: {spell_name} ({spell_power:.1f}% power)")
            
            # Play a sound for the spell
            if spell_name in ['Steam', 'Lava', 'Mud']:
                play_sound(basic_spell_sound)
            elif spell_name in ['Storm', 'Breeze', 'Sandstorm', 'Typhoon']:
                play_sound(advanced_spell_sound)
            elif spell_name in ['Teleport', 'Barrier']:
                play_sound(advanced_spell_sound)
            elif spell_name in ['Fireball', 'Tidal Wave', 'Earthquake', 'Tornado']:
                play_sound(power_spell_sound)
            
            # Update the level with the spell effect
            if current_level.update(spell_name, spell_power):
                # Level was completed!
                transition_time = 0
                current_state = STATE_LEVEL_COMPLETE
                play_sound(level_complete_sound)
            
            # Update game progress
            spell_unlocked = game_progress.complete_level(current_level_index)
            if spell_unlocked:
                # Get the newly unlocked spell for notification
                recently_unlocked_spell = game_progress.get_new_unlocks()[0]
                unlock_notification_timer = 180  # Show for 3 seconds
    
    # Update unlock notification timer
    if unlock_notification_timer > 0:
        unlock_notification_timer -= 1
        if unlock_notification_timer == 0:
            recently_unlocked_spell = None

    # Render
    screen.fill(BLACK)
    
    if current_state == STATE_MAIN_MENU:
        # Draw the main menu
        rendering.draw_main_menu(screen, menu_selected_option)
    
    elif current_state == STATE_LEVEL_TRANSITION:
        # Draw level transition screen
        rendering.draw_level_transition(screen, current_level_index + 1, len(levels))
    
    elif current_state == STATE_PLAYING or current_state == STATE_LEVEL_COMPLETE:
        # Draw the level elements
        rendering.draw_level(screen, current_level)
        
        # Draw the three wizards
        rendering.draw_player(screen, player1)
        rendering.draw_player(screen, player2)
        rendering.draw_player(screen, player3)
        
        # Draw the objective panel (new UI element)
        rendering.draw_objective_panel(screen, current_level)
        
        # Draw the spell circle
        rendering.draw_spell_circle(screen, spell_circle)
        
        # Draw any active spell effects
        rendering.draw_spell_effect(screen, spell_circle)
        
        # If level complete, draw a message
        if current_state == STATE_LEVEL_COMPLETE:
            font = pygame.font.SysFont(None, 72)
            complete_text = font.render("Level Complete!", True, (255, 255, 255))
            screen.blit(complete_text, (SCREEN_WIDTH//2 - complete_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            
            font = pygame.font.SysFont(None, 36)
            next_text = font.render("Press SPACE for next level", True, (200, 200, 200))
            screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, SCREEN_HEIGHT//2 + 30))
    
    # Draw unlock notification if active
    if recently_unlocked_spell and unlock_notification_timer > 0:
        rendering.draw_unlocked_spell(screen, recently_unlocked_spell)
    
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()