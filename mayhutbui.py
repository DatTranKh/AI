import random

MATRIX = [[1,0,0,0,1,1,1],
          [0,0,1,1,0,0,1],
          [1,1,0,1,0,0,1],
          [1,0,0,0,1,0,0]]
M = len(MATRIX[0])
N = len(MATRIX)
LIMIT = M*N*5
posX = random.randint(0,M-1)
posY = random.randint(0,N-1)

def possible_moves(posX, posY):
    moves = []
    if posX > 0: moves.append("LEFT")
    if posX < M-1: moves.append("RIGHT")
    if posY > 0: moves.append("UP")
    if posY < N-1: moves.append("DOWN")
    return moves

step = 0
while step < LIMIT:
    print("Step",step,":")
    print(posX, posY)
    if MATRIX[posY][posX] == 1: MATRIX[posY][posX] = 0
    print(MATRIX)
    moves = possible_moves(posX, posY)
    action = moves[random.randint(0,len(moves)-1)]
    if action == "UP": posY -= 1
    if action == "DOWN": posY += 1
    if action == "LEFT": posX -= 1
    if action == "RIGHT": posX += 1
    print(action)
    step+=1