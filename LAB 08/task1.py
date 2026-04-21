import numpy as np
import math
from typing import List, Tuple, Optional
import random

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X' # always first
        
    def display_board(self):
        """Display the current board state"""
        print("\n    0   1   2")
        print("  ┌───┬───┬───┐")
        for i, row in enumerate(self.board):
            print(f"{i} │", end=" ")
            print(" │ ".join(row), end=" ")
            print("│")
            if i < 2:
                print("  ├───┼───┼───┤")
        print("  └───┴───┴───┘\n")
    
    def make_move(self, row: int, col: int) -> bool:
        """Make a move on the board"""
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def undo_move(self, row: int, col: int):
        """Undo a move (useful for minimax)"""
        self.board[row][col] = ' '
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Return list of empty cell coordinates"""
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
    
    def check_winner(self) -> Optional[str]:
        """Check if there's a winner. Returns 'X', 'O', 'Tie', or None"""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        # Check for tie
        if not self.get_empty_cells():
            return 'Tie'
        
        return None
    
    def evaluate_board(self, player: str) -> Optional[int]:
        """Evaluate board state for minimax"""
        winner = self.check_winner()
        if winner == player:
            return 1   # AI wins
        elif winner != player and winner not in [None, 'Tie']:
            return -1
        elif winner == 'Tie':
            return 0
        return None

class MinimaxAI:
    def __init__(self, player='X'):
        self.player = player
        self.opponent = 'O' if player == 'X' else 'X'
    
    def minimax(self, game: TicTacToe, depth: int, is_maximizing: bool) -> int:
        """Minimax algorithm with depth consideration"""
        score = game.evaluate_board(self.player)
        
        # Terminal states
        if score is not None:
            if score == 1:
                return score - depth
            elif score == -1:
                return score + depth 
            return 0
        
        if is_maximizing:
            best_score = -math.inf
            for row, col in game.get_empty_cells():
                game.make_move(row, col)
                score = self.minimax(game, depth + 1, False)
                game.undo_move(row, col)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row, col in game.get_empty_cells():
                game.make_move(row, col)
                score = self.minimax(game, depth + 1, True)
                game.undo_move(row, col)
                best_score = min(score, best_score)
            return best_score
    
    def get_best_move(self, game: TicTacToe) -> Tuple[int, int]:
        """Find the best move using minimax"""
        best_score = -math.inf
        best_move = None
        
        for row, col in game.get_empty_cells():
            game.make_move(row, col)
            score = self.minimax(game, 0, False)
            game.undo_move(row, col)
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move

class AlphaBetaAI:
    def __init__(self, player='X'):
        self.player = player
        self.opponent = 'O' if player == 'X' else 'X'
        self.nodes_evaluated = 0
    
    def alphabeta(self, game: TicTacToe, depth: int, alpha: float, beta: float, 
                  is_maximizing: bool) -> int:
        """Alpha-beta pruning algorithm"""
        self.nodes_evaluated += 1
        score = game.evaluate_board(self.player)
        
        if score is not None:
            if score == 1:
                return score - depth  # Prefer quicker wins
            elif score == -1:
                return score + depth  # Prefer slower losses
            return 0
        
        if is_maximizing:
            max_score = -math.inf
            for row, col in game.get_empty_cells():
                game.make_move(row, col)
                score = self.alphabeta(game, depth + 1, alpha, beta, False)
                game.undo_move(row, col)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_score
        else:
            min_score = math.inf
            for row, col in game.get_empty_cells():
                game.make_move(row, col)
                score = self.alphabeta(game, depth + 1, alpha, beta, True)
                game.undo_move(row, col)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_score
    
    def get_best_move(self, game: TicTacToe) -> Tuple[int, int]:
        """Find the best move using alpha-beta pruning"""
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf
        self.nodes_evaluated = 0
        
        for row, col in game.get_empty_cells():
            game.make_move(row, col)
            score = self.alphabeta(game, 0, alpha, beta, False)
            game.undo_move(row, col)
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
            alpha = max(alpha, score)
        
        return best_move

class GameController:
    def __init__(self, ai_algorithm='alphabeta'):
        self.game = TicTacToe()
        self.ai_algorithms = {
            'minimax': MinimaxAI('X'),
            'alphabeta': AlphaBetaAI('X')
        }
        self.ai = self.ai_algorithms[ai_algorithm]
        self.human_player = 'O'
        self.ai_player = 'X'
    
    def play(self):
        """Main game loop"""
        print("\n=== TIC-TAC-TOE: Human vs AI ===")
        print("You are 'O', AI is 'X'")
        print("Enter moves as: row col (e.g., '1 2')\n")
        
        self.game.display_board()
        
        while True:
            if self.game.current_player == self.human_player:
                print("Your turn (O)")
                while True:
                    try:
                        move = input("Enter row and column (0-2): ").split()
                        if len(move) != 2:
                            print("Please enter two numbers separated by space")
                            continue
                        row, col = int(move[0]), int(move[1])
                        if 0 <= row <= 2 and 0 <= col <= 2:
                            if self.game.make_move(row, col):
                                break
                            else:
                                print("Cell already occupied!")
                        else:
                            print("Numbers must be between 0 and 2")
                    except ValueError:
                        print("Invalid input. Please enter numbers only.")
            
            else:
                print("AI thinking...")
                best_move = self.ai.get_best_move(self.game)
                if best_move:
                    self.game.make_move(best_move[0], best_move[1])
                    print(f"AI played at ({best_move[0]}, {best_move[1]})")
                    if isinstance(self.ai, AlphaBetaAI):
                        print(f"Nodes evaluated: {self.ai.nodes_evaluated}")
            
            self.game.display_board()
            winner = self.game.check_winner()
            if winner:
                if winner == 'Tie':
                    print("🤝 Game Over: It's a tie!")
                elif winner == self.ai_player:
                    print("🤖 Game Over: AI wins!")
                else:
                    print("🎉 Game Over: You win!")
                break

def test_ai_vs_ai():
    """Test: AI vs AI game"""
    print("\n=== AI vs AI Demo ===")
    game = TicTacToe()
    ai1 = AlphaBetaAI('X')
    ai2 = MinimaxAI('O')
    
    game.display_board()
    move_count = 0
    
    while True:
        move_count += 1
        if game.current_player == 'X':
            move = ai1.get_best_move(game)
            print(f"AI-1 (X) plays: {move}")
        else:
            move = ai2.get_best_move(game)
            print(f"AI-2 (O) plays: {move}")
        
        if move:
            game.make_move(move[0], move[1])
        
        game.display_board()
        
        winner = game.check_winner()
        if winner:
            print(f"\nGame Over after {move_count} moves!")
            print(f"Result: {winner}")
            break

if __name__ == "__main__":
    print("Choose game mode:")
    print("1. Human vs AI")
    print("2. AI vs AI (Demo)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == '1':
        print("\nChoose AI algorithm:")
        print("1. Minimax")
        print("2. Alpha-Beta Pruning")
        
        ai_choice = input("Enter choice (1 or 2): ").strip()
        ai_type = 'alphabeta' if ai_choice == '2' else 'minimax'
        
        controller = GameController(ai_algorithm=ai_type)
        controller.play()
    else:
        test_ai_vs_ai()