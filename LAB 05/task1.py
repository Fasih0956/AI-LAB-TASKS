graph = {
'A': {'B': 2, 'D': 1},
'B': {'C': 4, 'E': 1, 'A': 2, 'D': 2},
'C': {'B': 4, 'E': 3, 'F': 6},
'D': {'A': 1, 'B': 2, 'E': 2},
'E': {'D': 2, 'B': 1, 'C': 3, 'F': 2},
'F': {'E': 2, 'C': 6}
}
def ucs(graph, start, goal):
    frontier = [(start, 0)]
    visited = set()
    cost_so_far = {start: 0}
    came_from = {start: None}

    while frontier:
        frontier.sort(key=lambda x: x[1])
        current_node, current_cost = frontier.pop(0)

        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node == goal:
            path = []

            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"Goal found with UCS. Path: {path}, Total Cost: {current_cost}")
            return

        for neighbor, cost in graph[current_node].items():
            new_cost = current_cost + cost

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:

                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current_node
                frontier.append((neighbor, new_cost))

    print("Goal not found")

ucs(graph, 'A', 'F')   # from server A to server F