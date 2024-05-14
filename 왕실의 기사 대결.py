import copy

L, N, Q = map(int, input().split())

board = [[0 for i in range(L)] for i in range(L)]
environment = []
power = [0] * N
knights = []
dead = [False] * N
damagePoint = 0

##########################################
########## Initial Setting ###############

# set environment - trap(1), wall(2)
for idx in range(L):
    environment.append(list(map(int, input().split())))

# set knights
for idx in range(N):
    r, c, h, w, k = map(int, input().split())
    space = []

    for i in range(r, r+h):
        for j in range(c, c+w):
            board[i-1][j-1] = idx+1   # (idx+1) : knight index
            space.append([i-1, j-1])

    power[idx] = k
    knights.append(space)

originalPower = copy.deepcopy(power)

##########################################
############ Directions ##################

directions = [[-1,0], [0,1], [1,0], [0,-1]]

def sortByDirection(space, dirKey):
    newSpace = copy.deepcopy(space)

    if dirKey == 0: newSpace.sort(key=lambda s : s[0])     # 위로 이동 : 위에서부터 이동
    elif dirKey == 1: newSpace.sort(key=lambda s : -s[1])  # 우로 이동 : 오른쪽부터 이동
    elif dirKey == 2: newSpace.sort(key=lambda s : -s[0])  # 하로 이동 : 아래서부터 이동
    else: newSpace.sort(key=lambda s : s[1])               # 좌로 이동 : 왼쪽부터 이동

    return newSpace

##########################################
########### Move Knights #################
def moveKnight(id, dirKey):
    global board, environment, power, knights, directions, dead, damagePoint

    dx, dy = directions[dirKey][0], directions[dirKey][1]
    knightsToMove, knightsMoved = [id], []
    tempBoard, tempKnights = copy.deepcopy(board), copy.deepcopy(knights)
    stopMove = False
    while len(knightsToMove) > 0 and not stopMove:
        cur = knightsToMove.pop(0)
        if dead[cur-1]:
            continue
        knightsMoved.append(cur)

        curspace = sortByDirection(knights[cur-1], dirKey)
        tempSpace = []
        for i in range(len(curspace)):
            x, y = curspace[i][0], curspace[i][1]

            if tempBoard[x][y] == cur:
                tempBoard[x][y] = 0     # 원래 있던 곳에서 지워줌

            if x+dx < 0 or y+dy < 0 or x+dx >= L or y+dy >= L:  # 보드 밖으로 벗어날 수 없음
                stopMove = True
                break

            env, kn = environment[x+dx][y+dy], board[x+dx][y+dy]    # 옮길 곳의 지형 정보 & 옮길 곳의 나이트 번호
            if env == 2:
                stopMove = True
                break
            elif kn > 0 and kn not in knightsToMove and kn != cur and not dead[kn-1]:  # 옮길 곳에 나이트가 있고, 그 나이트가 knightsToMove에 없다면
                knightsToMove.append(kn)
            tempBoard[x+dx][y+dy] = cur     # 새로운 곳으로 옮겨줌 (보드에서 옮겨줌)
            tempSpace.append([x+dx, y+dy])
        tempKnights[cur-1] = tempSpace

    if not stopMove:
        board = tempBoard
        knights = tempKnights
    else:
        knightsMoved = []

    return knightsMoved

##########################################
########### Update Points ################

def updatePoints(id, moved):
    global damagePoint
    # print(id)
    if len(moved) > 0:
        moved.remove(id)

        for knight in moved:
            cnt = 0
            for i in range(len(knights[knight-1])):
                x, y = knights[knight-1][i][0], knights[knight-1][i][1]
                if environment[x][y] == 1:
                    cnt += 1
            power[knight-1] -= cnt
            # print(f"{knight} got damaged {cnt}")
            damagePoint += cnt

##########################################
########### Update Death #################

def checkDeath():
    global damagePoint

    for idx in range(len(power)):
        if power[idx] <= 0 and not dead[idx]:
            dead[idx] = True
            damagePoint = damagePoint + power[idx] - originalPower[idx]
            power[idx] = 0


##########################################
############# Queries ####################

# for i in range(L):  print(board[i])
# print()

for idx in range(Q):
    knightId, dir = map(int, input().split())
    if dead[knightId-1]:
        continue
    moved = moveKnight(knightId, dir)
    updatePoints(knightId, moved)
    checkDeath()
    # print(knights)
    # for i in range(L):
    #     print(board[i])
    # print()
    # print(power)
    # print(dead)
print(damagePoint)