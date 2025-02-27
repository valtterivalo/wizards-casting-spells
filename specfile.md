# Wizards Casting Spells - Development Spec File (Python & Pygame)

**Version**: 1.0  
**Date**: 2025-02-27
**Author**: Valtteri Valo

---

## 1. Introduction
*Wizards Casting Spells* is a cooperative multiplayer game where 1-3 players control wizards who combine magical elements to cast spells and tackle level objectives. After a tough go with C, we’re switching to Python with Pygame for a smoother, beginner-friendly experience. This spec outlines the project setup, provides a starting script, and maps out the development plan.

---

## 2. Game Overview
- **Genre**: Cooperative Puzzle / Strategy  
- **Platform**: Any system with Python and Pygame (Windows, Mac, Linux)  
- **Players**: 1-3 local players using the same keyboard  
- **Objective**: Work together to cast spells by combining elements (Fire, Water, Earth) to solve puzzles, fight enemies, or survive challenges.  
- **Tech Stack**: Python 3.x, Pygame library  

---

## 3. Core Features

### 3.1 Wizards
- **Fire Wizard**: Red, focuses on attack spells.  
- **Water Wizard**: Blue, supports with healing or barriers.  
- **Earth Wizard**: Green, offers utility like blocking or building.  

### 3.2 Spell Casting
- **How It Works**: Each player presses a key to cast their element into a shared "spell circle." If all players cast within 2 seconds, a spell activates based on the combo.  
- **Starting Spells**:  
  - Fire + Water = Steam (obscures enemies).  
  - Fire + Earth = Lava (damages enemies).  
  - Water + Earth = Mud (slows enemies or fills gaps).  
  - All Three = Storm (big area effect).  

### 3.3 Levels
- **Structure**: 5-10 short levels with unique goals.  
- **Types**:  
  - **Puzzle**: E.g., cast Mud to cross a gap.  
  - **Combat**: E.g., use Lava to defeat enemies.  
  - **Survival**: E.g., survive enemy waves with Steam.  

### 3.4 Visuals & Sound
- **Graphics**: 2D, starting with colored shapes (e.g., red square for Fire Wizard).  
- **Audio**: Basic beeps for now, later replaced with spell sounds.  

---

## 4. Project Structure
wizards_casting_spells/
├── main.py           # Game loop and Pygame setup
├── game.py           # Player, spell, and level logic
├── rendering.py      # Drawing functions
├── assets/
│   ├── images/       # For sprites (empty initially)
│   └── sounds/       # For sounds (empty initially)
└── requirements.txt  # Lists pygame

---

## 5. Starting Script
The basic `main.py` (already provided) initializes Pygame, opens an 800x600 window, and draws a red square. It’s the foundation we’ll expand.

---

## 6. Development Steps
Here’s the plan, broken into phases. Each builds on the last.

### Phase 1: Project Setup & Window
- **Goal**: Get the structure and basic window working.  
- **Tasks**:  
  - Create the folder structure.  
  - Set up `requirements.txt` with `pygame`.  
  - Test the provided `main.py`—ensure it runs and shows a red square.  
- **Next**: Move to rendering multiple wizards.  

### Phase 2: Basic Rendering
- **Goal**: Draw all three wizards on screen.  
- **Tasks**:  
  - Create `rendering.py` with a `draw_wizard(screen, position, color)` function.  
  - Update `main.py` to draw three wizards (e.g., red at (100, 100), blue at (200, 100), green at (300, 100)).  
- **Next**: Add player input.  

### Phase 3: Player Input & Wizards
- **Goal**: Let players control their wizards.  
- **Tasks**:  
  - In `game.py`, make a `Player` class with `element` (Fire/Water/Earth) and `position`.  
  - In `main.py`, detect key presses: `W` for Player 1, `Up` for Player 2, `I` for Player 3.  
  - Show feedback (e.g., wizard flashes when key is pressed).  
- **Next**: Build the spell system.  

### Phase 4: Spell Casting
- **Goal**: Combine elements into spells.  
- **Tasks**:  
  - In `game.py`, add a `SpellCircle` class to track elements and a 2-second timer.  
  - Define spell combos (e.g., Fire + Water = Steam).  
  - In `rendering.py`, draw the spell circle (e.g., a circle showing cast elements).  
  - Add a simple effect (e.g., screen flash) when a spell triggers.  
- **Next**: Add levels.  

### Phase 5: Levels & Objectives
- **Goal**: Create playable levels.  
- **Tasks**:  
  - In `game.py`, add a `Level` class with `objective` (e.g., “cast Mud”).  
  - Make 3 test levels: one puzzle, one combat, one survival.  
  - Update rendering to show level elements (e.g., enemies as white squares).  
- **Next**: Polish it up.  

### Phase 6: Polish & Progression
- **Goal**: Make it feel like a real game.  
- **Tasks**:  
  - Add a main menu in `rendering.py` (Start, Exit).  
  - Implement progression (e.g., unlock a new spell after a level).  
  - Swap placeholders for basic assets (e.g., simple sprites, sounds).  
- **Next**: Playtest and tweak.  

---

## 7. Technical Details
- **Language**: Python 3.x  
- **Library**: Pygame  
- **Controls**:  
  - Player 1 (Fire): `W`  
  - Player 2 (Water): `T`  
  - Player 3 (Earth): `I`  
- **Graphics**: 2D Pygame drawing (rectangles for now).  
- **FPS**: 60  

---

## 8. Tips
- **Install Pygame**: `pip install pygame` if you haven’t.  
- **Run**: `python main.py` from the project folder.  
- **Expand**: Add more spells or levels as you go—keep it modular!  

---