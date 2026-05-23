class node:
    def __init__(self, state, parent=None, move=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g                # g(n): Chi phí thực tế từ Start đến node hiện tại (số bước)
        self.h = h                # h(n): Số ô sai vị trí so với Goal
        self.f = self.g + self.h  # f(n): Tổng chi phí đánh giá

def get_0_pos(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def count_misplaced_tiles(state, goal_state):
    """Hàm tính số ô sai vị trí (bỏ qua ô trống số 0)"""
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                misplaced += 1
    return misplaced

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
            
            g_new = parent_node.g + 1
            h_new = count_misplaced_tiles(new_state, goal_state)
            
            children.append(node(state=new_state, parent=parent_node, move=move_name, g=g_new, h=h_new))
            
    return children

def solve_astar(start_state, goal_state):
    h_start = count_misplaced_tiles(start_state, goal_state)
    root = node(state=start_state, g=0, h=h_start)
    
    if root.state == goal_state: return []

    frontier = [root]
    reached = {str(root.state): root.f}

    while len(frontier) > 0:
        frontier.sort(key=lambda n: (n.f, n.h))
        
        current_node = frontier.pop(0)

        if current_node.state == goal_state:
            path = []
            temp = current_node
            while temp.move is not None:
                path.append(temp.move)
                temp = temp.parent
            return path[::-1]
        
        for child in get_children(current_node, goal_state):
            state_str = str(child.state)
            if state_str not in reached or child.f < reached[state_str]:
                reached[state_str] = child.f
                frontier.append(child)
                
    return None

# ----- CHẠY THỬ -----
START = [[1, 2, 3], 
         [4, 5, 6], 
         [0, 7, 8]]
         
GOAL = [[1, 2, 3], 
        [4, 5, 6], 
        [7, 8, 0]]

result = solve_astar(START, GOAL)
print("Các bước di chuyển:", result)
print("Tổng số bước:", len(result))