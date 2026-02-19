# Tic-Tac-Toe AI Agent (Minimax)

## Overview
This project implements an intelligent agent to play Tic-Tac-Toe against a human user. The agent uses adversarial search, specifically the Minimax algorithm, to make optimal decisions. It assumes the human opponent also plays optimally.

## Features
- **Core Minimax Algorithm:** Correct recursive implementation for perfect play.
- **Alpha-Beta Pruning :** Optimizes the search by pruning irrelevant branches. User can choose to enable/disable it to compare performance.
- **Interactive Gameplay:** Clear command-line interface with board display and input validation.
- **Performance Metrics:** Displays the number of game tree nodes expanded and the decision time for the AI's move.
- **Configurable Start:** User can choose who makes the first move.
- **Game Termination:** Accurately detects wins, losses, and draws.

## Requirements
- Python 3.6 or higher.
- No external libraries are required.
The program uses only Python Standard Library modules:
- `math` - for infinity values in alpha-beta pruning
- `time` - for performance measurement

---

## How to Run
1.  Save the Python script as `tic_tac_toe_agent.py`.
2.  Open a terminal or command prompt in the directory containing the file.
3.  Run the command: `python tic_tac_toe_agent.py`
4.  Follow the on-screen prompts to configure and play the game.

## Game Rules
- The board is numbered 1 to 9, corresponding to positions from top-left (1) to bottom-right (9).
- The Human player is 'X' (the Minimizing player in the algorithm's perspective).
- The AI agent is 'O' (the Maximizing player).
- Players take turns placing their marks in empty squares.
- The first player to get three of their marks in a row (horizontally, vertically, or diagonally) wins.
- If all nine squares are filled without a winner, the game is a draw.

## Algorithm Explanation
The AI's decision-making is based on the Minimax algorithm. It explores all possible future game states from the current position, assuming the opponent will also play optimally to minimize the AI's chance of winning.

- **Utility:** The utility function assigns values to terminal states: +1 for a win for 'O' (AI), -1 for a win for 'X' (Human), and 0 for a draw.
- **Maximizing Player (AI - 'O'):** Aims to choose moves that lead to states with the highest utility.
- **Minimizing Player (Human - 'X'):** Aims to choose moves that lead to states with the lowest utility.

The algorithm recursively evaluates moves until it reaches a terminal state, then propagates the utility values back up the game tree to select the best move for the current player. The optional Alpha-Beta pruning enhancement significantly speeds up this process by keeping track of the best possible outcomes for each player and ignoring branches that cannot possibly influence the final decision.

## Code Structure
- `TicTacToe` class: Manages the game board, rules, move validation, and win/draw detection.
- `MinimaxAgent` class: Encapsulates the search algorithms.
    - `get_best_move()`: Public interface for the agent.
    - `_minimax()`: Private recursive implementation of the standard Minimax algorithm.
    - `_minimax_alpha_beta()`: Private recursive implementation of Minimax with pruning.
    - `_copy_game()`: Helper to create deep copies of the game state for simulation.
- `play_game()`: Manages the main game loop, player turns, and user interaction.