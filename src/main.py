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
player1 = Player("Fire", (100, 100), RED)     # Fire Wizard with W key
player2 = Player("Water", (200, 100), BLUE)   # Water Wizard with T key
player3 = Player("Earth", (300, 100), GREEN)  # Earth Wizard with I key

# Create spell circle
spell_circle = SpellCircle(game_progress)

# Create levels
levels = create_levels()
current_level_index = 0
current_level = levels[current_level_index]

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

# Simple sound effects (we'll initialize these as None and create them when needed)
try:
    cast_sound = pygame.mixer.Sound('src/assets/sounds/cast.wav')
    spell_sound = pygame.mixer.Sound('src/assets/sounds/spell.wav')
    menu_sound = pygame.mixer.Sound('src/assets/sounds/menu.wav')
    level_complete_sound = pygame.mixer.Sound('src/assets/sounds/complete.wav')
except:
    # If sound files don't exist, we'll just print messages instead
    cast_sound = None
    spell_sound = None
    menu_sound = None
    level_complete_sound = None
    print("Sound files not found, continuing without sound")

def play_sound(sound):
    """Play a sound if it exists."""
    if sound:
        sound.play()

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
            
            # Playing state - wizard controls
            elif current_state == STATE_PLAYING:
                if event.key == pygame.K_w:  # W key for Player 1 (Fire)
                    player1.start_cast()
                    spell_circle.add_element("Fire")
                    play_sound(cast_sound)
                    print("Fire Wizard casting!")
                elif event.key == pygame.K_t:  # T key for Player 2 (Water)
                    player2.start_cast()
                    spell_circle.add_element("Water")
                    play_sound(cast_sound)
                    print("Water Wizard casting!")
                elif event.key == pygame.K_i:  # I key for Player 3 (Earth)
                    player3.start_cast()
                    spell_circle.add_element("Earth")
                    play_sound(cast_sound)
                    print("Earth Wizard casting!")
                # Escape key to return to menu
                elif event.key == pygame.K_ESCAPE:
                    current_state = STATE_MAIN_MENU
                    menu_selected_option = 0

    # Update game state based on current game state
    if current_state == STATE_PLAYING:
        # Update players
        player1.update()
        player2.update()
        player3.update()
        
        # Update spell circle and check for spell activation
        activated_spell = spell_circle.update()
        if activated_spell:
            play_sound(spell_sound)
            print(f"SPELL ACTIVATED: {activated_spell}")
        
        # Update level and check for completion
        level_changed = current_level.update(spell_circle.active_spell)
        
        # If level is completed, change state
        if current_level.is_completed:
            current_state = STATE_LEVEL_COMPLETE
            play_sound(level_complete_sound)
            print(f"Level {current_level_index + 1} completed!")
            
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
        
        # Draw the spell circle
        rendering.draw_spell_circle(screen, spell_circle)
        
        # Draw any active spell effects
        rendering.draw_spell_effect(screen, spell_circle)
        
        # Draw level text
        rendering.draw_level_text(screen, current_level)
        
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