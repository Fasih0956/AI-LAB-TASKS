def graph_coloring(graph, colors):
    solutions = []
    assignment = {}

    def is_valid(vertex, color):
        for neighbor in graph[vertex]:
            if neighbor in assignment and assignment[neighbor] == color:
                return False
        return True

    def backtrack():
        if len(assignment) == len(graph):
            solutions.append(assignment.copy())
            return

        unassigned = [v for v in graph if v not in assignment]
        vertex = unassigned[0]

        for color in colors:
            if is_valid(vertex, color):
                assignment[vertex] = color
                backtrack()
                del assignment[vertex]

    backtrack()
    return solutions

graph = {
    'A': ['B', 'E'],
    'B': ['A', 'C' , 'D'],
    'C': ['B' , 'D'],
    'D': ['B' , 'C' , 'E'],
    'E': ['A' , 'D']
}

colors = ['Red', 'Green', 'Blue']

solutions = graph_coloring(graph, colors)

print(f"Total Solutions: {len(solutions)}\n")
for i, sol in enumerate(solutions, 1):
    print(f"Solution {i}: {sol}")