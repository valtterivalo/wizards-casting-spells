# Wizards Casting Spells

A cooperative multiplayer puzzle/strategy game built with Python and Pygame where 1-3 players control wizards who combine magical elements to cast spells and tackle level objectives.

## Game Overview

- **Genre**: Cooperative Puzzle / Strategy
- **Platform**: Windows, Mac, Linux (any system with Python and Pygame)
- **Players**: 1-3 local players using the same keyboard
- **Objective**: Work together to cast spells by combining elements (Fire, Water, Earth) to solve puzzles, fight enemies, or survive challenges

## Features

- **Three Unique Wizards**:
  - **Fire Wizard** (Red): Focuses on attack spells
  - **Water Wizard** (Blue): Supports with healing or barriers
  - **Earth Wizard** (Green): Offers utility like blocking or building

- **Spell Casting System**:
  Players press their keys to cast elements into a shared "spell circle." If elements are combined within 2 seconds, a spell activates:
  - Fire + Water = Steam (obscures enemies)
  - Fire + Earth = Lava (damages enemies)
  - Water + Earth = Mud (slows enemies or fills gaps)
  - All Three = Storm (big area effect)

- **Varied Level Types**:
  - **Puzzle**: Cast specific spells to overcome obstacles
  - **Combat**: Defeat enemies using appropriate spells
  - **Survival**: Stay alive for a set duration using protective spells

## Installation

1. Ensure you have Python 3.x installed
2. Install Pygame:
   ```
   pip install pygame
   ```
3. Clone this repository:
   ```
   git clone https://github.com/yourusername/wizards-casting-spells.git
   cd wizards-casting-spells
   ```
4. Run the game:
   ```
   python src/main.py
   ```

## Controls

- **Fire Wizard**: `W` key
- **Water Wizard**: `T` key
- **Earth Wizard**: `I` key
- **Menu Navigation**: Arrow keys and Enter
- **Return to Menu**: Escape key

## Getting Started

1. From the main menu, select "Start Game"
2. Press Space to begin each level
3. Work together to cast spells by combining elements
4. Complete level objectives to progress
5. New spells unlock as you advance through the game

## Development

This project was created as a beginner-friendly Python/Pygame example. The modular design makes it easy to extend with:
- New spell combinations
- Additional levels
- Custom graphics and sound effects