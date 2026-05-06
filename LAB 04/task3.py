# We use BFS in this question because it guarantees solution and is complete with reasonable Time and Space complexity
from collections import deque
class EightPuzzleAgent:
    def __init__(self, start_state, goal_state):
        self.start_state = tuple(start_state)
        self.goal_state = tuple(goal_state)
    
    def get_neighbors(self, state):
        blank = state.index(0)
        neighbors = []
        
        moves = {
            0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
            3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
            6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
        }
        
        for new_pos in moves[blank]:
            new_state = list(state)
            new_state[blank], new_state[new_pos] = new_state[new_pos], new_state[blank]
            neighbors.append(tuple(new_state))
        
        return neighbors
    
    def print_state(self, state):
        for i in range(0, 9, 3):
            row = [str(x) if x != 0 else ' ' for x in state[i:i+3]]
            print(f"{' '.join(row)}")
        print()
    
    def solve(self):  #bfs used
        start = self.start_state
        goal = self.goal_state
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current == goal:
                return path
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
if __name__ == "__main__":
    start_state = [7, 2, 4,
                   5, 0, 6,  #0 represent blank
                   8, 3, 1]
    
    goal_state = [0, 1, 2,
                  3, 4, 5,
                  6, 7, 8]
    
    agent = EightPuzzleAgent(start_state, goal_state)
    solution = agent.solve()
    
    if solution:
        for i, state in enumerate(solution):
            print(f"Step {i}:")
            agent.print_state(state)
    else:
        print("No solution exists!")