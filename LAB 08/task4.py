import math
import time
from typing import List, Tuple, Optional

class MancalaGame:
    def __init__(self):
        self.pits_per_player = 6
        self.stones_per_pit = 4
        self.board = [self.stones_per_pit] * self.pits_per_player + [0] + \
                     [self.stones_per_pit] * self.pits_per_player + [0]
        self.current_player = 0
        self.player1_mancala = 6
        self.player2_mancala = 13
        
    def display_board(self):
        print("\n    ", end="")
        for i in range(self.pits_per_player, 0, -1):
            print(f"{self.board[12-i]:2d} ", end="")
        print("\n", end="")
        
        print(f"{self.board[13]:2d}", end="")
        print(" " * (self.pits_per_player * 3 + 1), end="")
        print(f"{self.board[6]:2d}")
        
        print("    ", end="")
        for i in range(self.pits_per_player):
            print(f"{self.board[i]:2d} ", end="")
        print("\n")
    
    def get_valid_moves(self) -> List[int]:
        if self.current_player == 0:
            return [i for i in range(0, self.pits_per_player) if self.board[i] > 0]
        else:
            return [i for i in range(7, 7 + self.pits_per_player) if self.board[i] > 0]
    
    def make_move(self, pit: int) -> bool:
        if pit not in self.get_valid_moves():
            return False
        
        stones = self.board[pit]
        self.board[pit] = 0
        current_pos = pit
        
        while stones > 0:
            current_pos = (current_pos + 1) % 14
            
            if self.current_player == 0 and current_pos == 13:
                continue
            if self.current_player == 1 and current_pos == 6:
                continue
            
            self.board[current_pos] += 1
            stones -= 1
        
        if self.current_player == 0 and current_pos == 6:
            return True
        elif self.current_player == 1 and current_pos == 13:
            return True
        
        if self.board[current_pos] == 1:
            if self.current_player == 0 and 0 <= current_pos <= 5:
                opposite_pos = 12 - current_pos
                if self.board[opposite_pos] > 0:
                    self.board[6] += self.board[current_pos] + self.board[opposite_pos]
                    self.board[current_pos] = 0
                    self.board[opposite_pos] = 0
            elif self.current_player == 1 and 7 <= current_pos <= 12:
                opposite_pos = 12 - current_pos
                if self.board[opposite_pos] > 0:
                    self.board[13] += self.board[current_pos] + self.board[opposite_pos]
                    self.board[current_pos] = 0
                    self.board[opposite_pos] = 0
        
        self.current_player = 1 - self.current_player
        return True
    
    def check_winner(self) -> Optional[int]:
        player1_empty = all(self.board[i] == 0 for i in range(6))
        player2_empty = all(self.board[i] == 0 for i in range(7, 13))
        
        if player1_empty or player2_empty:
            for i in range(6):
                self.board[6] += self.board[i]
                self.board[i] = 0
            for i in range(7, 13):
                self.board[13] += self.board[i]
                self.board[i] = 0
            
            if self.board[6] > self.board[13]:
                return 0
            elif self.board[13] > self.board[6]:
                return 1
            else:
                return 2
        return None
    
    def evaluate_board(self, player: int) -> int:
        winner = self.check_winner()
        if winner == player:
            return 1000
        elif winner == 1 - player:
            return -1000
        elif winner == 2:
            return 0
        
        if player == 0:
            score = self.board[6] - self.board[13]
        else:
            score = self.board[13] - self.board[6]
        
        for i in range(6):
            if self.board[i] > 0:
                score += self.board[i] * 0.1
        for i in range(7, 13):
            if self.board[i] > 0:
                score -= self.board[i] * 0.1
        
        return score
    
    def clone(self):
        new_game = MancalaGame()
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        return new_game

class MinimaxAI:
    def __init__(self, player=0, max_depth=5):
        self.player = player
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self.name = "Minimax"
    
    def minimax(self, game: MancalaGame, depth: int, is_maximizing: bool) -> Tuple[float, Optional[int]]:
        self.nodes_evaluated += 1
        
        winner = game.check_winner()
        if winner is not None:
            if winner == self.player:
                return 1000 - depth, None
            elif winner == 1 - self.player:
                return -1000 + depth, None
            else:
                return 0, None
        
        if depth >= self.max_depth:
            return game.evaluate_board(self.player), None
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return game.evaluate_board(self.player), None
        
        if is_maximizing:
            best_score = -math.inf
            best_move = valid_moves[0]
            
            for move in valid_moves:
                game_copy = game.clone()
                extra_turn = game_copy.make_move(move)
                
                if extra_turn:
                    score, _ = self.minimax(game_copy, depth + 1, True)
                else:
                    score, _ = self.minimax(game_copy, depth + 1, False)
                
                if score > best_score:
                    best_score = score
                    best_move = move
            
            return best_score, best_move
        else:
            best_score = math.inf
            best_move = valid_moves[0]
            
            for move in valid_moves:
                game_copy = game.clone()
                extra_turn = game_copy.make_move(move)
                
                if extra_turn:
                    score, _ = self.minimax(game_copy, depth + 1, False)
                else:
                    score, _ = self.minimax(game_copy, depth + 1, True)
                
                if score < best_score:
                    best_score = score
                    best_move = move
            
            return best_score, best_move
    
    def get_best_move(self, game: MancalaGame) -> int:
        self.nodes_evaluated = 0
        _, best_move = self.minimax(game, 0, True)
        return best_move

class AlphaBetaAI:
    def __init__(self, player=0, max_depth=7):
        self.player = player
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self.name = "Alpha-Beta"
    
    def alphabeta(self, game: MancalaGame, depth: int, alpha: float, beta: float, 
                  is_maximizing: bool) -> Tuple[float, Optional[int]]:
        self.nodes_evaluated += 1
        
        winner = game.check_winner()
        if winner is not None:
            if winner == self.player:
                return 1000 - depth, None
            elif winner == 1 - self.player:
                return -1000 + depth, None
            else:
                return 0, None
        
        if depth >= self.max_depth:
            return game.evaluate_board(self.player), None
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return game.evaluate_board(self.player), None
        
        ordered_moves = self.order_moves(game, valid_moves)
        best_move = ordered_moves[0]
        
        if is_maximizing:
            max_score = -math.inf
            
            for move in ordered_moves:
                game_copy = game.clone()
                extra_turn = game_copy.make_move(move)
                
                if extra_turn:
                    score, _ = self.alphabeta(game_copy, depth + 1, alpha, beta, True)
                else:
                    score, _ = self.alphabeta(game_copy, depth + 1, alpha, beta, False)
                
                if score > max_score:
                    max_score = score
                    best_move = move
                
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            
            return max_score, best_move
        else:
            min_score = math.inf
            
            for move in ordered_moves:
                game_copy = game.clone()
                extra_turn = game_copy.make_move(move)
                
                if extra_turn:
                    score, _ = self.alphabeta(game_copy, depth + 1, alpha, beta, False)
                else:
                    score, _ = self.alphabeta(game_copy, depth + 1, alpha, beta, True)
                
                if score < min_score:
                    min_score = score
                    best_move = move
                
                beta = min(beta, score)
                if beta <= alpha:
                    break
            
            return min_score, best_move
    
    def order_moves(self, game: MancalaGame, moves: List[int]) -> List[int]:
        move_scores = []
        for move in moves:
            game_copy = game.clone()
            extra_turn = game_copy.make_move(move)
            score = 0
            
            if extra_turn:
                score += 50
            if game.player == 0 and move <= 5:
                score += (6 - move)
            elif game.player == 1 and move >= 7:
                score += (move - 6)
            
            move_scores.append((score, move))
        
        move_scores.sort(reverse=True)
        return [move for _, move in move_scores]
    
    def get_best_move(self, game: MancalaGame) -> int:
        self.nodes_evaluated = 0
        _, best_move = self.alphabeta(game, 0, -math.inf, math.inf, True)
        return best_move

def play_human_vs_ai(ai):
    game = MancalaGame()
    human_player = 1
    ai_player = 0
    
    print(f"\nHuman vs {ai.name}")
    print("You are Player 2 (bottom row)")
    print("Enter pit number (1-6) for your move\n")
    
    game.display_board()
    
    while True:
        if game.current_player == human_player:
            print("Your turn")
            while True:
                try:
                    move = input("Select pit (1-6): ").strip()
                    if move.lower() == 'quit':
                        print("Game ended")
                        return
                    
                    pit = int(move) - 1 + 7
                    if pit in game.get_valid_moves():
                        extra_turn = game.make_move(pit)
                        break
                    else:
                        print("Invalid move")
                except ValueError:
                    print("Invalid input")
        else:
            print("AI thinking...")
            start_time = time.time()
            best_move = ai.get_best_move(game)
            end_time = time.time()
            
            extra_turn = game.make_move(best_move)
            print(f"{ai.name} selected pit {best_move + 1}")
            print(f"Time: {end_time - start_time:.2f}s")
            print(f"Nodes evaluated: {ai.nodes_evaluated}")
            
            if extra_turn:
                print(f"{ai.name} gets another turn")
        
        game.display_board()
        
        winner = game.check_winner()
        if winner is not None:
            print()
            if winner == ai_player:
                print(f"Game Over: {ai.name} wins")
                print(f"Score: AI {game.board[6]} - {game.board[13]} Human")
            elif winner == human_player:
                print("Game Over: You win")
                print(f"Score: Human {game.board[13]} - {game.board[6]} AI")
            else:
                print("Game Over: Tie")
                print(f"Score: {game.board[6]} - {game.board[13]}")
            break

def play_ai_vs_ai(ai1, ai2, display=True):
    game = MancalaGame()
    move_count = 0
    start_time = time.time()
    
    if display:
        print(f"\n{ai1.name} (Player 1) vs {ai2.name} (Player 2)")
        game.display_board()
    
    while True:
        move_count += 1
        
        if game.current_player == 0:
            move = ai1.get_best_move(game)
            extra_turn = game.make_move(move)
            if display:
                print(f"{ai1.name} plays pit {move + 1}")
                if extra_turn:
                    print(f"{ai1.name} gets another turn")
        else:
            move = ai2.get_best_move(game)
            extra_turn = game.make_move(move)
            if display:
                print(f"{ai2.name} plays pit {move - 6}")
                if extra_turn:
                    print(f"{ai2.name} gets another turn")
        
        if display:
            game.display_board()
        
        winner = game.check_winner()
        if winner is not None:
            end_time = time.time()
            if display:
                print(f"\nGame Over after {move_count} moves")
                if winner == 0:
                    print(f"Winner: {ai1.name}")
                elif winner == 1:
                    print(f"Winner: {ai2.name}")
                else:
                    print("Result: Tie")
                print(f"Final Score: {game.board[6]} - {game.board[13]}")
                print(f"Time: {end_time - start_time:.2f}s")
            
            return {
                'winner': winner,
                'moves': move_count,
                'time': end_time - start_time,
                'score_p1': game.board[6],
                'score_p2': game.board[13],
                'ai1_nodes': ai1.nodes_evaluated,
                'ai2_nodes': ai2.nodes_evaluated
            }

def compare_algorithms(num_games=5):
    print(f"\nComparing Minimax vs Alpha-Beta ({num_games} games)")
    print("=" * 60)
    
    results = {
        'Minimax': {'wins': 0, 'losses': 0, 'ties': 0, 'total_nodes': 0, 'total_time': 0, 'total_score': 0},
        'Alpha-Beta': {'wins': 0, 'losses': 0, 'ties': 0, 'total_nodes': 0, 'total_time': 0, 'total_score': 0}
    }
    
    for i in range(num_games):
        if i % 2 == 0:
            ai1 = MinimaxAI(player=0, max_depth=5)
            ai2 = AlphaBetaAI(player=1, max_depth=5)
        else:
            ai1 = AlphaBetaAI(player=0, max_depth=5)
            ai2 = MinimaxAI(player=1, max_depth=5)
        
        result = play_ai_vs_ai(ai1, ai2, display=False)
        
        print(f"\nGame {i + 1}: {ai1.name} vs {ai2.name}")
        print(f"  Score: {result['score_p1']} - {result['score_p2']}")
        print(f"  Winner: ", end="")
        if result['winner'] == 0:
            print(ai1.name)
            results[ai1.name]['wins'] += 1
            results[ai2.name]['losses'] += 1
        elif result['winner'] == 1:
            print(ai2.name)
            results[ai2.name]['wins'] += 1
            results[ai1.name]['losses'] += 1
        else:
            print("Tie")
            results[ai1.name]['ties'] += 1
            results[ai2.name]['ties'] += 1
        
        print(f"  Moves: {result['moves']}")
        print(f"  Time: {result['time']:.2f}s")
        print(f"  {ai1.name} nodes: {result['ai1_nodes']}")
        print(f"  {ai2.name} nodes: {result['ai2_nodes']}")
        
        results[ai1.name]['total_nodes'] += result['ai1_nodes']
        results[ai2.name]['total_nodes'] += result['ai2_nodes']
        results[ai1.name]['total_time'] += result['time'] / 2
        results[ai2.name]['total_time'] += result['time'] / 2
        results[ai1.name]['total_score'] += result['score_p1']
        results[ai2.name]['total_score'] += result['score_p2']
    
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
        print(f"  Avg Score: {stats['total_score']/games_played:.1f}")
        print(f"  Avg Nodes/Game: {stats['total_nodes']/games_played:,.0f}")
        print(f"  Avg Time/Game: {stats['total_time']/games_played:.2f}s")
    
    minimax_nodes = results['Minimax']['total_nodes']
    alphabeta_nodes = results['Alpha-Beta']['total_nodes']
    if minimax_nodes > 0:
        reduction = (1 - alphabeta_nodes / minimax_nodes) * 100
        print(f"\nAlpha-Beta evaluated {reduction:.1f}% fewer nodes than Minimax")

if __name__ == "__main__":
    print("\nMANCALA GAME")
    print("=" * 50)
    print("\nSelect game mode:")
    print("1. Human vs AI")
    print("2. AI vs AI")
    print("3. Compare Algorithms")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        print("\nSelect AI algorithm:")
        print("1. Minimax")
        print("2. Alpha-Beta")
        
        ai_choice = input("Enter choice (1 or 2): ").strip()
        
        print("\nSelect difficulty:")
        print("1. Easy (Depth 3)")
        print("2. Medium (Depth 5)")
        print("3. Hard (Depth 7)")
        
        diff_choice = input("Enter choice (1-3): ").strip()
        depth = {'1': 3, '2': 5, '3': 7}.get(diff_choice, 5)
        
        if ai_choice == '1':
            ai = MinimaxAI(player=0, max_depth=depth)
        else:
            ai = AlphaBetaAI(player=0, max_depth=depth)
        
        play_human_vs_ai(ai)
    
    elif choice == '2':
        print("\nSelect AI 1:")
        print("1. Minimax")
        print("2. Alpha-Beta")
        ai1_choice = input("Enter choice (1 or 2): ").strip()
        
        print("\nSelect AI 2:")
        print("1. Minimax")
        print("2. Alpha-Beta")
        ai2_choice = input("Enter choice (1 or 2): ").strip()
        
        ai1 = MinimaxAI(player=0, max_depth=5) if ai1_choice == '1' else AlphaBetaAI(player=0, max_depth=5)
        ai2 = MinimaxAI(player=1, max_depth=5) if ai2_choice == '1' else AlphaBetaAI(player=1, max_depth=5)
        
        play_ai_vs_ai(ai1, ai2, display=True)
    
    elif choice == '3':
        num_games = int(input("\nNumber of games (default 5): ") or "5")
        compare_algorithms(num_games)
    
    else:
        print("Invalid choice")