import heapq
graph = {
    'A': [('B', 3), ('C', 4), ('D',6),('E',30)],
    'B': [('A', 3), ('C', 6),('D',5),('E',7)],
    'C': [('A', 4),('B',6),('D',8),('E',9)],
    'D': [('A', 6), ('B', 5),('C',8),('E',10)],
    'E': [('A', 30), ('B', 7), ('C',9),('D',10)]
}
def beam_search(start, beam_width=2):
    num_nodes = len(graph)
    beam = [(0, [start], {start})]

    while beam:
        candidates = []
        for cost, path, visited in beam:
            current_node = path[-1]

            if len(visited) == num_nodes:
                return path + [start], cost + dict(graph[current_node])[start]

            for neighbor, edge_cost in graph[current_node]:
                if neighbor not in visited:
                    new_cost = cost + edge_cost
                    new_path = path + [neighbor]
                    new_visited = visited | {neighbor}
                    candidates.append((new_cost, new_path, new_visited))

        beam = heapq.nsmallest(beam_width, candidates, key=lambda x: x[0])

    return None, float('inf')

start_node = 'A'
beam_width = 4
path, cost = beam_search(start=start_node, beam_width=beam_width)

if path:
    print(f"Path found: {' → '.join(path)} with total cost: {cost}")
else:
    print("No path found.")