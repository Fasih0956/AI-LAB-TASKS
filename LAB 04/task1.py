import random
from collections import deque
import heapq

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.cost = random.randint(1, 10)  # Random cost for Uniform Cost Search

class BinaryTree:
    def __init__(self):
        self.root = None
        self.nodes = []
        self.create_tree()
    
    def create_tree(self):
        alphabets = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        random.shuffle(alphabets)
        
        for alpha in alphabets:
            self.nodes.append(Node(alpha))
        
        for i in range(len(self.nodes)):
            left_index = 2 * i + 1
            right_index = 2 * i + 2
            
            if left_index < len(self.nodes):
                self.nodes[i].left = self.nodes[left_index]
                self.nodes[left_index].parent = self.nodes[i]
            
            if right_index < len(self.nodes):
                self.nodes[i].right = self.nodes[right_index]
                self.nodes[right_index].parent = self.nodes[i]
        
        self.root = self.nodes[0]
    
    def get_random_node(self):
        return random.choice(self.nodes)
    
    def print_tree(self):
        if not self.root:
            return
        
        queue = deque([(self.root, 0)])
        current_level = 0
        level_nodes = []
        
        while queue:
            node, level = queue.popleft()
            
            if level > current_level:
                print(f"Level {current_level}: {' '.join(level_nodes)}")
                level_nodes = []
                current_level = level
            
            if node:
                level_nodes.append(f"{node.value}({node.cost})")
                queue.append((node.left, level + 1))
                queue.append((node.right, level + 1))
            else:
                level_nodes.append("None")
        
        if level_nodes:
            print(f"Level {current_level}: {' '.join(level_nodes)}")
    
    def bfs(self, start_node, goal_value):
        if not start_node:
            return None, [], 0
        
        visited = set()
        queue = deque([(start_node, [start_node])])
        nodes_explored = 0
        
        while queue:
            current_node, path = queue.popleft()
            nodes_explored += 1
            
            if current_node.value == goal_value:
                return path, [node.value for node in path], nodes_explored
            
            if current_node not in visited:
                visited.add(current_node)
                
                # Add children to queue (left to right for BFS)
                if current_node.left and current_node.left not in visited:
                    queue.append((current_node.left, path + [current_node.left]))
                if current_node.right and current_node.right not in visited:
                    queue.append((current_node.right, path + [current_node.right]))
        
        return None, [], nodes_explored
    
    def dfs(self, start_node, goal_value):
        if not start_node:
            return None, [], 0
        
        visited = set()
        stack = [(start_node, [start_node])]
        nodes_explored = 0
        
        while stack:
            current_node, path = stack.pop()
            nodes_explored += 1
            
            if current_node.value == goal_value:
                return path, [node.value for node in path], nodes_explored
            
            if current_node not in visited:
                visited.add(current_node)
                
                if current_node.right and current_node.right not in visited:
                    stack.append((current_node.right, path + [current_node.right]))
                if current_node.left and current_node.left not in visited:
                    stack.append((current_node.left, path + [current_node.left]))
        
        return None, [], 0
    
    def dls(self, start_node, goal_value, depth_limit):
        if not start_node:
            return None, [], 0
        
        def recursive_dls(node, goal, depth, path, visited, nodes_explored):
            nodes_explored += 1
            
            if node.value == goal:
                return path, nodes_explored
            
            if depth <= 0:
                return None, nodes_explored
            
            visited.add(node)
            
            for child in [node.left, node.right]:
                if child and child not in visited:
                    result, nodes_explored = recursive_dls(
                        child, goal, depth - 1, path + [child], visited.copy(), nodes_explored
                    )
                    if result is not None:
                        return result, nodes_explored
            
            return None, nodes_explored
        
        result, nodes_explored = recursive_dls(start_node, goal_value, depth_limit, [start_node], set(), 0)
        
        if result:
            return result, [node.value for node in result], nodes_explored
        return None, [], nodes_explored
    
    def ids(self, start_node, goal_value, max_depth=10):
        total_nodes_explored = 0
        
        for depth in range(max_depth + 1):
            result_path, path_values, nodes_explored = self.dls(start_node, goal_value, depth)
            total_nodes_explored += nodes_explored
            
            if result_path:
                return result_path, path_values, total_nodes_explored, depth
        
        return None, [], total_nodes_explored, None
    
    def ucs(self, start_node, goal_value):
        if not start_node:
            return None, [], 0
        
        counter = 0  # To handle ties in priority queue
        pq = [(0, counter, start_node, [start_node])]
        visited = set()
        nodes_explored = 0
        
        while pq:
            cost, _, current_node, path = heapq.heappop(pq)
            nodes_explored += 1
            
            if current_node.value == goal_value:
                return path, [node.value for node in path], nodes_explored, cost
            
            if current_node not in visited:
                visited.add(current_node)
                
                for child in [current_node.left, current_node.right]:
                    if child and child not in visited:
                        new_cost = cost + child.cost
                        counter += 1
                        heapq.heappush(pq, (new_cost, counter, child, path + [child]))
        
        return None, [], nodes_explored, 0

def print_path_info(algorithm_name, path_values, nodes_explored, additional_info=None):
    print(f"\n{algorithm_name}:")
    if path_values:
        print(f"  Path found: {' -> '.join(path_values)}")
        print(f"  Path length: {len(path_values)}")
    else:
        print("  Goal not found!")
    print(f"  Nodes explored: {nodes_explored}")
    if additional_info is not None:
        if isinstance(additional_info, tuple):
            for key, value in additional_info:
                print(f"  {key}: {value}")
        else:
            print(f"  {additional_info}")

def main():
    tree = BinaryTree()
    
    print("Binary Tree Structure (with costs):")
    print("-" * 50)
    tree.print_tree()
    start_node = tree.root
    goal_node = tree.get_random_node()
    goal_value = goal_node.value
    
    print(f"\nSearching for goal node: {goal_value}")
    print("=" * 50)
    
    path, path_values, nodes_explored = tree.bfs(start_node, goal_value)
    print_path_info("BFS (Breadth First Search)", path_values, nodes_explored)
    
    path, path_values, nodes_explored = tree.dfs(start_node, goal_value)
    print_path_info("DFS (Depth First Search)", path_values, nodes_explored)
    
    depth_limit = 3
    path, path_values, nodes_explored = tree.dls(start_node, goal_value, depth_limit)
    print_path_info(f"DLS (Depth Limited Search, limit={depth_limit})", 
                   path_values, nodes_explored)
    
    path, path_values, nodes_explored, depth_found = tree.ids(start_node, goal_value)
    print_path_info("IDS (Iterative Deepening Search)", path_values, nodes_explored,
                   f"Depth found at: {depth_found}")
    
    path, path_values, nodes_explored, total_cost = tree.ucs(start_node, goal_value)
    print_path_info("UCS (Uniform Cost Search)", path_values, nodes_explored,
                   f"Total cost: {total_cost}")

    print("\n" + "=" * 50)
    print("Tree Statistics:")
    print(f"  Root node: {start_node.value} (cost: {start_node.cost})")
    print(f"  Goal node: {goal_value} (cost: {goal_node.cost})")
    print(f"  Total nodes in tree: 26")

if __name__ == "__main__":
    main()