import pygame
import os

# Initialize pygame
pygame.init()

def create_wizard_sprite(color, size=50):
    """Create a simple wizard sprite in the given color.
    
    Args:
        color: RGB tuple for the wizard's main color
        size: Size of the sprite in pixels
        
    Returns:
        A pygame Surface with the wizard sprite
    """
    # Create a surface with alpha channel
    surface = pygame.Surface((size, size + 20), pygame.SRCALPHA)
    
    # Calculate colors for shading
    hat_color = tuple(min(c + 20, 255) for c in color)
    robe_color = color
    dark_color = tuple(max(c - 40, 0) for c in color)
    
    # Draw wizard body/robe (rounded rectangle)
    pygame.draw.rect(surface, robe_color, (0, size//3, size, size*2//3), border_radius=5)
    
    # Draw wizard hat (triangle)
    hat_points = [(size//2, 0), (size//5, size//3), (size*4//5, size//3)]
    pygame.draw.polygon(surface, hat_color, hat_points)
    
    # Draw hat brim
    pygame.draw.line(surface, dark_color, (size//6, size//3), (size*5//6, size//3), 3)
    
    # Draw wizard face (circle)
    face_center = (size//2, size//2)
    face_radius = size//5
    pygame.draw.circle(surface, (255, 220, 177), face_center, face_radius)
    
    # Draw eyes
    eye_size = size//12
    pygame.draw.circle(surface, (50, 50, 50), (face_center[0] - face_radius//2, face_center[1]), eye_size)
    pygame.draw.circle(surface, (50, 50, 50), (face_center[0] + face_radius//2, face_center[1]), eye_size)
    
    # Draw beard
    beard_points = [
        (face_center[0] - face_radius, face_center[1] + face_radius//2),
        (face_center[0], face_center[1] + face_radius * 2),
        (face_center[0] + face_radius, face_center[1] + face_radius//2)
    ]
    pygame.draw.polygon(surface, (200, 200, 200), beard_points)
    
    return surface

def create_wizard_sprites():
    """Create and save sprites for all three wizards."""
    # Define colors
    colors = {
        'fire': (255, 0, 0),     # Red
        'water': (0, 0, 255),    # Blue
        'earth': (0, 255, 0)     # Green
    }
    
    # Create sprites directory
    sprites_dir = os.path.dirname(os.path.abspath(__file__)) + '/images'
    os.makedirs(sprites_dir, exist_ok=True)
    
    # Create and save each wizard sprite
    for name, color in colors.items():
        sprite = create_wizard_sprite(color)
        
        # Also create a casting version (brighter)
        casting_color = tuple(min(c + 100, 255) for c in color)
        casting_sprite = create_wizard_sprite(casting_color)
        
        # Save sprites
        try:
            pygame.image.save(sprite, f"{sprites_dir}/{name}_wizard.png")
            pygame.image.save(casting_sprite, f"{sprites_dir}/{name}_wizard_casting.png")
            print(f"Saved {name} wizard sprites")
        except Exception as e:
            print(f"Error saving {name} wizard sprite: {e}")

if __name__ == "__main__":
    create_wizard_sprites()
    print("Wizard sprites generation complete.")
    pygame.quit() 