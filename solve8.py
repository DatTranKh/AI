import copy

GOAL = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

def get_pos(state, element):
    for r in range(3):
        for c in range(3):
            if state[r][c] == element:
                return r, c

def get_manhattan(state):
    distance = 0
    for i in range(1, 9):
        r1, c1 = get_pos(state, i)
        r2, c2 = get_pos(GOAL, i)
        distance += abs(r1 - r2) + abs(c1 - c2)
    return distance

def get_valid_moves(state):
    r, c = get_pos(state, 0)
    moves = []
    if r > 0: moves.append('UP')
    if r < 2: moves.append('DOWN')
    if c > 0: moves.append('LEFT')
    if c < 2: moves.append('RIGHT')
    return moves, (r, c)

def execute_move(state, action, pos):
    new_state = copy.deepcopy(state)
    r, c = pos
    if action == 'UP':
        new_state[r][c], new_state[r-1][c] = new_state[r-1][c], new_state[r][c]
    elif action == 'DOWN':
        new_state[r][c], new_state[r+1][c] = new_state[r+1][c], new_state[r][c]
    elif action == 'LEFT':
        new_state[r][c], new_state[r][c-1] = new_state[r][c-1], new_state[r][c]
    elif action == 'RIGHT':
        new_state[r][c], new_state[r][c+1] = new_state[r][c+1], new_state[r][c]
    return new_state

def solve_8_puzzle(start_state):
    current_state = start_state
    history = []
    
    print("Trạng thái bắt đầu:")
    for row in current_state: print(row)
    
    step = 0
    while get_manhattan(current_state) > 0:
        step += 1
        moves, pos = get_valid_moves(current_state)
        best_move = None
        min_score = float('inf')
        
        for move in moves:
            temp_state = execute_move(current_state, move, pos)
            score = get_manhattan(temp_state)
            
            if score < min_score and temp_state not in history:
                min_score = score
                best_move = move
                best_state = temp_state
        
        if best_move is None:
            print("AI bị kẹt vào cực tiểu cục bộ (Local Minima)!")
            break
            
        current_state = best_state
        history.append(current_state)
        
        print(f"\nBước {step}: Di chuyển {best_move}")
        for row in current_state: print(row)
        
        if step > 100:
            print("Quá số bước quy định!")
            break

    if get_manhattan(current_state) == 0:
        print("\nChúc mừng! AI đã giải xong.")

# Chạy thử nghiệm
initial_board = [
    [1, 2, 3],
    [5, 6, 4],
    [8, 7, 0]
]

solve_8_puzzle(initial_board)