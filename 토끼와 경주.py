from heapq import *

##################################
########### Get Input ############
Q, queries = None, []

# way 1
def readByTxt():
    global Q, queries

    f = open('input_rabbit.txt', 'r')
    Q = int(f.readline())

    for _ in range(Q):
        queries.append(list(map(int, f.readline().split())))

    f.close()

# way 2
def readByCommand():
    global Q, queries

    Q = int(input())

    for _ in range(Q):
        queries.append(list(map(int, input().split())))

##################################

readByCommand()
# readByTxt()

##################################
########### Setting ##############

command100 = queries[0]
N, M, P = command100[1], command100[2], command100[3]

rabbitQueue = []    # (count, r+c, r, c, pid)
rabbits = {}        # pid : (r, c, d)
points = {}         # pid : point
totScore = 0

for i in range(P):
    pid, d = command100[2*i + 4], command100[2*i + 5]

    rabbits[pid], points[pid] = (1, 1, d), 0
    heappush(rabbitQueue, (0, 2, 1, 1, pid))

##################################
############ Moving ##############

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
def moveByDirection(dirId, r0, c0, d):
    global directions

    dr = (d * directions[dirId][0]) % (2*(N-1))
    dc = (d * directions[dirId][1]) % (2*(M-1))

    newR = r0 + dr if (r0 + dr) <= N else 2*N - (r0 + dr)
    newC = c0 + dc if (c0 + dc) <= M else 2*M - (c0 + dc)

    return (newR, newC)

def move():
    global rabbits, rabbitQueue, moved, totScore

    rabbit = heappop(rabbitQueue)

    r, c, pid = rabbit[2], rabbit[3], rabbit[4]
    d = rabbits[pid][2]

    moveCandidates = []
    for i in range(4):
        newR, newC = moveByDirection(i, r, c, d)
        heappush(moveCandidates, (-newR - newC, -newR, -newC))
    where = heappop(moveCandidates)
    newR, newC = -where[1], -where[2]

    moved[pid] = (-newR - newC, -newR, -newC, -pid)

    # coordinate & score update
    rabbits[pid] = (newR, newC, rabbits[pid][2])
    heappush(rabbitQueue, (rabbit[0]+1, newR+newC, newR, newC, pid))
    points[pid] += (newR+newC)
    totScore += (newR+newC)
    # for idx in rabbits.keys():
    #     curR = rabbits[idx]
    #
    #     # 이동한 토끼의 좌표 업데이트
    #     if idx == pid:
    #         rabbits[idx] = (newR, newC, curR[2])
    #         heappush(rabbitQueue, (rabbit[0] + 1, newR + newC, newR, newC, idx))
    #
    #     # 이동하지 않은 토끼의 점수 업데이트
    #     else:
    #         points[idx] -= (newR+newC)

    # print("rabbitQueue:", rabbitQueue, "rabbits:" ,rabbits)

##################################
############ Queries #############

for i in range(1, Q):
    command = queries[i]
    cmd = command[0]

    if cmd == 200:
        K, S = command[1], command[2]

        moved = dict()
        for i in range(K):
            move()

        movedList = list(moved.values())
        heapify(movedList)

        topRabbit = heappop(movedList)
        topId = -topRabbit[3]
        points[topId] -= S
        # print("rabitQueue:", rabbitQueue, "rabbits:", rabbits)

    elif cmd == 300:
        pid, L = command[1], command[2]
        rabbits[pid] = (rabbits[pid][0], rabbits[pid][1], rabbits[pid][2] * L)

    else:
        pointList = list(points.values())
        heapify(pointList)
        print(-pointList[0] + totScore)