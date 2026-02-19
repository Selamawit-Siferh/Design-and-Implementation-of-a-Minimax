"""
Addis Ababa University - MSc in AI
Course: Artificial Intelligence
Assignment: Design and Implementation of a Minimax Game-Playing Agent
Instructor: Dr. Natnael Argaw Wondimu

Student: [Your Name Here]
ID: [Your ID Here]

Game: Tic-Tac-Toe
"""

import math
import time

class TicTacToe:
    """
    Represents the Tic-Tac-Toe game state and rules.
    """
    def __init__(self):
        """Initializes an empty board. Human is 'X' (MAX), AI is 'O' (MIN)."""
        self.board = [' ' for _ in range(9)]  # Represents 3x3 board as list
        self.current_winner = None

    def display_board(self):
        """Prints the current board state."""
        for i in range(3):
            row = self.board[i*3:(i+1)*3]
            print('| ' + ' | '.join(row) + ' |')
            if i < 2:
                print(' -----------')

    def display_board_with_indices(self):
        """Prints a board with numbered positions (1-9) to guide the user."""
        print("\nBoard positions (for your move):")
        for i in range(3):
            row_indices = [str(i*3 + j + 1) for j in range(3)]
            print('| ' + ' | '.join(row_indices) + ' |')
            if i < 2:
                print(' -----------')
        print()

    def available_moves(self):
        """Returns a list of indices (0-8) of empty squares."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def is_empty_square(self, square):
        """Checks if a specific square index is empty."""
        return self.board[square] == ' '

    def make_move(self, square, letter):
        """
        Places a letter on the board.
        Returns True if the move is valid and made, False otherwise.
        """
        if self.is_empty_square(square):
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        """
        Checks for a winning condition after the last move.
        Only needs to check the row, col, and diagonal of the last move.
        """
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        # Check column
        col_ind = square % 3
        column = [self.board[col_ind + i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonals (only if square is on a diagonal)
        if square % 2 == 0:
            # Main diagonal (0,4,8)
            diag1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diag1]):
                return True
            # Anti-diagonal (2,4,6)
            diag2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diag2]):
                return True

        return False

    def is_board_full(self):
        """Returns True if the board is full, False otherwise."""
        return ' ' not in self.board

    def get_board_state(self):
        """Returns a tuple representation of the board for hashing (optional)."""
        return tuple(self.board)


class MinimaxAgent:
    """
    Implements the Minimax algorithm with optional Alpha-Beta pruning.
    """
    def __init__(self, use_alpha_beta=True):
        """
        Initializes the agent.
        Args:
            use_alpha_beta (bool): Whether to use Alpha-Beta pruning.
        """
        self.use_alpha_beta = use_alpha_beta
        self.nodes_expanded = 0 # For performance metrics

    def get_best_move(self, game, state, player):
        """
        Public method to get the best move for the current player.
        Resets node counter and initiates the search.
        """
        self.nodes_expanded = 0
        start_time = time.time()

        if self.use_alpha_beta:
            print("AI is thinking (using Alpha-Beta Pruning)...")
            _, best_move = self._minimax_alpha_beta(game, state, player, -math.inf, math.inf)
        else:
            print("AI is thinking (using standard Minimax)...")
            _, best_move = self._minimax(game, state, player)

        end_time = time.time()
        print(f"AI decision time: {end_time - start_time:.4f} seconds")
        print(f"Nodes expanded: {self.nodes_expanded}")

        return best_move

    def _minimax(self, game, state, player):
        """
        Standard Minimax algorithm.
        Returns a tuple (utility, best_move_index).
        """
        self.nodes_expanded += 1
        max_player = 'O'  # AI is the maximizing player
        other_player = 'X' if player == 'O' else 'O'

        # Check for terminal states
        if game.current_winner == other_player:
            # If the previous move made the *other* player win, it's bad for us.
            # We return utility from the perspective of the player who just moved? No.
            # Utility should be from the perspective of the MAX player at the *leaf*.
            # If we are simulating a move that leads to MIN winning, that state is bad for MAX.
            if other_player == max_player: # Means MAX just won on this simulated move
                 return (1, None) # Good for MAX
            else: # Means MIN just won
                return (-1, None) # Bad for MAX
        elif game.is_board_full():
            return (0, None) # Draw

        moves = game.available_moves()

        if player == max_player: # Maximizing player (AI)
            best_utility = -math.inf
            best_move = moves[0]
            for move in moves:
                # Make a move on a copy of the game state
                game_copy = self._copy_game(game)
                game_copy.make_move(move, player)
                utility, _ = self._minimax(game_copy, state, other_player)
                if utility > best_utility:
                    best_utility = utility
                    best_move = move
            return (best_utility, best_move)

        else: # Minimizing player (Human)
            best_utility = math.inf
            best_move = moves[0]
            for move in moves:
                game_copy = self._copy_game(game)
                game_copy.make_move(move, player)
                utility, _ = self._minimax(game_copy, state, max_player)
                if utility < best_utility:
                    best_utility = utility
                    best_move = move
            return (best_utility, best_move)


    def _minimax_alpha_beta(self, game, state, player, alpha, beta):
        """
        Minimax algorithm with Alpha-Beta pruning.
        Returns a tuple (utility, best_move_index).
        """
        self.nodes_expanded += 1
        max_player = 'O'
        other_player = 'X' if player == 'O' else 'O'

        # Terminal state check (same as standard minimax)
        if game.current_winner == other_player:
            if other_player == max_player:
                 return (1, None)
            else:
                return (-1, None)
        elif game.is_board_full():
            return (0, None)

        moves = game.available_moves()

        if player == max_player: # Maximizing player
            best_utility = -math.inf
            best_move = moves[0]
            for move in moves:
                game_copy = self._copy_game(game)
                game_copy.make_move(move, player)
                utility, _ = self._minimax_alpha_beta(game_copy, state, other_player, alpha, beta)
                if utility > best_utility:
                    best_utility = utility
                    best_move = move
                # Alpha-Beta Pruning
                alpha = max(alpha, best_utility)
                if beta <= alpha:
                    # print(f"Pruned at depth for MAX player with alpha={alpha}, beta={beta}")
                    break
            return (best_utility, best_move)

        else: # Minimizing player
            best_utility = math.inf
            best_move = moves[0]
            for move in moves:
                game_copy = self._copy_game(game)
                game_copy.make_move(move, player)
                utility, _ = self._minimax_alpha_beta(game_copy, state, max_player, alpha, beta)
                if utility < best_utility:
                    best_utility = utility
                    best_move = move
                # Alpha-Beta Pruning
                beta = min(beta, best_utility)
                if beta <= alpha:
                    # print(f"Pruned at depth for MIN player with alpha={alpha}, beta={beta}")
                    break
            return (best_utility, best_move)


    def _copy_game(self, game):
        """Creates a deep copy of the game for state simulation."""
        game_copy = TicTacToe()
        game_copy.board = game.board.copy()
        game_copy.current_winner = game.current_winner
        return game_copy


def play_game(ai_starts=True, use_alpha_beta=True):
    """
    Main game loop for human vs. AI.
    """
    game = TicTacToe()
    agent = MinimaxAgent(use_alpha_beta=use_alpha_beta)

    human_letter = 'X'
    ai_letter = 'O'

    if ai_starts:
        current_player = ai_letter
        print("AI (O) starts the game.")
    else:
        current_player = human_letter
        print("Human (X) starts the game.")

    game.display_board_with_indices()
    game.display_board()

    while True:
        print(f"\n--- {current_player}'s turn ---")

        if current_player == human_letter:
            # Human move
            valid_move = False
            while not valid_move:
                try:
                    move_str = input("Enter your move (1-9): ")
                    move = int(move_str) - 1
                    if move < 0 or move > 8:
                        print("Please enter a number between 1 and 9.")
                    elif not game.is_empty_square(move):
                        print("That square is already taken. Choose another.")
                    else:
                        valid_move = True
                except ValueError:
                    print("Invalid input. Please enter a number.")

            game.make_move(move, human_letter)

        else:
            # AI move
            move = agent.get_best_move(game, game.get_board_state(), ai_letter)
            if move is not None:
                game.make_move(move, ai_letter)
                print(f"AI chose square {move + 1}")
            else:
                # This should not happen if there are available moves, but as a safeguard
                print("AI has no moves left?")
                break

        game.display_board()

        # Check for game end
        if game.current_winner == ai_letter:
            print("\n*** AI (O) wins! ***")
            break
        elif game.current_winner == human_letter:
            print("\n*** Congratulations! You (X) win! ***")
            break
        elif game.is_board_full():
            print("\n*** It's a draw! ***")
            break

        # Switch players
        current_player = human_letter if current_player == ai_letter else ai_letter


if __name__ == "__main__":
    print("="*40)
    print("   Welcome to Tic-Tac-Toe: Human vs. AI")
    print("="*40)
    print("You are 'X'. The AI is 'O'.")

    # --- Configuration ---
    while True:
        start_choice = input("\nWho should start? (1 for Human, 2 for AI): ")
        if start_choice == '1':
            ai_starts = False
            break
        elif start_choice == '2':
            ai_starts = True
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    while True:
        algo_choice = input("Use Alpha-Beta pruning? (y/n): ").lower()
        if algo_choice == 'y':
            use_alpha_beta = True
            break
        elif algo_choice == 'n':
            use_alpha_beta = False
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")

    # --- Start the game ---
    print("\n" + "="*40)
    play_game(ai_starts=ai_starts, use_alpha_beta=use_alpha_beta)
    print("\nGame Over.")