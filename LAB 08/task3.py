import math
from typing import Tuple, Optional
import time

class NimGame:
    def __init__(self, pile_size=21):
        self.pile = pile_size
        self.current_player = 1
        self.max_remove = 3
        self.min_remove = 1
        
    def display_state(self):
        print(f"\nPile size: {self.pile}")
        if self.pile > 0:
            print("Objects: " + "● " * self.pile)
    
    def make_move(self, remove_count: int) -> bool:
        if remove_count < self.min_remove or remove_count > self.max_remove:
            return False
        if remove_count > self.pile:
            return False
        
        self.pile -= remove_count
        self.current_player = 3 - self.current_player
        return True
    
    def undo_move(self, remove_count: int):
        self.pile += remove_count
        self.current_player = 3 - self.current_player
    
    def get_valid_moves(self):
        return [i for i in range(self.min_remove, min(self.max_remove, self.pile) + 1)]
    
    def check_winner(self) -> Optional[int]:
        if self.pile == 0:
            return 3 - self.current_player
        return None
    
    def evaluate_position(self, player: int) -> int:
        winner = self.check_winner()
        if winner == player:
            return 100
        elif winner is not None:
            return -100
        
        if self.pile % 4 == 1:
            return -10
        elif self.pile % 4 == 0:
            return 10
        
        return 0

class MinimaxAI:
    def __init__(self, player=1, max_depth=None):
        self.player = player
        self.opponent = 3 - player
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self.name = "Minimax"
    
    def minimax(self, game: NimGame, depth: int, is_maximizing: bool) -> Tuple[int, Optional[int]]:
        self.nodes_evaluated += 1
        
        winner = game.check_winner()
        if winner == self.player:
            return 100 - depth, None
        elif winner == self.opponent:
            return -100 + depth, None
        
        if self.max_depth and depth >= self.max_depth:
            return game.evaluate_position(self.player), None
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return 0, None
        
        if is_maximizing:
            best_score = -math.inf
            best_move = valid_moves[0]
            
            for move in valid_moves:
                game.make_move(move)
                score, _ = self.minimax(game, depth + 1, False)
                game.undo_move(move)
                
                if score > best_score:
                    best_score = score
                    best_move = move
            
            return best_score, best_move
        else:
            best_score = math.inf
            best_move = valid_moves[0]
            
            for move in valid_moves:
                game.make_move(move)
                score, _ = self.minimax(game, depth + 1, True)
                game.undo_move(move)
                
                if score < best_score:
                    best_score = score
                    best_move = move
            
            return best_score, best_move
    
    def get_best_move(self, game: NimGame) -> int:
        self.nodes_evaluated = 0
        _, best_move = self.minimax(game, 0, True)
        return best_move

class AlphaBetaAI:
    def __init__(self, player=1, max_depth=None):
        self.player = player
        self.opponent = 3 - player
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self.name = "Alpha-Beta"
    
    def alphabeta(self, game: NimGame, depth: int, alpha: float, beta: float, 
                  is_maximizing: bool) -> Tuple[int, Optional[int]]:
        self.nodes_evaluated += 1
        
        winner = game.check_winner()
        if winner == self.player:
            return 100 - depth, None
        elif winner == self.opponent:
            return -100 + depth, None
        
        if self.max_depth and depth >= self.max_depth:
            return game.evaluate_position(self.player), None
        
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return 0, None
        
        best_move = valid_moves[0]
        
        if is_maximizing:
            max_score = -math.inf
            
            for move in valid_moves:
                game.make_move(move)
                score, _ = self.alphabeta(game, depth + 1, alpha, beta, False)
                game.undo_move(move)
                
                if score > max_score:
                    max_score = score
                    best_move = move
                
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            
            return max_score, best_move
        else:
            min_score = math.inf
            
            for move in valid_moves:
                game.make_move(move)
                score, _ = self.alphabeta(game, depth + 1, alpha, beta, True)
                game.undo_move(move)
                
                if score < min_score:
                    min_score = score
                    best_move = move
                
                beta = min(beta, score)
                if beta <= alpha:
                    break
            
            return min_score, best_move
    
    def get_best_move(self, game: NimGame) -> int:
        self.nodes_evaluated = 0
        _, best_move = self.alphabeta(game, 0, -math.inf, math.inf, True)
        return best_move

def play_human_vs_ai(ai):
    pile_size = int(input("\nEnter starting pile size (default 21): ") or "21")
    game = NimGame(pile_size)
    human_player = 2
    ai_player = 1
    
    print(f"\nHuman vs {ai.name}")
    print(f"Starting pile: {pile_size} objects")
    print("Remove 1, 2, or 3 objects per turn\n")
    
    game.display_state()
    
    while True:
        if game.current_player == human_player:
            print("\nYour turn")
            while True:
                try:
                    move = input("Remove objects (1-3): ").strip()
                    if move.lower() == 'quit':
                        print("Game ended")
                        return
                    
                    remove_count = int(move)
                    if 1 <= remove_count <= 3 and remove_count <= game.pile:
                        game.make_move(remove_count)
                        break
                    else:
                        print(f"Remove 1-3 objects (max {game.pile})")
                except ValueError:
                    print("Invalid input")
        else:
            print("\nAI thinking...")
            start_time = time.time()
            best_move = ai.get_best_move(game)
            end_time = time.time()
            
            game.make_move(best_move)
            print(f"{ai.name} removed {best_move} objects")
            print(f"Time: {end_time - start_time:.4f}s")
            print(f"Nodes evaluated: {ai.nodes_evaluated}")
        
        game.display_state()
        
        winner = game.check_winner()
        if winner is not None:
            print()
            if winner == ai_player:
                print(f"Game Over: {ai.name} wins")
            else:
                print("Game Over: You win")
            break

def play_ai_vs_ai(ai1, ai2, pile_size=21, display=True):
    game = NimGame(pile_size)
    move_count = 0
    start_time = time.time()
    
    if display:
        print(f"\n{ai1.name} vs {ai2.name}")
        print(f"Starting pile: {pile_size}")
        game.display_state()
    
    while True:
        move_count += 1
        
        if game.current_player == 1:
            move = ai1.get_best_move(game)
            if display:
                print(f"{ai1.name} removes {move} objects")
        else:
            move = ai2.get_best_move(game)
            if display:
                print(f"{ai2.name} removes {move} objects")
        
        game.make_move(move)
        
        if display:
            game.display_state()
        
        winner = game.check_winner()
        if winner is not None:
            end_time = time.time()
            if display:
                print(f"\nGame Over after {move_count} moves")
                if winner == 1:
                    print(f"Winner: {ai1.name}")
                else:
                    print(f"Winner: {ai2.name}")
                print(f"Time: {end_time - start_time:.4f}s")
            
            return {
                'winner': winner,
                'moves': move_count,
                'time': end_time - start_time,
                'ai1_nodes': ai1.nodes_evaluated,
                'ai2_nodes': ai2.nodes_evaluated
            }

def compare_algorithms(num_games=10, pile_size=21):
    print(f"\nComparing Minimax vs Alpha-Beta ({num_games} games)")
    print("=" * 50)
    
    results = {
        'Minimax': {'wins': 0, 'losses': 0, 'total_nodes': 0, 'total_time': 0},
        'Alpha-Beta': {'wins': 0, 'losses': 0, 'total_nodes': 0, 'total_time': 0}
    }
    
    def play_match(match_id):
        if match_id % 2 == 0:
            ai1 = MinimaxAI(player=1)
            ai2 = AlphaBetaAI(player=2)
        else:
            ai1 = AlphaBetaAI(player=1)
            ai2 = MinimaxAI(player=2)
        
        result = play_ai_vs_ai(ai1, ai2, pile_size, display=False)
        
        return {
            'match_id': match_id,
            'winner': ai1.name if result['winner'] == 1 else ai2.name,
            'ai1_name': ai1.name,
            'ai2_name': ai2.name,
            'ai1_nodes': ai1.nodes_evaluated,
            'ai2_nodes': ai2.nodes_evaluated,
            'moves': result['moves'],
            'time': result['time']
        }
    
    for i in range(num_games):
        match_result = play_match(i)
        
        print(f"\nMatch {match_result['match_id'] + 1}: "
              f"{match_result['ai1_name']} vs {match_result['ai2_name']}")
        print(f"  Winner: {match_result['winner']}")
        print(f"  Moves: {match_result['moves']}")
        print(f"  Time: {match_result['time']:.4f}s")
        print(f"  {match_result['ai1_name']} nodes: {match_result['ai1_nodes']}")
        print(f"  {match_result['ai2_name']} nodes: {match_result['ai2_nodes']}")
        
        results[match_result['winner']]['wins'] += 1
        loser = match_result['ai2_name'] if match_result['winner'] == match_result['ai1_name'] else match_result['ai1_name']
        results[loser]['losses'] += 1
        
        results[match_result['ai1_name']]['total_nodes'] += match_result['ai1_nodes']
        results[match_result['ai2_name']]['total_nodes'] += match_result['ai2_nodes']
        results[match_result['ai1_name']]['total_time'] += match_result['time'] / 2
        results[match_result['ai2_name']]['total_time'] += match_result['time'] / 2
    
    print("\n" + "=" * 50)
    print("SUMMARY STATISTICS")
    print("=" * 50)
    
    for algo_name in ['Minimax', 'Alpha-Beta']:
        stats = results[algo_name]
        games_played = stats['wins'] + stats['losses']
        
        print(f"\n{algo_name}:")
        print(f"  Wins: {stats['wins']}")
        print(f"  Losses: {stats['losses']}")
        print(f"  Win Rate: {stats['wins']/games_played*100:.1f}%")
        print(f"  Avg Nodes/Game: {stats['total_nodes']/games_played:,.0f}")
        print(f"  Avg Time/Game: {stats['total_time']/games_played:.4f}s")
    
    minimax_nodes = results['Minimax']['total_nodes']
    alphabeta_nodes = results['Alpha-Beta']['total_nodes']
    if minimax_nodes > 0:
        reduction = (1 - alphabeta_nodes / minimax_nodes) * 100
        print(f"\nAlpha-Beta evaluated {reduction:.1f}% fewer nodes than Minimax")

if __name__ == "__main__":
    print("\nNIM GAME")
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
        
        if ai_choice == '1':
            ai = MinimaxAI(player=1)
        else:
            ai = AlphaBetaAI(player=1)
        
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
        
        ai1 = MinimaxAI(player=1) if ai1_choice == '1' else AlphaBetaAI(player=1)
        ai2 = MinimaxAI(player=2) if ai2_choice == '1' else AlphaBetaAI(player=2)
        
        pile_size = int(input("\nPile size (default 21): ") or "21")
        play_ai_vs_ai(ai1, ai2, pile_size, display=True)
    
    elif choice == '3':
        num_games = int(input("\nNumber of games (default 10): ") or "10")
        pile_size = int(input("Pile size (default 21): ") or "21")
        compare_algorithms(num_games, pile_size)
    
    else:
        print("Invalid choice")