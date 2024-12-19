"""
search algo, path finding, combination of Greedy best first search

"""
import heapq


# Define A* search function
def astar_search(start, goal, grid):
    rows, cols = len(grid), len(grid[0])

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    def neighbors(node):
        x, y = node
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 1:
                yield (nx, ny)

    open_set = [(0 + heuristic(start, goal), 0, start, None)]
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, g, current, parent = heapq.heappop(open_set)

        if current in came_from:
            continue

        came_from[current] = parent

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Reverse the path

        for neighbor in neighbors(current):
            new_cost = cost_so_far[current] + 1  # Each step costs 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, new_cost, neighbor, current))

    return None  # No path found


# Example grid (0: free, 1: obstacle)
grid = [
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

# Run A* search
path = astar_search(start, goal, grid)
if path:
    print("Path found:", path)
else:
    print("No path found.")
