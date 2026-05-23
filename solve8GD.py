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

def get_children(parent_node, goal_state):
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
            
            misplaced_tiles = 0
            for i in range(3):
                for j in range(3):
                    if new_state[i][j] != 0 and new_state[i][j] != goal_state[i][j]:
                        misplaced_tiles += 1
                        
            children.append(node(state=new_state, parent=parent_node, move=move_name, cost=misplaced_tiles))
    return children

def solve_greedy(start_state, goal_state):
    root = node(state=start_state)
    if root.state == goal_state: return []

    frontier = [root]
    reached = [root.state] 

    while len(frontier) > 0:
        frontier.sort(key=lambda n: n.cost)
        
        current_node = frontier.pop(0)

        if current_node.state == goal_state:
            path = []
            temp = current_node  
            while temp.move is not None:
                path.append(temp.move)
                temp = temp.parent
            return path[::-1]  
        
        for child in get_children(current_node, goal_state):
            if child.state not in reached:
                reached.append(child.state)
                frontier.append(child)
                
    return None

START = [[0, 1, 3], 
         [4, 2, 6], 
         [7, 5, 8]]
GOAL = [[1, 2, 3], 
        [4, 5, 6], 
        [7, 8, 0]]

result = solve_greedy(START, GOAL)
print("Các bước di chuyển:", result)