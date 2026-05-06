import heapq
from collections import defaultdict
# we use UCS in this becuase it provides the best optimal solution with lesser time and space complexity and is complete.
class RomanianMapSearch:
    def __init__(self):
        self.graph = {
            'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
            'Zerind': {'Arad': 75, 'Oradea': 71},
            'Oradea': {'Zerind': 71, 'Sibiu': 151},
            'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
            'Timisoara': {'Arad': 118, 'Lugoj': 111},
            'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
            'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
            'Drobeta': {'Mehadia': 75, 'Craiova': 120},
            'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
            'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
            'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
            'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
            'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
            'Giurgiu': {'Bucharest': 90},
            'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
            'Hirsova': {'Urziceni': 98, 'Eforie': 86},
            'Eforie': {'Hirsova': 86},
            'Vaslui': {'Urziceni': 142, 'Iasi': 92},
            'Iasi': {'Vaslui': 92, 'Neamt': 87},
            'Neamt': {'Iasi': 87}
        }
        
        self.heuristics = {   #Assumed
            'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242,
            'Eforie': 161, 'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151,
            'Iasi': 226, 'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
            'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
            'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80,
            'Vaslui': 199, 'Zerind': 374
        }

    def uniform_cost_search(self, start, goal):
        counter = 0
        pq = [(0, counter, start, [start])]
        
        visited = {}
        explored_nodes = []
        
        print(f"\n{'='*70}")
        print(f"UNIFORM COST SEARCH: {start} → {goal}")
        print(f"{'='*70}")
        print(f"{'Step':<6} {'Current Node':<20} {'Path':<40} {'Cost':<8} {'Queue Size'}")
        print(f"{'-'*70}")
        
        step = 0
        
        while pq:
            cost, _, current_node, path = heapq.heappop(pq)
            
            if current_node == goal:
                explored_nodes.append(current_node)
                print(f"{step:<6} {current_node:<20} {' → '.join(path):<40} {cost:<8} GOAL FOUND!")
                print(f"\n{'='*70}")
                return {
                    'path': path,
                    'cost': cost,
                    'explored': explored_nodes,
                    'visited_count': len(visited)
                }
            
            if current_node in visited and visited[current_node] <= cost:
                continue
            
            visited[current_node] = cost
            explored_nodes.append(current_node)
            
            step += 1
            print(f"{step:<6} {current_node:<20} {' → '.join(path):<40} {cost:<8} {len(pq)}")
            
            for neighbor, edge_cost in self.graph.get(current_node, {}).items():
                new_cost = cost + edge_cost
                
                if neighbor not in visited or new_cost < visited[neighbor]:
                    counter += 1
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_cost, counter, neighbor, new_path))
                    
        return None
    
    def visualize_path(self, path, cost):
        print(f"\n{'='*70}")
        print("PATH VISUALIZATION")
        print(f"{'='*70}")
        
        if not path:
            print("No path found!")
            return
        
        for i in range(len(path) - 1):
            city1 = path[i]
            city2 = path[i + 1]
            distance = self.graph[city1][city2]
            h1 = self.heuristics[city1]
            h2 = self.heuristics[city2]
            
            print(f"\n   {city1:20} ---{distance:>3} km---> {city2:20}")
            print(f"   (h={h1} km to Bucharest)      (h={h2} km to Bucharest)")
        
        print(f"\n   {'─'*50}")
        print(f"   Total Distance: {cost} km")
        print(f"   Number of Stops: {len(path) - 1}")
        print(f"   Avg Distance/Stop: {cost/(len(path)-1):.1f} km")

def main():
    romania = RomanianMapSearch()
    
    start_city = 'Arad'
    goal_city = 'Bucharest'
    
    print("\n" + "MAP ROUTE FINDER".center(70))
    print("="*70)
    print(f"Finding optimal route from {start_city} to {goal_city}")
    print(f"Goal: Minimize total travel distance")
    
    result = romania.uniform_cost_search(start_city, goal_city)
    
    if result:
        romania.visualize_path(result['path'], result['cost'])
        
        print(f"\n{'='*70}")
        print("SEARCH STATISTICS")
        print(f"{'='*70}")
        print(f"  Start City: {start_city}")
        print(f"  Goal City: {goal_city}")
        print(f"  Algorithm: Uniform Cost Search (Dijkstra's variant)")
        print(f"  Optimal Path Found: {' → '.join(result['path'])}")
        print(f"  Total Distance: {result['cost']} km")
        print(f"  Number of Stops: {len(result['path']) - 1}")
        print(f"  Cities Explored: {len(result['explored'])}")
        print(f"  Unique Cities Visited: {result['visited_count']}")
        
        straight_line = romania.heuristics[start_city]
        print(f"\n  Efficiency Metrics:")
        print(f"  - Straight-line distance (heuristic): {straight_line} km")
        print(f"  - Actual road distance: {result['cost']} km")
        print(f"  - Route efficiency: {straight_line/result['cost']*100:.1f}%")
        
        # Alternative routes
        print(f"\n{'='*70}")
        print("💡 ALTERNATIVE ROUTES ANALYSIS")
        print(f"{'='*70}")
        
        routes = [
            (['Arad', 'Sibiu', 'Fagaras', 'Bucharest'], 140+99+211),
            (['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest'], 140+80+97+101),
            (['Arad', 'Timisoara', 'Lugoj', 'Mehadia', 'Drobeta', 'Craiova', 'Pitesti', 'Bucharest'], 
             118+111+70+75+120+138+101),
        ]
        
        for i, (route, distance) in enumerate(routes, 1):
            marker = "OPTIMAL" if route == result['path'] else "   "
            print(f"  Route {i}: {marker}")
            print(f"     Path: {' → '.join(route)}")
            print(f"     Distance: {distance} km")
            if route != result['path']:
                print(f"     Extra distance vs optimal: {distance - result['cost']} km")
            print()

if __name__ == "__main__":
    main()