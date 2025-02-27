# Wizards Casting Spells - Updated Development Spec File (Python & Pygame)

**Version**: 2.0  
**Date**: February 27, 2025  
**Author**: Valtteri Valo  
**Progress Update**: April 10, 2025

---

## 1. Introduction

*Wizards Casting Spells* is a cooperative multiplayer game where 1-3 players control wizards who combine magical elements to cast spells and complete level objectives. The current MVP, built with Python and Pygame, includes basic casting mechanics, three wizards (Fire, Water, Earth), and a few levels with puzzle, combat, and survival elements. However, player feedback indicates the game feels too static, the casting is overly simplistic, the UI is cluttered, and spell variety lacks depth. This updated spec file outlines the next phase of development to address these issues, introducing enhanced mechanics, movement, a streamlined UI, and richer spell options.

---

## 2. Key Feedback and Solutions

Feedback from the MVP highlights four critical areas for improvement. Here's how we'll tackle them:

### 2.1. Casting Mechanic Feels Too Easy and Boring
- **Issue**: Pressing a key once at the right time lacks challenge and engagement.
- **Solution**: Replace the single-press system with a **charging mechanic**. Players must hold their key to charge a spell, with power scaling based on duration. Overcharging risks failure, adding skill and coordination.
- **Status**: COMPLETED ✓

### 2.2. Lack of Movement Makes Gameplay Static
- **Issue**: Stationary wizards limit dynamism and strategy.
- **Solution**: Add **movement controls** so wizards can navigate levels, avoid enemies, and position for spells. Introduce terrain and obstacles to make movement meaningful.
- **Status**: COMPLETED ✓

### 2.3. Cluttered and Unclear UI
- **Issue**: The current UI confuses players with unclear information.
- **Solution**: Redesign the UI with a **dedicated spell circle display**, **player status bars**, and a **clear objective panel**. Use icons and color-coding for quick readability.
- **Status**: COMPLETED ✓

### 2.4. Limited Spell Variety Reduces Dynamism
- **Issue**: Few spell combinations limit replayability and excitement.
- **Solution**: Expand the spell system with **new elements** (e.g., Air) and **multi-cast spells** (e.g., two Fire casts for a Fireball). Add diverse effects like teleportation or shields.
- **Status**: COMPLETED ✓ (Air element and multi-cast spells implemented)

---

## 3. Updated Core Features

### 3.1. Enhanced Spell Casting Mechanic
- **Charging System**: Players hold their casting key (e.g., 1, 4, 7) to charge their element. Charge level (0-100%) determines spell power.
  - **Visual Feedback**: A charge bar appears above each wizard.
  - **Risk-Reward**: Holding beyond 100% (e.g., >2 seconds) risks overcharge, reducing power or failing the cast.
- **Combination Timing**: Spells still require casts within a 2-second window, but charge levels influence the outcome.
- **Status**: COMPLETED ✓

### 3.2. Wizard Movement
- **Controls**: 
  - Player 1 (Fire): WASD (W=up, S=down, A=left, D=right)
  - Player 2 (Water): TFGH (T=up, G=down, F=left, H=right)
  - Player 3 (Earth): IJKL (I=up, K=down, J=left, L=right)
- **Casting Keys**:
  - Player 1: 1
  - Player 2: 4
  - Player 3: 7
- **Mechanics**: Wizards move at a set speed, with collision detection for terrain and enemies.
- **Strategic Impact**: Positioning affects spell range or effectiveness (e.g., closer casts hit harder).
- **Status**: COMPLETED ✓ (Basic movement and collision detection implemented)

### 3.3. Streamlined UI
- **Spell Circle**: Central display showing elements cast, charge levels, and a shrinking timer ring.
- **Player Status**: Bars above wizards for charge progress and health (if added).
- **Objective Panel**: Top bar with level goals and progress (e.g., "Enemies Left: 3").
- **Status**: COMPLETED ✓

### 3.4. Expanded Spell Variety
- **New Elements**: Add Air (e.g., Player 1 alternate key: 2).
- **Multi-Cast Spells**: Multiple casts of one element unlock stronger variants (e.g., Fire x2 = Fireball, Fire x3 = Firestorm).
- **New Effects**: Beyond damage/slowing, include teleportation, barriers, or enemy repulsion.
- **Status**: COMPLETED ✓ (Air element added with casting keys for all players - 2, 5, 8. Multi-cast spells implemented)

---

## 4. Development Roadmap

This roadmap builds on the existing MVP in `src/game.py`, `src/main.py`, and `src/rendering.py`. Each phase is actionable and sequential.

### Phase 1: Implement Charging Mechanic
- **Goal**: Replace single-press casting with a skill-based charging system.
- **Tasks**:
  - **Update `Player` Class** (`game.py`): COMPLETED ✓
    - Add `charge_level` (0-100) and `max_charge_time` (120 frames = 2 seconds).
    - Modify `start_cast()` to reset `charge_level`; update `update()` to increment it while the key is held (e.g., 1, 4, 7).
    - Add overcharge penalty (e.g., if `charge_level > 100`, spell power drops to 50%).
  - **Update `SpellCircle` Class** (`game.py`): COMPLETED ✓
    - Store `charge_level` with each element in `elements` (e.g., `["Fire", 75]`).
    - Adjust `_check_spell_combination()` to scale spell effects by average charge.
  - **Enhance Rendering** (`rendering.py`): COMPLETED ✓
    - In `draw_player()`, add a charge bar above each wizard (e.g., `pygame.draw.rect()` with width tied to `charge_level`).
  - **Update Input** (`main.py`): COMPLETED ✓
    - Change casting keys from W, T, I to 1, 4, 7.
  - **Test**: Ensure charging feels responsive and overcharging penalizes without frustrating. COMPLETED ✓
- **Duration**: 3-4 days. COMPLETED ✓

### Phase 2: Add Wizard Movement
- **Goal**: Enable wizards to move, adding dynamism and strategy.
- **Tasks**:
  - **Update `Player` Class** (`game.py`): COMPLETED ✓
    - Add `move_speed` (e.g., 3 pixels/frame) and `velocity` (x, y).
    - In `update()`, adjust `position` based on key inputs (WASD, TFGH, IJKL).
  - **Collision Detection** (`game.py`): COMPLETED ✓
    - Add `collides_with()` method to check against level elements (e.g., gaps, enemies).
    - Prevent movement into obstacles or off-screen.
  - **Update `Level` Class** (`game.py`): COMPLETED ✓
    - Enhance `elements` with terrain (e.g., `{'type': 'wall', 'position': (300, 200), 'size': (100, 50)}`).
    - Adjust `update()` to account for wizard positions (e.g., enemies target nearest wizard).
  - **Rendering** (`rendering.py`): COMPLETED ✓
    - In `draw_level()`, render terrain (e.g., gray rectangles for walls).
    - Update `draw_player()` to reflect new positions.
  - **Update Input** (`main.py`): COMPLETED ✓
    - Add movement keys: WASD (Player 1), TFGH (Player 2), IJKL (Player 3).
  - **Test**: Verify movement is smooth and collisions work. COMPLETED ✓
- **Duration**: 4-5 days. COMPLETED ✓

### Phase 3: Redesign UI
- **Goal**: Make the UI intuitive and uncluttered.
- **Tasks**:
  - **Spell Circle** (`rendering.py`): COMPLETED ✓
    - Redesign `draw_spell_circle()` to show element icons (e.g., small circles) and a timer ring (shrinking `timer_radius`).
    - Display charge levels as arc segments inside the circle.
  - **Player Status** (`rendering.py`): COMPLETED ✓
    - In `draw_player()`, add a health bar (if health is implemented) alongside the charge bar.
  - **Objective Panel** (`rendering.py`): COMPLETED ✓
    - Add `draw_objective_panel()` to render a top bar with `current_level.objective` and progress (e.g., enemies left).
  - **Test**: Ensure all elements are clear and don't overlap. COMPLETED ✓
- **Duration**: 3-4 days. COMPLETED ✓

### Phase 4: Expand Spell Variety
- **Goal**: Increase spell options for depth and excitement.
- **Tasks**:
  - **New Elements** (`game.py`): COMPLETED ✓
    - Add Air element (e.g., Player 1 alternate key: 2).
    - Update `SpellCircle._check_spell_combination()` with combos like Fire + Air = Explosion.
  - **Multi-Cast Spells** (`game.py`): COMPLETED ✓
    - Modify `add_element()` to allow duplicates (e.g., `["Fire", "Fire"]`).
    - Define new spells: Fire x2 = Fireball (high damage), Fire x3 = Firestorm (area damage).
  - **New Effects** (`game.py` & `rendering.py`): COMPLETED ✓
    - In `Level.update()`, implement effects like teleportation (move wizard), barriers (block enemies).
    - In `draw_spell_effect()`, add visuals (e.g., white flash for teleport).
  - **Test**: Balance new spells for fun and fairness. PARTIAL ✓
    - **TODO**: Additional playtesting needed to ensure spell balance.
- **Duration**: 4-5 days. COMPLETED ✓

### Phase 5: Polish and Bug Fixing
- **Goal**: Refine gameplay and fix issues.
- **Tasks**:
  - **Bug Fixes**: Address movement glitches, spell misfires, or UI overlaps. TODO
  - **Balance**: Adjust charge times (e.g., 1.5-2 seconds optimal), movement speed, and enemy difficulty. TODO
  - **Enhanced Cooperative Spellcasting System**: Implement expanded mechanics for deeper teamwork. COMPLETED ✓ 
    - **Tertiary Elements**: Allow each wizard to cast a third element (Fire→Water, Water→Earth, Earth→Fire) COMPLETED ✓
    - **Effort-Based Casting**: Implement variable charge times and power levels based on element affinity COMPLETED ✓
    - **Elemental Resonance**: Add bonuses when multiple wizards cast the same element COMPLETED ✓
    - **Attunement Mechanic**: Create system for wizards to boost others' casting abilities COMPLETED ✓
    - **Visual Feedback**: Add effects showing wizard cooperation and combined casting COMPLETED ✓
  - **Polish**: Enhance visuals (e.g., sprite animations in `create_wizard_sprites.py`) and sounds (e.g., charge hum in `create_sounds.py`). TODO
  - **Tutorial**: Add a first level explaining mechanics (e.g., "Hold 1 to charge Fire"). TODO
  - **Test**: Playtest with 1-3 players to ensure flow and fun. TODO
- **Duration**: 4-6 days. IN PROGRESS

---

## 5. Technical Details

- **Language**: Python 3.x  COMPLETED ✓
- **Library**: Pygame 2.5.0  COMPLETED ✓
- **Notes**:
    - The developer's console doesn't support the && syntax and needs to use ; instead
    - The developer doesn't have python in path, and py needs to be used instead
- **Updated Controls**:
  - **Player 1 (Fire)**: COMPLETED ✓
    - Movement: WASD (W=up, S=down, A=left, D=right)
    - Casting: Hold 1
    - Alternate Cast (e.g., Air): 2
    - **New Controls**: COMPLETED ✓
      - Tertiary Cast (Water): 3
      - Attunement/Spell Donation: E
  - **Player 2 (Water)**: COMPLETED ✓
    - Movement: TFGH (T=up, G=down, F=left, H=right)
    - Casting: Hold 4
    - Alternate Cast: 5
    - **New Controls**: COMPLETED ✓
      - Tertiary Cast (Earth): 6
      - Attunement/Spell Donation: Y
  - **Player 3 (Earth)**: COMPLETED ✓
    - Movement: IJKL (I=up, K=down, J=left, L=right)
    - Casting: Hold 7
    - Alternate Cast: 8
    - **New Controls**: COMPLETED ✓
      - Tertiary Cast (Fire): 9
      - Attunement/Spell Donation: O
- **Files to Modify**:
  - `game.py`: Core logic for charging, movement, spells, and levels. COMPLETED ✓
  - `main.py`: Input handling for new controls. COMPLETED ✓
  - `rendering.py`: UI and visual updates. COMPLETED ✓
  - `assets/`: New sprites and sounds as needed. PARTIAL (Sound files partially implemented)

---

## 6. Art and Audio Assets

- **Sprites**: Add movement animations (e.g., walking frames in `create_wizard_sprites.py`). TODO
- **UI Icons**: Element symbols (e.g., flame for Fire) in `images/`. TODO
- **Sounds**: Charging sound (rising pitch), movement steps in `create_sounds.py`. PARTIAL
  - **TODO**: Implement charging sound effects and movement step sounds.

---

## 7. Testing and Quality Assurance

- **Unit Tests**: Test charging, movement, and spell combos in isolation. PARTIAL
- **Integration Tests**: Ensure movement and casting sync without lag. PARTIAL
- **Playtesting**: Focus on pacing (not too easy/hard) and UI clarity. TODO

---

## 8. Next Steps

Start with **Phase 1** to overhaul the casting mechanic, as it's the core of the gameplay experience. Once that's stable, proceed to **Phase 2** for movement, which will transform the game's feel. The UI and spell variety (Phases 3-4) will build on these foundations, with **Phase 5** ensuring a polished release.

- Phase 1: Implement Charging Mechanic - COMPLETED ✓
- Phase 2: Add Wizard Movement - COMPLETED ✓
- Phase 3: Redesign UI - COMPLETED ✓
- Phase 4: Expand Spell Variety - COMPLETED ✓
- Phase 5: Polish and Bug Fixing - TODO

---