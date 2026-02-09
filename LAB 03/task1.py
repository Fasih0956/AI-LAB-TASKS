import random
class Environment:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [['Dirty' if random.choice([True, False]) else 'Clean' 
                      for _ in range(cols)] for _ in range(rows)]

    def is_dirty(self, x, y):
        return self.grid[x][y] == 'Dirty'

    def clean_cell(self, x, y):
        self.grid[x][y] = 'Clean'

    def display(self):
        for row in self.grid:
            print(' | '.join(row))
        print('-' * (self.cols * 8))

class SimpleReflexAgent:
    def __init__(self, environment):
        self.env = environment
        self.x = 0
        self.y = 0

    def clean_environment(self):
        for i in range(self.env.rows):
            if i % 2 == 0: 
                for j in range(self.env.cols):
                    self.move_to(i, j)
            else: 
                for j in reversed(range(self.env.cols)):
                    self.move_to(i, j)
        print("Cleaning Complete!")

    def move_to(self, x, y):
        self.x = x
        self.y = y
        if self.env.is_dirty(x, y):
            print(f"Cleaning cell ({x}, {y})")
            self.env.clean_cell(x, y)
        self.env.display()

env = Environment(4, 5)  # 4 x 5 grid
robot = SimpleReflexAgent(env)

print("Initial Environment:")
env.display()

robot.clean_environment()
