import random
import copy

def is_solvable(board):
    """An 8-puzzle is solvable iff the number of inversions is even."""
    flat = [n for row in board for n in row if n != 0]
    inversions = sum(
        1 for i in range(len(flat)) for j in range(i + 1, len(flat))
        if flat[i] > flat[j]
    )
    return inversions % 2 == 0

def generate_initial_state():
    numbers = list(range(9))          # 0 = blank
    while True:
        random.shuffle(numbers)
        board = [numbers[i:i+3] for i in range(0, 9, 3)]
        if is_solvable(board):
            return board

# ── Heuristics 
def manhattan_distance(state, goal):
    """
    Manhattan distance is a much stronger heuristic than misplaced
    tiles — it gives a tighter lower bound and guides search more accurately,
    so we get stuck far less often.
    """
    goal_pos = {}
    for i in range(3):
        for j in range(3):
            goal_pos[goal[i][j]] = (i, j)

    dist = 0
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:
                gi, gj = goal_pos[tile]
                dist += abs(i - gi) + abs(j - gj)
    return dist

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def hill_climbing_single(start, goal):
    """One hill-climbing attempt from `start`. Returns (path, solved)."""
    current = start
    path = [current]
    visited = set()
    visited.add(str(current))

    while True:
        h = manhattan_distance(current, goal)
        if h == 0:
            return path, True            

        neighbors = get_neighbors(current)
        neighbors = [n for n in neighbors if str(n) not in visited]

        if not neighbors:
            return path, False    

        neighbors.sort(key=lambda n: manhattan_distance(n, goal))
        best_h = manhattan_distance(neighbors[0], goal)

        if best_h >= h:
            return path, False      

        current = neighbors[0]
        visited.add(str(current))
        path.append(current)

def hill_climbing_with_restarts(goal, max_restarts=1000):
    """
    FIX 4: Random-restart hill climbing.
    Each restart begins from a freshly generated solvable board.
    This lets us escape local minima that a single run can never leave.
    """
    for attempt in range(1, max_restarts + 1):
        start = generate_initial_state()
        path, solved = hill_climbing_single(start, goal)
        if solved:
            print(f"Solved on attempt {attempt}.")
            return start, path
    print("No solution found within restart limit.")
    return None, []

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
initial_state, path = hill_climbing_with_restarts(goal_state)

if initial_state:
    print("Initial State:")
    for row in initial_state:
        print(row)

    print("\nGoal State:")
    for row in goal_state:
        print(row)

    print(f"\nSolution Path ({len(path) - 1} moves):")
    for step, state in enumerate(path):
        print(f"Step {step}:")
        for row in state:
            print(row)
        print()