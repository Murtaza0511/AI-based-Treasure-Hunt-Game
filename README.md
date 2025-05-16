# Treasure Race: AI Board Game

## Overview

Treasure Race is a two-player interactive Python game built using Pygame. In this exciting board game, players race to collect treasures while avoiding AI-controlled guards. The game includes dynamic gameplay mechanics like power-ups, collectibles, and an engaging AI that chases players based on their position. The first player to collect 6 treasures and reach the goal at the bottom-right corner wins the game.

## Game Objective

* Players must collect **6 treasures** scattered across the grid.
* After collecting all treasures, the player must race to the **bottom-right corner** to win.
* Players must avoid getting caught by **AI guards**.
* If both players are caught by the guards, the guards win.

## Controls

* **Player 1 (Blue)**: Use the **Arrow Keys** (↑ ↓ ← →)
* **Player 2 (Green)**: Use the **W A S D keys**
* Press **SPACE** to start the game.
* Press **R** to replay the game.
* Press **ESC** to quit the game.

## Key Features

### AI Guard Logic

* Guards chase the closest player using **Manhattan distance**.
* Guards move towards the player every **1.3 seconds**.
* They are programmed to avoid collisions with each other.
* If a guard catches a player, that player is eliminated.

### Power-ups and Scoring

* **Treasures (Yellow)**: Collecting a treasure gives **+1 point**.
* **Power-Ups (White)**: Temporarily boost a player's speed.
* The first player to collect 6 treasures and reach the goal wins.
* Collectibles (treasures and power-ups) are randomly placed on the board.

### Visual & UX Features

* Smooth, tile-based movement across a **14x14 grid**.
* The window is **resizable** and adjusts the grid size accordingly.
* **Title screen** with game instructions.
* **Game-over screen** displays the winner and gives an option to replay.
* The **finishing arrow** shows the direction of the goal.

## How to Run the Game

1. Install Python 3.x on your machine.
2. Install the required dependencies using pip:

   ```bash
   pip install pygame
   ```
3. Download the project files.
4. Run the game:

   ```bash
   python game.py
   ```

## Demo and Conclusion

* The game features **AI pathfinding** and intelligent decision-making by the guards.
* **Guard movement** is based on the Manhattan distance, ensuring the game is challenging but fair.
* Players experience **dynamic gameplay** with every match, thanks to the random placement of treasures, power-ups, and guards.
