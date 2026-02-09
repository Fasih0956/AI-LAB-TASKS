class Environment:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_winner = None

    def display(self):
        for row in self.board:
            print('|'.join(row))
            print('-'*5)
        print()

    def empty_cells(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            if self.check_winner(player):
                self.current_winner = player
            return True
        return False

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3)) and self.current_winner is None

class GoalBasedAgent:
    def __init__(self, player_symbol):
        self.player = player_symbol
        self.opponent = 'O' if player_symbol == 'X' else 'X'

    def best_move(self, env):
        for row, col in env.empty_cells():
            env.board[row][col] = self.player
            if env.check_winner(self.player):
                env.board[row][col] = ' '
                return (row, col)
            env.board[row][col] = ' '

        for row, col in env.empty_cells():
            env.board[row][col] = self.opponent
            if env.check_winner(self.opponent):
                env.board[row][col] = ' '
                return (row, col)
            env.board[row][col] = ' '

        if (1,1) in env.empty_cells():
            return (1,1) 
        for move in [(0,0),(0,2),(2,0),(2,2)]:
            if move in env.empty_cells():
                return move
        return env.empty_cells()[0]

env = Environment()
agent_X = GoalBasedAgent('X')
agent_O = GoalBasedAgent('O')

turn = 'X'

print("Initial Board:")
env.display()

while not env.current_winner and not env.is_draw():
    if turn == 'X':
        row, col = agent_X.best_move(env)
        env.make_move(row, col, 'X')
    else:
        row, col = agent_O.best_move(env)
        env.make_move(row, col, 'O')

    print(f"After {turn}'s move:")
    env.display()

    if env.current_winner:
        print(f"Winner: {env.current_winner}")
        break
    elif env.is_draw():
        print("The game is a draw!")
        break

    turn = 'O' if turn == 'X' else 'X'
