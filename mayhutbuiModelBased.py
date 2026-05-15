import random

MATRIX = [[1, 0, 'X', 0, 1, 1, 1],
          [0, 0, 1, 1, 'X', 0, 1],
          [1, 'X', 0, 1, 0, 0, 1],
          [1, 0, 0, 0, 1, 'X', 0]]

M, N = len(MATRIX[0]), len(MATRIX)
LIMIT = M * N * 5

while True:
    posX, posY = random.randint(0, M - 1), random.randint(0, N - 1)
    if MATRIX[posY][posX] != 'X': break

state = None        
model = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
last_action = None  

def update_state(current_state, action, percept, model):
    new_state = []
    for row in percept:
        new_state.append(row[:])
    return new_state

def rule_match(curr_y, curr_x, current_state, model):
    rules = []
    for act, (dx, dy) in model.items():
        nx, ny = curr_x + dx, curr_y + dy
        if 0 <= nx < M and 0 <= ny < N and current_state[ny][nx] != 'X':
            if current_state[ny][nx] == 1:
                return act 
            rules.append(act)
    return random.choice(rules) if rules else None

step = 0
while step < LIMIT:
    print(f"Step {step}: Position({posX}, {posY})")
    
    state = update_state(state, last_action, MATRIX, model)
    
    if MATRIX[posY][posX] == 1:
        MATRIX[posY][posX] = 0
        print("Action: SUCK")
    
    action = rule_match(posY, posX, state, model)
    
    if action is None: break
        
    dx, dy = model[action]
    posX += dx
    posY += dy
    last_action = action
    
    for row in MATRIX: print(row)
    print(f"Move: {action}\n" + "-"*20)
    step += 1