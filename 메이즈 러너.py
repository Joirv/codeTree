import copy


def printBoard(board):
    for row in board[1:]:
        print(row[1:])
    print()

###########################################
########### Initial Setting ###############

N, M, K = map(int, input().split())
ans = 0

wall = [[0 for _ in range(N+1)]]
# board = [[[] for _ in range(N)] for _ in range(N)]
coordinates = []

for _ in range(N):
    wallrow = list(map(int, input().split()))
    wallrow.insert(0,0)
    wall.append(wallrow)

for i in range(M):
    x, y = map(int, input().split())
    coordinates.append((x, y))

exitX, exitY = map(int, input().split())

###########################################
############# Find Square #################

def findSquare():
    global coordinates, exitX, exitY

    minwidth = 11
    r0, c0 = 11, 11
    for i in range(len(coordinates)):
        x, y = coordinates[i][0], coordinates[i][1]
        width = max(abs(x-exitX), abs(y-exitY))

        downSide, rightSide = max(x, exitX), max(y, exitY)
        upSide, leftSide = max(1, downSide - width), max(1, rightSide - width)
        # print(x, y, width, upSide, leftSide, downSide, rightSide)
        if width < minwidth:
            minwidth, r0, c0 = width, upSide, leftSide
        elif width == minwidth and (upSide < r0 or (upSide == r0 and leftSide < c0)):
            minwidth, r0, c0 = width, upSide, leftSide

    return (r0, c0), minwidth+1

###########################################
############ Rotate Square ################

def changeCoordinates(x, y, r, c, w):
    dx, dy = r-1, c-1
    return (y-dy+dx, w+1-x+dx+dy)

def rotateSquare(r0, c0, width):
    global coordinates, wall, N, exitX, exitY

    # print(f"square : {(r0, c0)} with length={width}")

    # 참가자 회전
    for i in range(len(coordinates)):
        x, y = coordinates[i][0], coordinates[i][1]
        # 참가자 이동
        if r0 <= x < r0+width and c0 <= y < c0+width:   # 정사각형 범위 내에 있다면
            coordinates[i] = changeCoordinates(x, y, r0, c0, width)

    # 출구 회전
    if r0 <= exitX < r0+width and c0 <= exitY < c0+width:
        exitX, exitY = changeCoordinates(exitX, exitY, r0, c0, width)

    # 벽 회
    newWall = copy.deepcopy(wall)
    for i in range(r0, r0+width):
        for j in range(c0, c0+width):
            newX, newY = changeCoordinates(i, j, r0, c0, width)
            newWall[newX][newY] = max(0, wall[i][j] - 1)
    wall = newWall

###########################################
########## Move Participant ###############

def move():
    global coordinates, wall, exitX, exitY, ans

    for i in range(len(coordinates)):
        moved = False
        x, y = coordinates[i][0], coordinates[i][1]

        if not moved and x < exitX and wall[x+1][y] == 0:
            moved, coordinates[i] = True, (x+1, y)
        elif not moved and x > exitX and wall[x-1][y] == 0:
            moved, coordinates[i] = True, (x-1, y)
        elif not moved and y < exitY and wall[x][y+1] == 0:
            moved, coordinates[i] = True, (x, y+1)
        elif not moved and y > exitY and wall[x][y-1] == 0:
            moved, coordinates[i] = True, (x, y-1)

        if moved:
            ans += 1
    while (exitX, exitY) in coordinates:
        coordinates.remove((exitX, exitY))

###########################################
############# Make Board ##################
def makeBoard():
    global coordinates, exitX, exitY
    board = [[[] for _ in range(N+1)] for _ in range(N+1)]

    board[exitX][exitY] = -1
    for i in range(len(coordinates)):
        x, y = coordinates[i][0], coordinates[i][1]
        board[x][y].append(i)
    return board

###########################################
############# Game Start ##################

# printBoard(wall)
# printBoard(makeBoard())

for i in range(K):
    # print(f"\n#### Turn {i+1} #####")
    # print("#### Moving ######")
    move()
    # printBoard(makeBoard())
    if len(coordinates)==0:
        break
    (r0, c0), width = findSquare()
    # print("#### Rotating ####")
    rotateSquare(r0, c0, width)

    # printBoard(wall)
    # printBoard(makeBoard())
    # print(exitX, exitY)

print(ans)
print(exitX, exitY)