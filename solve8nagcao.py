GOAL = [[1, 2, 3],
        [4, 5, 6], 
        [7, 8, 0]]
MATRIX = [[1, 2, 3], 
          [4, 5, 6], 
          [8, 0, 7]]

state = None        # Trạng thái hiện tại môi trường
model = {           # Mô hình dự báo hành động
    "UP": (-1, 0), "DOWN": (1, 0), 
    "LEFT": (0, -1), "RIGHT": (0, 1)
}
last_move = None  # Hành động trước đó
memo = []           # Bộ nhớ các trạng thái đã qua

def update_state(current_state, moves, percept, model):
    new_state = []
    for row in percept:
        new_state.append(row[:])
    return new_state

def rule_match(current_state, memo, model):
    r, c = 0, 0
    for i in range(len(current_state)):
        for j in range(len(current_state[0])):
            if current_state[i][j] == 0:
                r, c = i, j
    
    for move in ["UP", "DOWN", "LEFT", "RIGHT"]:
        dr, dc = model[move]
        nr, nc = r + dr, c + dc
        
        if 0 <= nr < len(MATRIX) and 0 <= nc < len(MATRIX[0]):
            test_st = []
            for row in current_state: test_st.append(row[:])
            test_st[r][c], test_st[nr][nc] = test_st[nr][nc], test_st[r][c]
            
            if test_st not in memo:
                return move
    return None


step = 1
while step < 50:
    print(f"Step {step}:")
    
    state = update_state(state, last_move, MATRIX, model)
    memo.append(state)
    
    if state == GOAL:
        print("SOLVED")
        break
        
    current_move = rule_match(state, memo, model)
    
    if current_move == None:
        print("STUCK")
        break
        
    print(f"move: {current_move}")

    r, c = 0, 0
    for i in range(3):
        for j in range(3):
            if MATRIX[i][j] == 0: r, c = i, j
            
    dr, dc = model[current_move]
    nr, nc = r + dr, c + dc
    MATRIX[r][c], MATRIX[nr][nc] = MATRIX[nr][nc], MATRIX[r][c]
    
    for row in MATRIX: print(row)
    
    last_move = current_move
    step += 1