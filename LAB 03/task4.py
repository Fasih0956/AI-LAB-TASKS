class Environment:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def set_obstacles(self, obstacle_positions):
        for (x, y) in obstacle_positions:
            if 0 <= x < self.rows and 0 <= y < self.cols:
                self.grid[x][y] = 1

    def is_free(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] == 0

    def display(self, agent_pos=None, path=[]):
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                if agent_pos == (i, j):
                    row += "A " # current pos
                elif (i, j) in path:
                    row += "* "  # Path
                elif self.grid[i][j] == 1:
                    row += "X "  # Obstacle
                else:
                    row += ". "
            print(row)
        print()

class UtilityAgent:
    def __init__(self, environment):
        self.env = environment

    def shortest_path(self, start, goal):
        from collections import deque  

        queue = deque([start])
        visited = {start: None}

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        while queue:
            current = queue.popleft()
            if current == goal:
                break

            for dx, dy in directions:
                nx, ny = current[0] + dx, current[1] + dy
                if self.env.is_free(nx, ny) and (nx, ny) not in visited:
                    visited[(nx, ny)] = current
                    queue.append((nx, ny))

        path = []
        node = goal
        if node not in visited:
            return [], float('inf')

        while node is not None:
            path.insert(0, node)
            node = visited[node]

        return path, len(path) - 1
    
    def move(self, start, goal):
        path, distance = self.shortest_path(start, goal)
        if not path:
            print("No path to destination!")
            return

        for pos in path:
            self.env.display(agent_pos=pos, path=path)
            print(f"Moving to {pos}...\n")

env = Environment(5, 6)  # 5 x 6 grid
env.set_obstacles([(1, 2), (2, 2), (3, 4)])

agent = UtilityAgent(env)

print("Initial Grid:")
env.display()

# Agent moves from (0,0) to (4,5)
agent.move((0, 0), (4, 5))
