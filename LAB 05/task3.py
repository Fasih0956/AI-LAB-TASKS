graph = {
'A': {'B': 2, 'D': 1},
'B': {'C': 4, 'E': 1, 'A': 2, 'D': 2},
'C': {'B': 4, 'E': 3, 'F': 6},
'D': {'A': 1, 'B': 2, 'E': 2},
'E': {'D': 2, 'B': 1, 'C': 3, 'F': 2},
'F': {'E': 2, 'C': 6}
}
# estimated heuristics because not provided
heuristic = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 7, 'F': 0}
def greedy_bfs(graph, start, goal):
    frontier = [(start, heuristic[start])]   # (node, heuristic)
    visited = set()
    came_from = {start: None}

    while frontier:
        frontier.sort(key=lambda x: x[1])
        current_node, _ = frontier.pop(0)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == goal:
            path = []

            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()

            print(f"Goal found with GBFS. Path: {path}\n")
            return

        for neighbor in graph[current_node]:

            if neighbor not in visited:
                came_from[neighbor] = current_node
                frontier.append((neighbor, heuristic[neighbor]))

    print("\nGoal not found")

greedy_bfs(graph, 'A', 'F')