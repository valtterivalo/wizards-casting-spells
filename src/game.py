import pygame

class Player:
    """
    Represents a wizard player in the game.
    
    Attributes:
        element (str): The wizard's element ('Fire', 'Water', or 'Earth')
        position (tuple): (x, y) coordinates of the wizard
        color (tuple): RGB color value representing the wizard
        is_casting (bool): Whether the wizard is currently casting a spell
        cast_time (int): Timer for how long the wizard has been casting
        charge_level (float): Current spell charge level (0-100)
        max_charge_time (int): Maximum time to reach 100% charge (in frames)
        is_overcharged (bool): Whether the spell is overcharged (held too long)
        velocity (tuple): (x, y) velocity vector for movement
        move_speed (float): Base movement speed in pixels per frame
        size (int): Size of the wizard for collision detection
        casting_element (str): The element currently being cast
        is_attuned (bool): Whether the wizard is in attunement state
        attuned_wizards (list): List of wizard IDs this wizard is attuned with
    """
    
    def __init__(self, element, position, color):
        """
        Initialize a new player wizard.
        
        Args:
            element (str): 'Fire', 'Water', or 'Earth'
            position (tuple): Starting (x, y) position
            color (tuple): RGB color value
        """
        self.element = element
        self.position = position
        self.color = color
        self.is_casting = False
        self.cast_time = 0
        self.charge_level = 0
        self.max_charge_time = 120  # 2 seconds at 60 FPS
        self.is_overcharged = False
        self.velocity = (0, 0)  # (x, y) velocity vector
        self.move_speed = 3.0    # Base movement speed (pixels per frame)
        self.size = 50          # Size for collision detection
        self.casting_element = None  # Element currently being cast
        self.is_attuned = False  # Attunement state
        self.attuned_wizards = []  # List of wizard IDs this wizard is attuned with
        
    def start_cast(self, element=None):
        """
        Start charging a spell element.
        
        Args:
            element (str, optional): The element to cast. If None, uses the wizard's primary element.
        """
        self.is_casting = True
        self.cast_time = 0
        self.charge_level = 0
        self.is_overcharged = False
        
        # Set the casting element (default to primary)
        if element is None:
            self.casting_element = self.element
        else:
            self.casting_element = element
        
    def stop_cast(self):
        """
        Stop casting and return the current charge level.
        
        Returns:
            float: The final charge level (0-100)
        """
        final_charge = self.charge_level
        if self.is_overcharged:
            # Penalty for overcharging - reduce to 50%
            final_charge = 50
            
        self.is_casting = False
        element_cast = self.casting_element
        self.casting_element = None
        return final_charge
        
    def start_attunement(self):
        """
        Start attuning with other wizards.
        """
        self.is_attuned = True
        print(f"{self.element} Wizard is now attuned and can boost other wizards.")
        
    def stop_attunement(self):
        """
        Stop attuning with other wizards.
        """
        self.is_attuned = False
        self.attuned_wizards = []
        
    def attune_with(self, wizard_id):
        """
        Attune with another wizard to boost their casting.
        
        Args:
            wizard_id: Unique identifier of the wizard to attune with
        """
        if self.is_attuned and wizard_id not in self.attuned_wizards:
            self.attuned_wizards.append(wizard_id)
            return True
        return False
        
    def set_velocity(self, direction, is_moving):
        """
        Set the velocity in a given direction.
        
        Args:
            direction (str): 'up', 'down', 'left', or 'right'
            is_moving (bool): Whether to start or stop moving in that direction
        """
        # Get current x, y velocity
        vx, vy = self.velocity
        
        # Update velocity based on direction
        if direction == 'up':
            vy = -self.move_speed if is_moving else 0
        elif direction == 'down':
            vy = self.move_speed if is_moving else 0
        elif direction == 'left':
            vx = -self.move_speed if is_moving else 0
        elif direction == 'right':
            vx = self.move_speed if is_moving else 0
            
        # Set the new velocity
        self.velocity = (vx, vy)
        
    def update(self):
        """
        Update the player's state. Advances the cast timer and charge level, and handles movement.
        """
        if self.is_casting:
            self.cast_time += 1
            
            # Calculate charge level (0-100) based on element affinity
            charge_rate_multiplier = self._get_charge_rate_multiplier()
            
            # Calculate charge level with the multiplier
            self.charge_level = min(100, (self.cast_time / (self.max_charge_time * charge_rate_multiplier)) * 100)
            
            # Check for overcharge
            if self.cast_time > self.max_charge_time * charge_rate_multiplier:
                self.is_overcharged = True
        
        # Update position based on velocity
        x, y = self.position
        vx, vy = self.velocity
        
        # Store original position in case we need to revert
        self.prev_position = (x, y)
        
        # Update position
        self.position = (x + vx, y + vy)
        
    def _get_charge_rate_multiplier(self):
        """
        Get the charge rate multiplier based on element affinity.
        Returns:
            float: Multiplier for charge rate (1.0 = normal, >1.0 = slower)
        """
        # Default is 1.0 (normal speed)
        multiplier = 1.0
        
        # Primary element is fastest
        if self.casting_element == self.element:
            multiplier = 1.0
        # Air is shared by all, but still slightly slower
        elif self.casting_element == "Air":
            multiplier = 1.2
        # Tertiary elements are much slower
        else:
            multiplier = 1.8
            
        return multiplier
        
    def collides_with(self, other_obj):
        """
        Check if this player collides with another object.
        
        Args:
            other_obj: An object with position and size attributes
            
        Returns:
            bool: True if there's a collision
        """
        # Simple AABB collision
        x1, y1 = self.position
        x2, y2 = other_obj['position']
        
        # Make sure width/height are defined
        w1, h1 = self.size, self.size
        w2, h2 = other_obj.get('size', (50, 50))
        
        # If size is a tuple, unpack it
        if isinstance(w2, tuple):
            w2, h2 = w2
            
        # Check for intersection
        return (
            x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2
        )
    
    def keep_in_bounds(self, screen_width, screen_height):
        """
        Keep the player within the screen bounds.
        
        Args:
            screen_width (int): Width of the screen
            screen_height (int): Height of the screen
        """
        x, y = self.position
        
        # Constrain X position
        x = max(0, min(screen_width - self.size, x))
        
        # Constrain Y position
        y = max(0, min(screen_height - self.size, y))
        
        self.position = (x, y)
                
    def get_display_color(self):
        """
        Get the color to display the wizard. If casting, returns a brighter color.
        If attuned, returns a glowing effect.
        
        Returns:
            tuple: RGB color value
        """
        if self.is_casting:
            if self.is_overcharged:
                # Pulsing red for overcharge
                pulse = abs(((self.cast_time % 20) - 10) / 10)
                return (255, 50 + int(pulse * 50), 50)
            else:
                # Make a brighter version of the color based on charge level
                brightness = min(100, int(self.charge_level))
                return tuple(min(c + brightness, 255) for c in self.color)
        elif self.is_attuned:
            # Pulsing white glow for attunement
            pulse = abs(((pygame.time.get_ticks() % 1000) - 500) / 500)
            return tuple(min(c + int(pulse * 100), 255) for c in self.color)
        
        return self.color

class GameProgress:
    """
    Tracks overall game progress including unlocked spells and completed levels.
    
    Attributes:
        completed_levels (list): List of indices of completed levels
        unlocked_spells (list): List of spell names that have been unlocked
        new_unlocks (list): List of newly unlocked spells (for notifications)
    """
    
    def __init__(self):
        """Initialize game progress with default unlocks."""
        self.completed_levels = []
        # Start with only the basic two-element spells unlocked
        self.unlocked_spells = ['Steam', 'Lava', 'Mud']  
        self.new_unlocks = []
        
    def complete_level(self, level_index):
        """
        Mark a level as completed and possibly unlock new spells.
        
        Args:
            level_index (int): Index of the completed level
            
        Returns:
            bool: True if a new spell was unlocked
        """
        # If level already completed, do nothing
        if level_index in self.completed_levels:
            return False
        
        # Mark level as completed
        self.completed_levels.append(level_index)
        
        # Unlock new spells based on progress
        spell_unlocked = False
        
        # Unlock Storm spell after completing all three levels
        if len(self.completed_levels) >= 3:
            # Unlock Storm spell
            if 'Storm' not in self.unlocked_spells:
                self.unlocked_spells.append('Storm')
                self.new_unlocks.append('Storm')
                spell_unlocked = True
            
            # Unlock Air element and its basic combinations
            if 'Breeze' not in self.unlocked_spells:
                self.unlocked_spells.extend(['Breeze', 'Sandstorm', 'Typhoon'])
                self.new_unlocks.extend(['Breeze', 'Sandstorm', 'Typhoon'])
                spell_unlocked = True
                
            # Unlock multi-cast spells
            if 'Fireball' not in self.unlocked_spells:
                self.unlocked_spells.extend(['Fireball', 'Tidal Wave', 'Earthquake', 'Tornado'])
                self.new_unlocks.extend(['Fireball', 'Tidal Wave', 'Earthquake', 'Tornado'])
                spell_unlocked = True
            
        return spell_unlocked
    
    def is_spell_unlocked(self, spell_name):
        """
        Check if a spell is unlocked.
        
        Args:
            spell_name (str): Name of the spell to check
            
        Returns:
            bool: True if spell is unlocked
        """
        return spell_name in self.unlocked_spells
    
    def get_new_unlocks(self):
        """
        Get list of newly unlocked spells and clear the list.
        
        Returns:
            list: List of newly unlocked spell names
        """
        unlocks = list(self.new_unlocks)
        self.new_unlocks = []
        return unlocks

class SpellCircle:
    """
    Tracks spell elements contributed by players and handles spell activation.
    
    Attributes:
        elements (list): List of elements currently in the spell circle
        element_charges (list): List of charge levels corresponding to each element
        activation_timer (int): Countdown timer for spell activation
        active_spell (str): Currently active spell, if any
        active_spell_power (float): Power level of the active spell (0-100)
        spell_effect_timer (int): Timer for how long a spell effect is shown
        game_progress (GameProgress): Reference to the game progress tracker
        target_position (tuple): Mouse cursor position for targeted spell casting
    """
    
    def __init__(self, game_progress=None):
        """
        Initialize a new spell circle.
        
        Args:
            game_progress (GameProgress, optional): Game progress tracker
        """
        self.elements = []
        self.element_charges = []
        self.activation_timer = 0
        self.active_spell = None
        self.active_spell_power = 0
        self.spell_effect_timer = 0
        self.game_progress = game_progress
        self.target_position = (400, 300)  # Default to center of screen
        
    def add_element(self, element, charge_level=100, wizard_id=None):
        """
        Add an element to the spell circle.
        
        Args:
            element (str): Element to add ('Fire', 'Water', 'Earth', or 'Air')
            charge_level (float): The charge level of the element (0-100)
            wizard_id: Unique identifier of the wizard casting the element
        """
        # Check for resonance (same element already in circle)
        resonance_bonus = 1.0
        if element in self.elements:
            # If the same element exists, apply resonance bonus
            resonance_bonus = 1.5
            print(f"Resonance bonus applied for {element}!")
            
        # Apply charge level with resonance bonus
        boosted_charge = min(100, charge_level * resonance_bonus)
        
        # Only add the element if it's not already in the circle
        if element not in self.elements:
            self.elements.append(element)
            self.element_charges.append(boosted_charge)
        else:
            # Update the charge level for the existing element
            index = self.elements.index(element)
            self.element_charges[index] = boosted_charge
            
        # Reset the activation timer (2 seconds at 60 FPS = 120 frames)
        self.activation_timer = 120
        
    def set_target_position(self, position):
        """
        Set the target position for the spell (from mouse cursor).
        
        Args:
            position (tuple): (x, y) coordinates for spell targeting
        """
        self.target_position = position
        
    def update(self):
        """
        Update the spell circle state, checking for spell activation.
        
        Returns:
            tuple or None: (spell_name, spell_power, target_position) if a new spell activates, or None
        """
        # If a spell is currently active, update its effect timer
        if self.active_spell:
            self.spell_effect_timer -= 1
            if self.spell_effect_timer <= 0:
                self.active_spell = None
                self.active_spell_power = 0
                return None
            
        # If there are elements in the circle, count down the timer
        if self.elements and self.activation_timer > 0:
            self.activation_timer -= 1
            
            # If the timer runs out or we have all three elements, try to activate a spell
            if self.activation_timer == 0 or len(self.elements) == 3:
                spell_result = self._check_spell_combination()
                if spell_result:
                    spell_name, spell_power = spell_result
                    # Check if the spell is unlocked
                    if not self.game_progress or self.game_progress.is_spell_unlocked(spell_name):
                        self.active_spell = spell_name
                        self.active_spell_power = spell_power
                        self.spell_effect_timer = 180  # 3 seconds at 60 FPS
                        self.elements = []  # Clear the elements after casting
                        self.element_charges = []  # Clear charges too
                        return (spell_name, spell_power, self.target_position)
                    else:
                        # If spell is not unlocked, show a visual cue
                        print(f"Spell {spell_name} is not unlocked yet!")
                
                # Clear the elements if no valid combo or spell not unlocked
                self.elements = []
                self.element_charges = []
        
        return None
    
    def _check_spell_combination(self):
        """
        Check if the current elements form a valid spell combination.
        
        Returns:
            tuple or None: (spell_name, spell_power) if valid, None otherwise
        """
        # Calculate average charge level
        if not self.elements:
            return None
            
        avg_charge = sum(self.element_charges) / len(self.element_charges)
        
        # Get sorted elements for consistent checking
        elements_with_charges = list(zip(self.elements, self.element_charges))
        sorted_pairs = sorted(elements_with_charges, key=lambda pair: pair[0])
        sorted_elements = [pair[0] for pair in sorted_pairs]
        
        # Count occurrences of each element
        element_counts = {}
        for element in sorted_elements:
            if element in element_counts:
                element_counts[element] += 1
            else:
                element_counts[element] = 1
        
        # Check for multi-cast spells (same element twice or more)
        if len(sorted_elements) >= 2:
            # Fire + Fire = Fireball
            if element_counts.get('Fire', 0) >= 2:
                return ('Fireball', avg_charge * 1.5)  # Boosted power
            
            # Water + Water = Tidal Wave
            if element_counts.get('Water', 0) >= 2:
                return ('Tidal Wave', avg_charge * 1.5)
            
            # Earth + Earth = Earthquake
            if element_counts.get('Earth', 0) >= 2:
                return ('Earthquake', avg_charge * 1.5)
            
            # Air + Air = Tornado
            if element_counts.get('Air', 0) >= 2:
                return ('Tornado', avg_charge * 1.5)
        
        # Check for unique element combinations (original spells)
        unique_elements = set(sorted_elements)
        
        # Two-element combinations
        if len(unique_elements) == 2:
            if 'Earth' in unique_elements and 'Fire' in unique_elements:
                return ('Lava', avg_charge)
            elif 'Fire' in unique_elements and 'Water' in unique_elements:
                return ('Steam', avg_charge)
            elif 'Earth' in unique_elements and 'Water' in unique_elements:
                return ('Mud', avg_charge)
            elif 'Air' in unique_elements and 'Fire' in unique_elements:
                return ('Breeze', avg_charge)
            elif 'Air' in unique_elements and 'Earth' in unique_elements:
                return ('Sandstorm', avg_charge)
            elif 'Air' in unique_elements and 'Water' in unique_elements:
                return ('Typhoon', avg_charge)
            # New spell combination for teleportation
            elif 'Air' in unique_elements and 'Fire' in unique_elements and element_counts.get('Air', 0) >= 1 and element_counts.get('Fire', 0) >= 2:
                return ('Teleport', avg_charge)
            # New spell combination for barrier
            elif 'Water' in unique_elements and 'Earth' in unique_elements and element_counts.get('Water', 0) >= 2 and element_counts.get('Earth', 0) >= 1:
                return ('Barrier', avg_charge)
            
        # Three-element combinations
        elif len(unique_elements) == 3:
            if 'Earth' in unique_elements and 'Fire' in unique_elements and 'Water' in unique_elements:
                return ('Storm', avg_charge)
            if 'Air' in unique_elements and 'Fire' in unique_elements and 'Water' in unique_elements:
                return ('Inferno', avg_charge * 1.8)
            if 'Air' in unique_elements and 'Earth' in unique_elements and 'Water' in unique_elements:
                return ('Tsunami', avg_charge * 1.8)
            if 'Air' in unique_elements and 'Earth' in unique_elements and 'Fire' in unique_elements:
                return ('Volcano', avg_charge * 1.8)
        
        # Four-element combinations
        elif len(unique_elements) == 4:
            return ('Cataclysm', avg_charge * 2.0)  # Ultimate spell with all elements
            
        return None

class Level:
    """
    Represents a game level with objectives and elements.
    
    Attributes:
        name (str): The name of the level
        level_type (str): Type of level ('puzzle', 'combat', or 'survival')
        objective (str): Description of what the player needs to do
        target_spell (str): The spell needed to complete the objective (if applicable)
        elements (list): List of level elements like enemies or obstacles
        is_completed (bool): Whether the level has been completed
        timer (int): For survival levels, counts down time remaining
        enemy_spawn_timer (int): For combat/survival levels, timer for spawning enemies
    """
    
    def __init__(self, name, level_type, objective, target_spell=None):
        """
        Initialize a new level.
        
        Args:
            name (str): Level name
            level_type (str): 'puzzle', 'combat', or 'survival'
            objective (str): Text description of the objective
            target_spell (str, optional): Spell needed to complete the objective
        """
        self.name = name
        self.level_type = level_type
        self.objective = objective
        self.target_spell = target_spell
        self.elements = []
        self.is_completed = False
        self.timer = 0
        self.enemy_spawn_timer = 0
        self.players = []  # Initialize empty players list
        
        # Set up level elements based on type
        if level_type == 'puzzle':
            # For puzzle levels, add obstacles or targets
            self._setup_puzzle()
        elif level_type == 'combat':
            # For combat levels, add enemies
            self._setup_combat()
        elif level_type == 'survival':
            # For survival levels, add timer and enemies
            self._setup_survival()
    
    def _setup_puzzle(self):
        """Set up elements for a puzzle level."""
        # Add a gap in the middle that needs to be filled
        self.elements.append({
            'type': 'gap',
            'position': (400, 300),
            'size': (150, 50)
        })
        
        # Add some walls to create a more interesting layout
        self.elements.append({
            'type': 'wall',
            'position': (200, 200),
            'size': (30, 200)
        })
        
        self.elements.append({
            'type': 'wall',
            'position': (600, 200),
            'size': (30, 200)
        })
    
    def _setup_combat(self):
        """Set up elements for a combat level."""
        # Add some enemies
        for i in range(3):
            self.elements.append({
                'type': 'enemy',
                'position': (600, 150 + i * 120),
                'health': 100,
                'speed': 1
            })
        
        # Add obstacles for strategic positioning
        self.elements.append({
            'type': 'wall',
            'position': (400, 150),
            'size': (50, 50)
        })
        
        self.elements.append({
            'type': 'wall',
            'position': (400, 400),
            'size': (50, 50)
        })
        
        self.enemy_spawn_timer = 300  # 5 seconds at 60 FPS
    
    def _setup_survival(self):
        """Set up elements for a survival level."""
        # Set survival timer (30 seconds at 60 FPS)
        self.timer = 30 * 60
        
        # Add some initial enemies
        for i in range(2):
            self.elements.append({
                'type': 'enemy',
                'position': (600, 200 + i * 200),
                'health': 100,
                'speed': 2
            })
        
        # Add protective barriers players can hide behind
        self.elements.append({
            'type': 'wall',
            'position': (200, 150),
            'size': (80, 20)
        })
        
        self.elements.append({
            'type': 'wall',
            'position': (200, 350),
            'size': (80, 20)
        })
        
        self.elements.append({
            'type': 'wall',
            'position': (350, 250),
            'size': (20, 100)
        })
        
        self.enemy_spawn_timer = 180  # 3 seconds at 60 FPS
    
    def is_position_blocked(self, position, size):
        """
        Check if a position is blocked by any obstacle.
        
        Args:
            position (tuple): (x, y) position to check
            size (int or tuple): Size of the object
            
        Returns:
            bool: True if the position is blocked
        """
        # Create a test object
        test_obj = {
            'position': position,
            'size': size
        }
        
        # Check collision with each wall element
        for elem in self.elements:
            if elem['type'] == 'wall':
                # Simple AABB collision check
                x1, y1 = test_obj['position']
                x2, y2 = elem['position']
                
                # Check size format
                w1, h1 = test_obj['size'] if isinstance(test_obj['size'], tuple) else (test_obj['size'], test_obj['size'])
                w2, h2 = elem['size']
                
                # Check for collision
                if (x1 < x2 + w2 and
                    x1 + w1 > x2 and
                    y1 < y2 + h2 and
                    y1 + h1 > y2):
                    return True
                    
        # Also check screen boundaries
        x, y = position
        w, h = size if isinstance(size, tuple) else (size, size)
        
        if x < 0 or y < 0 or x + w > 800 or y + h > 600:
            return True
            
        return False
    
    def update(self, active_spell=None, spell_power=100, target_position=None):
        """
        Update the level state based on elapsed time and player actions.
        
        Args:
            active_spell (str or None): The currently active spell
            spell_power (float): The power level of the active spell (0-100)
            target_position (tuple): The (x, y) position to target the spell effect
            
        Returns:
            bool: True if level state changed (completed, enemy died, etc.)
        """
        # Use center of screen if no target position provided
        if target_position is None:
            target_position = (400, 300)
            
        state_changed = False
        
        # Calculate power multiplier (0.5 - 1.5 based on spell power)
        power_multiplier = 0.5 + (spell_power / 100)
        
        # Check for level completion
        if not self.is_completed:
            if self.level_type == 'puzzle' and active_spell == self.target_spell:
                # In puzzle levels, casting the target spell completes the level
                # For puzzles, we might require a minimum power level
                if spell_power >= 60:  # At least 60% charge required
                    self.is_completed = True
                    state_changed = True
                else:
                    # Not enough power - show some feedback in the console
                    print(f"Spell not powerful enough ({spell_power:.1f}%). Need at least 60%.")
            
            elif self.level_type == 'combat':
                # In combat levels, check if all enemies are defeated
                if not any(elem['type'] == 'enemy' for elem in self.elements):
                    self.is_completed = True
                    state_changed = True
                
                # Update enemy spawn timer
                self.enemy_spawn_timer -= 1
                if self.enemy_spawn_timer <= 0 and len([e for e in self.elements if e['type'] == 'enemy']) < 5:
                    # Spawn a new enemy
                    import random
                    self.elements.append({
                        'type': 'enemy',
                        'position': (random.randint(500, 700), random.randint(100, 500)),
                        'health': 100,
                        'speed': 1
                    })
                    self.enemy_spawn_timer = 300  # Reset timer
                    state_changed = True
                
                # Check for spell damage to enemies - scale damage by spell power
                if active_spell == 'Lava':
                    # Lava damages enemies (base damage scaled by power)
                    damage = 2 * power_multiplier
                    # Get the spell's area of effect radius based on power
                    aoe_radius = 100 * power_multiplier
                    
                    for elem in self.elements:
                        if elem['type'] == 'enemy':
                            # Calculate distance from spell target to enemy
                            enemy_x, enemy_y = elem['position']
                            import math
                            distance = math.sqrt((enemy_x - target_position[0])**2 + (enemy_y - target_position[1])**2)
                            
                            # Only affect enemies within the area of effect
                            if distance <= aoe_radius:
                                # Apply damage with distance falloff (more damage closer to center)
                                falloff = 1 - (distance / aoe_radius)
                                actual_damage = damage * falloff
                                elem['health'] -= actual_damage
                                if elem['health'] <= 0:
                                    self.elements.remove(elem)
                                    state_changed = True
                
                elif active_spell == 'Steam':
                    # Steam slows enemies (slow effect scaled by power)
                    slow_factor = 0.4 * power_multiplier
                    # Get the spell's area of effect radius
                    aoe_radius = 120 * power_multiplier
                    
                    for elem in self.elements:
                        if elem['type'] == 'enemy':
                            # Calculate distance from spell target to enemy
                            enemy_x, enemy_y = elem['position']
                            import math
                            distance = math.sqrt((enemy_x - target_position[0])**2 + (enemy_y - target_position[1])**2)
                            
                            # Only affect enemies within the area of effect
                            if distance <= aoe_radius:
                                # Apply slow effect with distance falloff
                                falloff = 1 - (distance / aoe_radius)
                                elem['speed'] = max(0.2, elem['speed'] - (slow_factor * falloff))
                
                elif active_spell == 'Mud':
                    # Mud slows and damages enemies
                    damage = 1 * power_multiplier
                    slow_factor = 0.3 * power_multiplier
                    # Get the spell's area of effect radius
                    aoe_radius = 110 * power_multiplier
                    
                    for elem in self.elements:
                        if elem['type'] == 'enemy':
                            # Calculate distance from spell target to enemy
                            enemy_x, enemy_y = elem['position']
                            import math
                            distance = math.sqrt((enemy_x - target_position[0])**2 + (enemy_y - target_position[1])**2)
                            
                            # Only affect enemies within the area of effect
                            if distance <= aoe_radius:
                                # Apply effects with distance falloff
                                falloff = 1 - (distance / aoe_radius)
                                elem['health'] -= damage * falloff
                                elem['speed'] = max(0.1, elem['speed'] - (slow_factor * falloff))
                                if elem['health'] <= 0:
                                    self.elements.remove(elem)
                                    state_changed = True
                
                elif active_spell == 'Storm':
                    # Storm damages all enemies at once (powerful combo spell)
                    damage = 5 * power_multiplier
                    # Larger area of effect for this powerful spell
                    aoe_radius = 200 * power_multiplier
                    
                    enemies_to_remove = []
                    for i, elem in enumerate(self.elements):
                        if elem['type'] == 'enemy':
                            # Calculate distance from spell target to enemy
                            enemy_x, enemy_y = elem['position']
                            import math
                            distance = math.sqrt((enemy_x - target_position[0])**2 + (enemy_y - target_position[1])**2)
                            
                            # Only affect enemies within the area of effect
                            if distance <= aoe_radius:
                                # Apply damage with distance falloff
                                falloff = 1 - (distance / aoe_radius)
                                elem['health'] -= damage * falloff
                                if elem['health'] <= 0:
                                    enemies_to_remove.append(i)
                    
                    # Remove dead enemies (in reverse order to avoid index issues)
                    for i in sorted(enemies_to_remove, reverse=True):
                        self.elements.pop(i)
                        state_changed = True

                # Implement teleport spell effect
                elif active_spell == 'Teleport':
                    # Teleport moves all players to the target position
                    if self.players:  # Make sure we have players
                        # Spread the players around the target point
                        angles = [0, 120, 240]  # Spread players evenly
                        distance = 40 * power_multiplier  # Distance from target, scales with power
                        
                        for i, player in enumerate(self.players):
                            if i < len(angles):
                                angle_rad = angles[i] * 3.14159 / 180
                                import math
                                new_x = target_position[0] + distance * math.cos(angle_rad)
                                new_y = target_position[1] + distance * math.sin(angle_rad)
                                # Make sure the position is valid
                                if not self.is_position_blocked((new_x, new_y), player.size):
                                    player.position = (new_x, new_y)
                                    print(f"Teleported {player.element} Wizard to ({new_x:.1f}, {new_y:.1f})")
                        state_changed = True

                # Implement barrier spell effect
                elif active_spell == 'Barrier':
                    # Create a barrier wall at the target position
                    barrier_size = int(60 + (40 * power_multiplier))  # Size scales with power
                    
                    # Create a barrier element
                    self.elements.append({
                        'type': 'wall',
                        'position': (target_position[0] - barrier_size/2, target_position[1] - barrier_size/2),
                        'size': (barrier_size, barrier_size),
                        'temp': True,  # This is a temporary wall
                        'timer': int(300 * power_multiplier)  # 5 seconds * power multiplier
                    })
                    print(f"Created barrier at ({target_position[0]}, {target_position[1]})")
                    state_changed = True
                
                # Implementation for multi-cast spells
                elif active_spell == 'Fireball':
                    # Fireball: Powerful fire attack that damages enemies in a larger area
                    damage = 10 * power_multiplier  # High base damage
                    radius = 150 * power_multiplier  # Large area of effect
                    
                    enemies_to_remove = []
                    for i, elem in enumerate(self.elements):
                        if elem['type'] == 'enemy':
                            # Calculate distance from fireball center
                            enemy_x, enemy_y = elem['position']
                            import math
                            distance = math.sqrt((enemy_x - target_position[0])**2 + (enemy_y - target_position[1])**2)
                            
                            # If within radius, apply damage (more damage closer to center)
                            if distance <= radius:
                                # Damage falls off with distance
                                distance_factor = 1 - (distance / radius)
                                actual_damage = damage * distance_factor
                                elem['health'] -= actual_damage
                                
                                if elem['health'] <= 0:
                                    enemies_to_remove.append(i)
                    
                    # Remove dead enemies
                    for i in sorted(enemies_to_remove, reverse=True):
                        self.elements.pop(i)
                        state_changed = True
                    
                    # Add a visual effect element
                    self.elements.append({
                        'type': 'effect',
                        'effect_type': 'explosion',
                        'position': target_position,
                        'radius': radius,
                        'timer': 60,  # 1 second
                        'color': (255, 100, 0)  # Orange-red
                    })
                
                elif active_spell == 'Tidal Wave':
                    # Tidal Wave: Pushes enemies away and damages them
                    damage = 5 * power_multiplier
                    push_strength = 20 * power_multiplier
                    
                    if self.players:
                        # Get the position of the Water wizard to launch from
                        water_wizard = next((p for p in self.players if p.element == 'Water'), self.players[0])
                        center_x, center_y = water_wizard.position
                        
                        for elem in self.elements:
                            if elem['type'] == 'enemy':
                                # Calculate direction from wave center to enemy
                                enemy_x, enemy_y = elem['position']
                                import math
                                distance = math.sqrt((enemy_x - center_x)**2 + (enemy_y - center_y)**2)
                                
                                if distance > 0:  # Avoid division by zero
                                    # Unit direction vector
                                    dir_x = (enemy_x - center_x) / distance
                                    dir_y = (enemy_y - center_y) / distance
                                    
                                    # Push enemy and apply damage
                                    new_x = enemy_x + (dir_x * push_strength)
                                    new_y = enemy_y + (dir_y * push_strength)
                                    
                                    # Apply damage
                                    elem['health'] -= damage
                                    
                                    # Update position if not blocked
                                    if not self.is_position_blocked((new_x, new_y), elem.get('size', 50)):
                                        elem['position'] = (new_x, new_y)
                                        state_changed = True
                        
                        # Remove enemies with no health
                        self.elements = [e for e in self.elements if e['type'] != 'enemy' or e['health'] > 0]
                        
                        # Add a visual effect
                        self.elements.append({
                            'type': 'effect',
                            'effect_type': 'wave',
                            'position': (center_x, center_y),
                            'radius': 0,  # Start small
                            'max_radius': 200,  # Grow to this size
                            'timer': 60,  # 1 second
                            'color': (0, 100, 255)  # Blue
                        })
                
                elif active_spell == 'Earthquake':
                    # Earthquake: Stuns enemies and damages them over time
                    damage = 3 * power_multiplier
                    stun_duration = int(120 * power_multiplier)  # 2 seconds at 60 FPS
                    
                    if self.players:
                        # Get the position of the Earth wizard to launch from
                        earth_wizard = next((p for p in self.players if p.element == 'Earth'), self.players[0])
                        
                        for elem in self.elements:
                            if elem['type'] == 'enemy':
                                # Apply damage
                                elem['health'] -= damage
                                
                                # Stun the enemy
                                elem['stunned'] = True
                                elem['stun_timer'] = stun_duration
                                
                                # Stop movement while stunned
                                elem['original_speed'] = elem.get('speed', 1)
                                elem['speed'] = 0
                                
                                state_changed = True
                        
                        # Remove enemies with no health
                        self.elements = [e for e in self.elements if e['type'] != 'enemy' or e['health'] > 0]
                        
                        # Add a visual effect
                        self.elements.append({
                            'type': 'effect',
                            'effect_type': 'earthquake',
                            'position': (400, 300),  # Center of screen
                            'timer': 90,  # 1.5 seconds
                            'color': (139, 69, 19)  # Brown
                        })
                
                elif active_spell == 'Tornado':
                    # Tornado: Pulls enemies toward the center and damages them
                    damage = 1 * power_multiplier  # Lower damage but continuous
                    pull_strength = 5 * power_multiplier
                    tornado_duration = int(180 * power_multiplier)  # 3 seconds at 60 FPS
                    
                    # Create a persistent tornado effect
                    if self.players:
                        # Get the position of an Air-casting wizard
                        air_wizard = next((p for p in self.players if p.casting_element == 'Air'), self.players[0])
                        center_x, center_y = air_wizard.position
                        
                        # Create the tornado element
                        self.elements.append({
                            'type': 'tornado',
                            'position': (center_x, center_y),
                            'radius': 120 * power_multiplier,
                            'damage': damage,
                            'pull': pull_strength,
                            'timer': tornado_duration,
                            'color': (200, 200, 200)  # Light gray
                        })
                        
                        state_changed = True
                    
                # Let's also handle any temporary elements like barriers or effects
                elements_to_remove = []
                for i, elem in enumerate(self.elements):
                    # Handle temporary walls like barriers
                    if elem.get('type') == 'wall' and elem.get('temp', False):
                        elem['timer'] = elem.get('timer', 0) - 1
                        if elem['timer'] <= 0:
                            elements_to_remove.append(i)
                    
                    # Handle effect elements
                    elif elem.get('type') == 'effect':
                        elem['timer'] = elem.get('timer', 0) - 1
                        if elem['timer'] <= 0:
                            elements_to_remove.append(i)
                        
                        # Handle expanding effects
                        if elem.get('effect_type') == 'wave' and 'max_radius' in elem:
                            elem['radius'] = min(elem.get('max_radius', 100), 
                                              elem.get('radius', 0) + elem.get('max_radius', 100) / elem.get('timer', 60))
                    
                    # Handle tornado elements
                    elif elem.get('type') == 'tornado':
                        elem['timer'] = elem.get('timer', 0) - 1
                        if elem['timer'] <= 0:
                            elements_to_remove.append(i)
                        else:
                            # Apply tornado effects to enemies
                            tornado_x, tornado_y = elem['position']
                            tornado_radius = elem['radius']
                            
                            for enemy in [e for e in self.elements if e['type'] == 'enemy']:
                                enemy_x, enemy_y = enemy['position']
                                import math
                                distance = math.sqrt((enemy_x - tornado_x)**2 + (enemy_y - tornado_y)**2)
                                
                                if distance <= tornado_radius:
                                    # Pull enemy toward tornado center
                                    pull = elem['pull'] * (1 - distance/tornado_radius)  # Stronger pull closer to center
                                    
                                    # Calculate direction toward tornado center
                                    if distance > 0:  # Avoid division by zero
                                        dir_x = (tornado_x - enemy_x) / distance
                                        dir_y = (tornado_y - enemy_y) / distance
                                        
                                        # Update enemy position
                                        new_x = enemy_x + (dir_x * pull)
                                        new_y = enemy_y + (dir_y * pull)
                                        
                                        if not self.is_position_blocked((new_x, new_y), enemy.get('size', 50)):
                                            enemy['position'] = (new_x, new_y)
                                    
                                    # Apply damage
                                    enemy['health'] -= elem['damage']
                            
                            # Remove enemies with no health
                            self.elements = [e for e in self.elements if e['type'] != 'enemy' or e['health'] > 0]
                            
                            # Move the tornado slightly in a random direction
                            import random
                            tornado_x += random.uniform(-1, 1)
                            tornado_y += random.uniform(-1, 1)
                            elem['position'] = (tornado_x, tornado_y)
                        
                            state_changed = True
                    
                # Remove expired elements
                for i in sorted(elements_to_remove, reverse=True):
                    self.elements.pop(i)
                    state_changed = True
            
            elif self.level_type == 'survival':
                # In survival levels, check if timer ran out
                self.timer -= 1
                if self.timer <= 0:
                    self.is_completed = True
                    state_changed = True
                
                # Update enemy spawn timer
                self.enemy_spawn_timer -= 1
                if self.enemy_spawn_timer <= 0:
                    # Spawn a new enemy
                    import random
                    self.elements.append({
                        'type': 'enemy',
                        'position': (random.randint(500, 700), random.randint(100, 500)),
                        'health': 100,
                        'speed': 2
                    })
                    self.enemy_spawn_timer = 120  # Shorter timer for survival
                    state_changed = True
                
                # Check for spell effects on enemies
                if active_spell == 'Steam':
                    # Steam slows down enemies
                    for elem in self.elements:
                        if elem['type'] == 'enemy':
                            elem['speed'] = 0.5  # Slowed
                elif active_spell == 'Lava':
                    # Lava damages enemies
                    for elem in self.elements:
                        if elem['type'] == 'enemy':
                            elem['health'] -= 1
                            if elem['health'] <= 0:
                                self.elements.remove(elem)
                
                # Teleport spell effect for both combat and survival levels
                elif active_spell == 'Teleport':
                    # Teleport all players to random safe positions
                    for player in self.players:
                        # Find a new random position
                        for _ in range(10):  # Try up to 10 times to find a safe position
                            new_x = random.randint(50, 750)
                            new_y = random.randint(50, 550)
                            new_position = (new_x, new_y)
                            
                            # Check if the position is blocked by any level element
                            if not self.is_position_blocked(new_position, (40, 40)):
                                # Set the player's position to the new safe position
                                player.position = new_position
                                break
                    
                    # Teleport spell also damages nearby enemies
                    teleport_range = 150 * power_multiplier
                    for player in self.players:
                        for elem in self.elements[:]:  # Use a copy to safely remove elements
                            if elem['type'] == 'enemy':
                                # Calculate distance from player to enemy
                                dx = player.position[0] - elem['position'][0]
                                dy = player.position[1] - elem['position'][1]
                                distance = (dx**2 + dy**2)**0.5
                                
                                # If enemy is within teleport range, damage it
                                if distance < teleport_range:
                                    elem['health'] -= 10 * power_multiplier
                                    if elem['health'] <= 0:
                                        self.elements.remove(elem)
                                        state_changed = True
                
                # Barrier spell effect for both combat and survival levels
                elif active_spell == 'Barrier':
                    # Create barriers around each player
                    barrier_duration = int(300 * power_multiplier)  # 5 seconds (60 FPS) scaled by power
                    barrier_size = int(80 * power_multiplier)
                    
                    for player in self.players:
                        # Create a barrier element with the player's position
                        barrier = {
                            'type': 'barrier',
                            'position': (player.position[0] - barrier_size // 2, player.position[1] - barrier_size // 2),
                            'size': (barrier_size, barrier_size),
                            'duration': barrier_duration,
                            'player_id': id(player)  # Store the player ID to follow the player
                        }
                        self.elements.append(barrier)
                        state_changed = True
        
        # Update enemy positions (they move toward the players)
        for elem in self.elements:
            if elem['type'] == 'enemy':
                # Simple AI: move toward center-left of screen
                target_x, target_y = 200, 300
                dx = target_x - elem['position'][0]
                dy = target_y - elem['position'][1]
                
                # Normalize and apply speed
                distance = max(1, (dx**2 + dy**2)**0.5)  # avoid division by zero
                elem['position'] = (
                    elem['position'][0] + (dx / distance) * elem['speed'],
                    elem['position'][1] + (dy / distance) * elem['speed']
                )
                state_changed = True
        
        # Update barriers
        for elem in self.elements[:]:  # Use a copy to safely remove elements
            if elem['type'] == 'barrier':
                # Reduce duration
                elem['duration'] -= 1
                
                # Remove if duration expired
                if elem['duration'] <= 0:
                    self.elements.remove(elem)
                    state_changed = True
                else:
                    # Update barrier position to follow player
                    for player in self.players:
                        if id(player) == elem['player_id']:
                            barrier_size = elem['size'][0]
                            elem['position'] = (player.position[0] - barrier_size // 2, player.position[1] - barrier_size // 2)
                
                # Check if barriers block enemies
                for enemy in self.elements[:]:
                    if enemy['type'] == 'enemy':
                        # Check if enemy collides with any barrier
                        barrier_rect = pygame.Rect(elem['position'][0], elem['position'][1], 
                                                  elem['size'][0], elem['size'][1])
                        enemy_rect = pygame.Rect(enemy['position'][0], enemy['position'][1], 40, 40)
                        
                        if barrier_rect.colliderect(enemy_rect):
                            # Push enemy away from barrier
                            dx = enemy['position'][0] - (elem['position'][0] + elem['size'][0]/2)
                            dy = enemy['position'][1] - (elem['position'][1] + elem['size'][1]/2)
                            
                            # Normalize the direction vector
                            length = max(1, (dx**2 + dy**2)**0.5)
                            dx /= length
                            dy /= length
                            
                            # Push enemy away
                            push_strength = 5
                            enemy['position'] = (enemy['position'][0] + dx * push_strength,
                                                enemy['position'][1] + dy * push_strength)
        
        return state_changed
                
    def get_display_text(self):
        """
        Get text to display for this level.
        
        Returns:
            list: List of (text, position) tuples for rendering
        """
        texts = [
            (f"Level: {self.name}", (20, 20)),
            (f"Objective: {self.objective}", (20, 50))
        ]
        
        if self.level_type == 'survival':
            # Add timer for survival levels
            seconds_left = self.timer // 60
            texts.append((f"Time: {seconds_left}s", (20, 80)))
        
        if self.is_completed:
            texts.append(("COMPLETED!", (300, 20)))
            
        return texts
        
def create_levels():
    """
    Create a list of test levels.
    
    Returns:
        list: List of Level objects
    """
    levels = [
        # Puzzle level - cast Mud to fill a gap
        Level(
            "Bridge the Gap", 
            "puzzle", 
            "Cast MUD to create a bridge across the gap",
            "Mud"
        ),
        
        # Combat level - defeat enemies with Lava
        Level(
            "Flame On", 
            "combat", 
            "Cast LAVA to defeat all enemies"
        ),
        
        # Survival level - survive for 30 seconds using Steam to slow enemies
        Level(
            "Foggy Escape", 
            "survival", 
            "Survive for 30 seconds! Use STEAM to slow down enemies"
        )
    ]
    
    return levels
