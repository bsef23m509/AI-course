from collections import deque

# -----------------------------
# File Handling
# -----------------------------
def read_file(filename):
    """
    Reads the grid from a text file.
    Returns number of rows, columns, and the grid as a list of lists.
    """
    with open(filename, "r") as file:
        rows, cols = map(int, file.readline().split())
        grid = []
        for _ in range(rows):
            grid.append(file.readline().split())
    return rows, cols, grid

# -----------------------------
# Task 1: State Space Functions
# -----------------------------
def get_state(row, col):
    return (row, col)

def initial_state(grid):
    return (0, 0)


def goal_test(state, grid):
    r, c = state
    return grid[r][c] == 'G'

def actions(state, grid):
    final_actions = []
    r, c = state
    all_actions = [(-1,0), (1,0), (0,-1), (0,1)] 

    grid_rows = len(grid)
    grid_cols = len(grid[0])

    for i in all_actions:
        dr, dc = i
        if r + dr >= 0 and c + dc >= 0 and r + dr < grid_rows and c + dc < grid_cols and grid[r + dr][c + dc] != '#':
            final_actions.append((dr, dc))
        
    return final_actions

def transition(state, action):
    r, c = state
    dr, dc = action
    return (r + dr, c + dc)

# -----------------------------
# Search Algorithms (Students implement)
# -----------------------------
def bfs(grid, start, goal, rows, cols):
    paths = deque([[start]])
    visited = set()
    explored_order = []
    final_path = None

    while paths:
        path = paths.popleft()
        cur_state = path[-1]
        

        if cur_state in visited:
            continue

        if goal_test(cur_state, grid):
            final_path = path
            break


        visited.add(cur_state)

        for action in actions(cur_state, grid):
            new_path = list(path)
            next_state = transition(cur_state, action)
            new_path.append(next_state)
            paths.append(new_path)


    return final_path, len(visited)

def dfs(grid, start, goal, rows, cols):
    paths = [[start]]
    visited = set()
    explored_order = []
    final_path = None

    while paths:
        path = paths.pop()
        cur_state = path[-1]

        if cur_state in visited:
            continue

        if goal_test(cur_state, grid):
            final_path = path
            break


        visited.add(cur_state)

        for action in actions(cur_state, grid):
            new_path = list(path)
            next_state = transition(cur_state, action)
            new_path.append(next_state)
            paths.append(new_path)


    return final_path, len(visited)
        

# -----------------------------
# Output Handling
# -----------------------------
def write_output(filename, content):
    """
    Writes the search results to a text file.
    """
    with open(filename, "w") as file:
        file.write(content)

# -----------------------------
# Main Program
# -----------------------------
def main():
    rows, cols, grid = read_file("campus.txt")
    start = initial_state(grid)
    goal = None

    # Goal state calculation
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if goal_test((i, j), grid):
                goal = (i, j)
                break
        if goal != None:
            break


    dfs_path, dfs_nodes = dfs(grid, start, goal, rows, cols)
    bfs_path, bfs_nodes = bfs(grid, start, goal, rows, cols)
    

    output_text = ""

    if bfs_path:
        output_text += "Algorithm: BFS\n"
        output_text += "Path: " + " -> ".join(str(p) for p in bfs_path) + "\n"
        output_text += "Path Length: " + str(len(bfs_path)) + "\n"
        output_text += "Nodes Explored: " + str(bfs_nodes) + "\n"
        output_text += "--------------------------------\n"

    if dfs_path:
        output_text += "Algorithm: DFS\n"
        output_text += "Path: " + " -> ".join(str(p) for p in dfs_path) + "\n"
        output_text += "Path Length: " + str(len(dfs_path)) + "\n"
        output_text += "Nodes Explored: " + str(dfs_nodes) + "\n"

    write_output("result.txt", output_text)

if __name__ == "__main__":
    main()
