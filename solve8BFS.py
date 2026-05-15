class node:
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost

def get_0_pos(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def get_children(parent_node):
    children = []
    r, c = get_0_pos(parent_node.state)
    moves = {"UP": (-1, 0), 
             "DOWN": (1, 0), 
             "LEFT": (0, -1), 
             "RIGHT": (0, 1)}
    
    for move_name, (dr, dc) in moves.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = [row[:] for row in parent_node.state]
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            children.append(node(state=new_state, parent=parent_node, move=move_name, cost=parent_node.cost + 1))
    return children

def solve_bfs(start_state, goal_state):
    root = node(state=start_state)
    if root.state == goal_state:
        return []

    frontier = [root]
    reached = [start_state]

    while len(frontier) > 0:
        current_node = frontier.pop(0)
        
        for child in get_children(current_node):
            if child.state not in reached:
                if child.state == goal_state:
                    path = []
                    temp = child
                    while temp.move is not None:
                        path.append(temp.move)
                        temp = temp.parent
                    return path[::-1]
                
                reached.append(child.state)
                frontier.append(child)
    return None

START = [[1, 2, 3], 
         [4, 5, 6], 
         [0, 7, 8]]
GOAL = [[1, 2, 3], 
        [4, 5, 6], 
        [7, 8, 0]]

result = solve_bfs(START, GOAL)
print(result)