class Player:
    """
    Represents a wizard player in the game.
    
    Attributes:
        element (str): The wizard's element ('Fire', 'Water', or 'Earth')
        position (tuple): (x, y) coordinates of the wizard
        color (tuple): RGB color value representing the wizard
        is_casting (bool): Whether the wizard is currently casting a spell
        cast_time (int): Timer for how long the wizard has been casting
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
        
    def start_cast(self):
        """
        Start casting a spell element.
        """
        self.is_casting = True
        self.cast_time = 0
        
    def update(self):
        """
        Update the player's state. Currently just advances the cast timer.
        """
        if self.is_casting:
            self.cast_time += 1
            # After 30 frames (0.5 seconds at 60 FPS), stop casting
            if self.cast_time > 30:
                self.is_casting = False
                
    def get_display_color(self):
        """
        Get the color to display the wizard. If casting, returns a brighter color.
        
        Returns:
            tuple: RGB color value
        """
        if self.is_casting:
            # Make a brighter version of the color when casting
            return tuple(min(c + 100, 255) for c in self.color)
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
        if len(self.completed_levels) >= 3 and 'Storm' not in self.unlocked_spells:
            self.unlocked_spells.append('Storm')
            self.new_unlocks.append('Storm')
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
        activation_timer (int): Countdown timer for spell activation
        active_spell (str): Currently active spell, if any
        spell_effect_timer (int): Timer for how long a spell effect is shown
        game_progress (GameProgress): Reference to the game progress tracker
    """
    
    def __init__(self, game_progress=None):
        """
        Initialize a new spell circle.
        
        Args:
            game_progress (GameProgress, optional): Game progress tracker
        """
        self.elements = []
        self.activation_timer = 0
        self.active_spell = None
        self.spell_effect_timer = 0
        self.game_progress = game_progress
        
    def add_element(self, element):
        """
        Add an element to the spell circle.
        
        Args:
            element (str): Element to add ('Fire', 'Water', or 'Earth')
        """
        # Only add the element if it's not already in the circle
        if element not in self.elements:
            self.elements.append(element)
            # Reset the activation timer (2 seconds at 60 FPS = 120 frames)
            self.activation_timer = 120
    
    def update(self):
        """
        Update the spell circle state, checking for spell activation.
        
        Returns:
            str or None: The name of a newly activated spell, or None
        """
        # If a spell is currently active, update its effect timer
        if self.active_spell:
            self.spell_effect_timer -= 1
            if self.spell_effect_timer <= 0:
                self.active_spell = None
                return None
            
        # If there are elements in the circle, count down the timer
        if self.elements and self.activation_timer > 0:
            self.activation_timer -= 1
            
            # If the timer runs out or we have all three elements, try to activate a spell
            if self.activation_timer == 0 or len(self.elements) == 3:
                spell_name = self._check_spell_combination()
                if spell_name:
                    # Check if the spell is unlocked
                    if not self.game_progress or self.game_progress.is_spell_unlocked(spell_name):
                        self.active_spell = spell_name
                        self.spell_effect_timer = 180  # 3 seconds at 60 FPS
                        self.elements = []  # Clear the elements after casting
                        return spell_name
                    else:
                        # If spell is not unlocked, show a visual cue
                        print(f"Spell {spell_name} is not unlocked yet!")
                
                # Clear the elements if no valid combo or spell not unlocked
                self.elements = []
        
        return None
    
    def _check_spell_combination(self):
        """
        Check if the current elements form a valid spell combination.
        
        Returns:
            str or None: Name of the spell if valid, None otherwise
        """
        # Sort the elements for consistent checking
        sorted_elements = sorted(self.elements)
        
        # Check for valid combinations
        if sorted_elements == ['Earth', 'Fire']:
            return 'Lava'
        elif sorted_elements == ['Fire', 'Water']:
            return 'Steam'
        elif sorted_elements == ['Earth', 'Water']:
            return 'Mud'
        elif sorted_elements == ['Earth', 'Fire', 'Water']:
            return 'Storm'
        
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
        self.enemy_spawn_timer = 180  # 3 seconds at 60 FPS
    
    def update(self, active_spell):
        """
        Update the level state based on elapsed time and player actions.
        
        Args:
            active_spell (str or None): The currently active spell
            
        Returns:
            bool: True if level state changed (completed, enemy died, etc.)
        """
        state_changed = False
        
        # Check for level completion
        if not self.is_completed:
            if self.level_type == 'puzzle' and active_spell == self.target_spell:
                # In puzzle levels, casting the target spell completes the level
                self.is_completed = True
                state_changed = True
            
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
                
                # Check for spell damage to enemies
                if active_spell == 'Lava':
                    # Lava damages enemies
                    for elem in self.elements:
                        if elem['type'] == 'enemy':
                            elem['health'] -= 2
                            if elem['health'] <= 0:
                                self.elements.remove(elem)
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
