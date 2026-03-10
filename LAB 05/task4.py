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

def a_star(graph, start, goal):
    frontier = [(start, 0 + heuristic[start])]  
    visited = set() 
    g_costs = {start: 0} 
    came_from = {start: None} 

    while frontier:
        frontier.sort(key=lambda x: x[1])
        current_node, current_f = frontier.pop(0)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"Goal found with A*. Path: {path}\n")
            return

        for neighbor, cost in graph[current_node].items():
            new_g_cost = g_costs[current_node] + cost
            f_cost = new_g_cost + heuristic[neighbor]

            if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_g_cost
                came_from[neighbor] = current_node
                frontier.append((neighbor, f_cost))

    print("Goal not found.\n")

a_star(graph, 'A', 'F')