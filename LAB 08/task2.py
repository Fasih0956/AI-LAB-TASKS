import numpy as np
import math
from typing import List, Tuple, Optional
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class ConnectFour:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.current_player = 1
        self.last_move = None
        
    def display_board(self):
        print("\n  1   2   3   4   5   6   7")
        print("┌───┬───┬───┬───┬───┬───┬───┐")
        
        for i in range(self.rows):
            print("│", end="")
            for j in range(self.cols):
                if self.board[i][j] == 1:
                    print(" X │", end="")
                elif self.board[i][j] == 2:
                    print(" O │", end="")
                else:
                    print("   │", end="")
            print()
            if i < self.rows - 1:
                print("├───┼───┼───┼───┼───┼───┼───┤")
        
        print("└───┴───┴───┴───┴───┴───┴───┘")
        print("  1   2   3   4   5   6   7\n")
    
    def is_valid_move(self, col: int) -> bool:
        return 0 <= col < self.cols and self.board[0][col] == 0
    
    def get_valid_moves(self) -> List[int]:
        return [col for col in range(self.cols) if self.is_valid_move(col)]
    
    def make_move(self, col: int) -> bool:
        if not self.is_valid_move(col):
            return False
        
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.last_move = (row, col)
                self.current_player = 3 - self.current_player
                return True
        return False
    
    def undo_move(self, col: int):
        for row in range(self.rows):
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                self.current_player = 3 - self.current_player
                break
    
    def check_winner(self) -> Optional[int]:
        if self.last_move is None:
            return None
        
        row, col = self.last_move
        player = self.board[row][col]
        
        directions = [
            [(0, 1), (0, -1)],
            [(1, 0), (-1, 0)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)]
        ]
        
        for dir_pair in directions:
            count = 1
            for dr, dc in dir_pair:
                r, c = row + dr, col + dc
                while 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.board[r][c] == player:
                        count += 1
                        r += dr
                        c += dc
                    else:
                        break
            
            if count >= 4:
                return player
        
        if len(self.get_valid_moves()) == 0:
            return 0
        
        return None
    
    def evaluate_window(self, window: List[int], player: int) -> int:
        opponent = 3 - player
        score = 0
        
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2
        
        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 4
        
        return score
    
    def evaluate_board(self, player: int) -> int:
        winner = self.check_winner()
        if winner == player:
            return 1000
        elif winner == 3 - player:
            return -1000
        elif winner == 0:
            return 0
        
        score = 0
        
        center_array = [int(self.board[i][self.cols // 2]) for i in range(self.rows)]
        center_count = center_array.count(player)
        score += center_count * 3
        
        for r in range(self.rows):
            row_array = [int(self.board[r][c]) for c in range(self.cols)]
            for c in range(self.cols - 3):
                window = row_array[c:c+4]
                score += self.evaluate_window(window, player)
        
        for c in range(self.cols):
            col_array = [int(self.board[r][c]) for r in range(self.rows)]
            for r in range(self.rows - 3):
                window = col_array[r:r+4]
                score += self.evaluate_window(window, player)
        
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)
        
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r+3-i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)
        
        return score

class MinimaxAI:
    def __init__(self, player=1, max_depth=4):
        self.player = player
        self.opponent = 3 - player
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self.name = "Minimax"
    
    def minimax(self, game: ConnectFour, depth: int, is_maximizing: bool) -> Tuple[int, Optional[int]]:
        self.nodes_evaluated += 1
        
        winner = game.check_winner()
        if winner == self.player:
            return 1000 - depth, None
        elif winner == self.opponent:
            return -1000 + depth, None
        elif winner == 0:
            return 0, None
        
        if depth == self.max_depth:
            return game.evaluate_board(self.player), None
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return 0, None
        
        ordered_moves = self.order_moves(valid_moves)
        
        if is_maximizing:
            best_score = -math.inf
            best_move = valid_moves[0]
            
            for col in ordered_moves:
                game.make_move(col)
                score, _ = self.minimax(game, depth + 1, False)
                game.undo_move(col)
                
                if score > best_score:
                    best_score = score
                    best_move = col
            
            return best_score, best_move
        else:
            best_score = math.inf
            best_move = valid_moves[0]
            
            for col in ordered_moves:
                game.make_move(col)
                score, _ = self.minimax(game, depth + 1, True)
                game.undo_move(col)
                
                if score < best_score:
                    best_score = score
                    best_move = col
            
            return best_score, best_move
    
    def order_moves(self, moves: List[int]) -> List[int]:
        center = 3
        return sorted(moves, key=lambda x: abs(x - center))
    
    def get_best_move(self, game: ConnectFour) -> int:
        self.nodes_evaluated = 0
        _, best_move = self.minimax(game, 0, True)
        return best_move

class AlphaBetaAI:
    def __init__(self, player=1, max_depth=6):
        self.player = player
        self.opponent = 3 - player
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self.name = "Alpha-Beta"
    
    def alphabeta(self, game: ConnectFour, depth: int, alpha: float, beta: float, 
                  is_maximizing: bool) -> Tuple[int, Optional[int]]:
        self.nodes_evaluated += 1
        
        winner = game.check_winner()
        if winner == self.player:
            return 1000 - depth, None
        elif winner == self.opponent:
            return -1000 + depth, None
        elif winner == 0:
            return 0, None
        
        if depth == self.max_depth:
            return game.evaluate_board(self.player), None
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return 0, None
        
        best_move = valid_moves[0]
        ordered_moves = self.order_moves(valid_moves)
        
        if is_maximizing:
            max_score = -math.inf
            
            for col in ordered_moves:
                game.make_move(col)
                score, _ = self.alphabeta(game, depth + 1, alpha, beta, False)
                game.undo_move(col)
                
                if score > max_score:
                    max_score = score
                    best_move = col
                
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            
            return max_score, best_move
        else:
            min_score = math.inf
            
            for col in ordered_moves:
                game.make_move(col)
                score, _ = self.alphabeta(game, depth + 1, alpha, beta, True)
                game.undo_move(col)
                
                if score < min_score:
                    min_score = score
                    best_move = col
                
                beta = min(beta, score)
                if beta <= alpha:
                    break
            
            return min_score, best_move
    
    def order_moves(self, moves: List[int]) -> List[int]:
        center = 3
        return sorted(moves, key=lambda x: abs(x - center))
    
    def get_best_move(self, game: ConnectFour) -> int:
        self.nodes_evaluated = 0
        _, best_move = self.alphabeta(game, 0, -math.inf, math.inf, True)
        return best_move

def play_ai_vs_ai(ai1, ai2, display=True):
    game = ConnectFour()
    move_count = 0
    start_time = time.time()
    
    if display:
        print(f"\n{ai1.name} (X) vs {ai2.name} (O)")
        game.display_board()
    
    while True:
        move_count += 1
        
        if game.current_player == 1:
            move = ai1.get_best_move(game)
            if display:
                print(f"{ai1.name} (X) plays column {move + 1}")
        else:
            move = ai2.get_best_move(game)
            if display:
                print(f"{ai2.name} (O) plays column {move + 1}")
        
        if move is not None:
            game.make_move(move)
        
        if display:
            game.display_board()
        
        winner = game.check_winner()
        if winner is not None:
            end_time = time.time()
            if display:
                print(f"\nGame Over after {move_count} moves")
                if winner == 1:
                    print(f"Winner: {ai1.name} (X)")
                elif winner == 2:
                    print(f"Winner: {ai2.name} (O)")
                else:
                    print("Result: Tie")
                print(f"Time: {end_time - start_time:.2f}s")
            
            return {
                'winner': winner,
                'moves': move_count,
                'time': end_time - start_time,
                'ai1_nodes': ai1.nodes_evaluated,
                'ai2_nodes': ai2.nodes_evaluated
            }

def play_human_vs_ai(ai):
    game = ConnectFour()
    human_player = 2
    ai_player = 1
    
    print(f"\nHuman (O) vs {ai.name} (X)")
    print("Enter column numbers 1-7\n")
    
    game.display_board()
    
    while True:
        if game.current_player == human_player:
            print("Your turn (O)")
            while True:
                try:
                    col_input = input("Enter column (1-7): ").strip()
                    if col_input.lower() == 'quit':
                        print("Game ended")
                        return
                    
                    col = int(col_input) - 1
                    if 0 <= col < 7:
                        if game.make_move(col):
                            break
                        else:
                            print("Column is full")
                    else:
                        print("Enter number between 1 and 7")
                except ValueError:
                    print("Invalid input")
        else:
            print("AI thinking...")
            start_time = time.time()
            best_move = ai.get_best_move(game)
            end_time = time.time()
            
            if best_move is not None:
                game.make_move(best_move)
                print(f"{ai.name} played column {best_move + 1}")
                print(f"Time: {end_time - start_time:.2f}s")
                print(f"Nodes evaluated: {ai.nodes_evaluated}")
        
        game.display_board()
        
        winner = game.check_winner()
        if winner is not None:
            if winner == 0:
                print("Game Over: Tie")
            elif winner == ai_player:
                print(f"Game Over: {ai.name} wins")
            else:
                print("Game Over: You win")
            break

def compare_algorithms_concurrent(num_games=5):
    print(f"\nComparing Minimax vs Alpha-Beta ({num_games} games)")
    print("=" * 60)
    
    results = {
        'Minimax': {'wins': 0, 'losses': 0, 'ties': 0, 'total_nodes': 0, 'total_time': 0},
        'Alpha-Beta': {'wins': 0, 'losses': 0, 'ties': 0, 'total_nodes': 0, 'total_time': 0}
    }
    
    def play_match(match_id):
        if match_id % 2 == 0:
            ai1 = MinimaxAI(player=1, max_depth=4)
            ai2 = AlphaBetaAI(player=2, max_depth=4)
        else:
            ai1 = AlphaBetaAI(player=1, max_depth=4)
            ai2 = MinimaxAI(player=2, max_depth=4)
        
        result = play_ai_vs_ai(ai1, ai2, display=False)
        
        if result['winner'] == 1:
            winner_name = ai1.name
            loser_name = ai2.name
        elif result['winner'] == 2:
            winner_name = ai2.name
            loser_name = ai1.name
        else:
            winner_name = 'Tie'
            loser_name = 'Tie'
        
        return {
            'match_id': match_id,
            'winner': winner_name,
            'ai1_name': ai1.name,
            'ai2_name': ai2.name,
            'ai1_nodes': ai1.nodes_evaluated,
            'ai2_nodes': ai2.nodes_evaluated,
            'moves': result['moves'],
            'time': result['time']
        }
    
    with ThreadPoolExecutor(max_workers=min(num_games, 4)) as executor:
        futures = [executor.submit(play_match, i) for i in range(num_games)]
        
        for future in as_completed(futures):
            match_result = future.result()
            
            print(f"\nMatch {match_result['match_id'] + 1}: "
                  f"{match_result['ai1_name']} vs {match_result['ai2_name']}")
            print(f"  Winner: {match_result['winner']}")
            print(f"  Moves: {match_result['moves']}")
            print(f"  Time: {match_result['time']:.2f}s")
            print(f"  {match_result['ai1_name']} nodes: {match_result['ai1_nodes']}")
            print(f"  {match_result['ai2_name']} nodes: {match_result['ai2_nodes']}")
            
            if match_result['winner'] != 'Tie':
                results[match_result['winner']]['wins'] += 1
                loser = match_result['ai2_name'] if match_result['winner'] == match_result['ai1_name'] else match_result['ai1_name']
                results[loser]['losses'] += 1
            else:
                results['Minimax']['ties'] += 1
                results['Alpha-Beta']['ties'] += 1
            
            results[match_result['ai1_name']]['total_nodes'] += match_result['ai1_nodes']
            results[match_result['ai2_name']]['total_nodes'] += match_result['ai2_nodes']
            results[match_result['ai1_name']]['total_time'] += match_result['time'] / 2
            results[match_result['ai2_name']]['total_time'] += match_result['time'] / 2
    
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    
    for algo_name in ['Minimax', 'Alpha-Beta']:
        stats = results[algo_name]
        games_played = stats['wins'] + stats['losses'] + stats['ties']
        
        print(f"\n{algo_name}:")
        print(f"  Wins: {stats['wins']}")
        print(f"  Losses: {stats['losses']}")
        print(f"  Ties: {stats['ties']}")
        print(f"  Win Rate: {stats['wins']/games_played*100:.1f}%")
        print(f"  Avg Nodes/Game: {stats['total_nodes']/games_played:,.0f}")
        print(f"  Avg Time/Game: {stats['total_time']/games_played:.2f}s")
    
    minimax_nodes = results['Minimax']['total_nodes']
    alphabeta_nodes = results['Alpha-Beta']['total_nodes']
    if minimax_nodes > 0:
        reduction = (1 - alphabeta_nodes / minimax_nodes) * 100
        print(f"\nAlpha-Beta evaluated {reduction:.1f}% fewer nodes than Minimax")

if __name__ == "__main__":
    print("\nCONNECT FOUR - Adversarial Search Algorithms")
    print("=" * 50)
    print("\nSelect game mode:")
    print("1. Human vs AI")
    print("2. AI vs AI (Single Game)")
    print("3. Compare Algorithms (Multiple Games)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        print("\nSelect AI algorithm:")
        print("1. Minimax")
        print("2. Alpha-Beta")
        
        ai_choice = input("Enter choice (1 or 2): ").strip()
        
        print("\nSelect difficulty:")
        print("1. Easy (Depth 3)")
        print("2. Medium (Depth 4)")
        print("3. Hard (Depth 5)")
        
        diff_choice = input("Enter choice (1-3): ").strip()
        depth = {'1': 3, '2': 4, '3': 5}.get(diff_choice, 4)
        
        if ai_choice == '1':
            ai = MinimaxAI(player=1, max_depth=depth)
        else:
            ai = AlphaBetaAI(player=1, max_depth=depth)
        
        play_human_vs_ai(ai)
    
    elif choice == '2':
        print("\nSelect AI 1 algorithm:")
        print("1. Minimax")
        print("2. Alpha-Beta")
        ai1_choice = input("Enter choice (1 or 2): ").strip()
        
        print("\nSelect AI 2 algorithm:")
        print("1. Minimax")
        print("2. Alpha-Beta")
        ai2_choice = input("Enter choice (1 or 2): ").strip()
        
        ai1 = MinimaxAI(player=1, max_depth=4) if ai1_choice == '1' else AlphaBetaAI(player=1, max_depth=4)
        ai2 = MinimaxAI(player=2, max_depth=4) if ai2_choice == '1' else AlphaBetaAI(player=2, max_depth=4)
        
        play_ai_vs_ai(ai1, ai2, display=True)
    
    elif choice == '3':
        num_games = int(input("\nNumber of games (default 5): ") or "5")
        compare_algorithms_concurrent(num_games)
    
    else:
        print("Invalid choice")