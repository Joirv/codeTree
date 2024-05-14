from heapq import *

######################################

N, M, K = map(int, input().split())

power = dict()
invpower = dict()
for i in range(N):
    line = list(map(int, input().split()))
    for j in range(M):
        if line[j] > 0:
            power[(i, j)] = [line[j], 0, -(i + j), -j]  # power, -recent, -(r+c), -c
            invpower[(i, j)] = [-line[j], 0, i + j, j]  # -power, recent, r+c, c


######################################
########### Laser Route ##############

def outOfBoundary(dx, x, x0, x1):
    small, big = min(x0, x1), max(x0, x1)
    #print(dx, small, big)
    if (dx > 0 and x0 == big) or (dx < 0 and x0 == small):
        return True if small < x < big else False
    else:
        return True if ((x < small) or (x > big)) else False

def searchingAlgorithm(dr, dc, r0, c0, r1, c1):
    stack, canMove, success = [(r0, c0)], [], False
    # print("dr, dc:", dr, dc)
    while len(stack) > 0 and not success:
        # print(stack, end=" ")
        r, c = stack.pop(-1)
        # print(r,c)
        if (r, c) not in power.keys():
            # print("here1")
            continue
        if outOfBoundary(dr, r, r0, r1) or outOfBoundary(dc, c, c0, c1):
            # print("here2", outOfBoundary(dr, r, r0, r1), outOfBoundary(dc, c, c0, c1))
            continue
        canMove.append((r, c))

        newr, newc = (r + dr) % N, (c + dc) % M
        if (newr == r1 and c == c1) or (r == r1 and newc == c1):
            success = True
            break

        if dr > 0 and dc < 0:
            stack.append((r, newc))
            stack.append((newr, c))
        elif dr == 0:
            stack.append((r, newc))
        elif dc == 0:
            stack.append((newr, c))
        else:
            stack.append((newr, c))  # 우선 순위가 낮은 상하 방향
            stack.append((r, newc))

    return success, canMove

def searchRoute(r0, c0, r1, c1):
    global power

    # 직선 경로
    # if r0 == r1:
    #     for j in range(c0 + 1, c1):
    #         if (r0, j) not in power.keys(): return None
    #         route.append((r0, j))
    #     return route
    # if c0 == c1:
    #     for i in range(r0 + 1, r1):
    #         if (i, c0) not in power.keys(): return None
    #         route.append((i, c0))
    #     return route

    # dr, dc 계산
    halfN, halfM = N / 2, M / 2
    if r1 == r0: dr = 0
    elif ((0 < r1 - r0 <= halfN) or r1 - r0 <= -halfN): dr = 1
    else: dr = -1

    if c1 == c0: dc = 0
    elif ((0 < c1 - c0 <= halfM) or c1 - c0 <= -halfM): dc = 1
    else: dc = -1

    # 우 -> 하 -> 좌 -> 상 순으로 이동
    success, canMove = searchingAlgorithm(dr, dc, r0, c0, r1, c1)
    if not success and (M%2==0) and abs(c1-c0)==halfM:
        success, canMove = searchingAlgorithm(dr, -dc, r0, c0, r1, c1)
        if success: dc = -dc
    if not success and (N%2==0) and abs(r1-r0)==halfN:
        success, canMove = searchingAlgorithm(-dr, dc, r0, c0, r1, c1)
        if success: dr = -dr
    if not success and (N%2==0) and (M%2==0) and abs(r1-r0)==halfN and abs(c1-c0)==halfM:
        success, canMove = searchingAlgorithm(-dr, -dc, r0, c0, r1, c1)
        if success: dr, dc = -dr, -dc

    if not success: return None

    steps = ((r1 - r0) * dr) % N + ((c1 - c0) * dc) % M
    # print(canMove)
    if canMove[0] == (r0, c0): canMove.pop(0)
    # print("canMove and steps:", canMove, steps)
    return canMove[(-steps):]

######################################
########### Bomb Route ###############

def bombRoute(r, c):
    rm, rp, cm, cp = (r-1)%N, (r+1)%N, (c-1)%M, (c+1)%M
    return {(rm, cm), (rm, c), (rm, cp), (r, cm), (r, cp), (rp, cm), (rp, c), (rp, cp)}

######################################

for turn in range(K):
    # print(power)
    # print(invpower)
    weak, strong = list(power.values()), list(invpower.values())
    heapify(weak)
    heapify(strong)

    if len(weak) < 2:
        break
    wnode, snode = heappop(weak), heappop(strong)
    wr, wc, sr, sc = -wnode[2] + wnode[3], -wnode[3], snode[2] - snode[3], snode[3]
    wnode[0] += (N + M)
    wpower, spower = wnode[0], -snode[0]

    print(wr, wc, sr, sc)
    print("power", wpower, spower)
    route = searchRoute(wr, wc, sr, sc)
    if route is None:
        print("No route found", end = " ")
        route = bombRoute(sr, sc)

    print(route)
    tempkeys = list(power.keys())
    for node in tempkeys:
        if node in route and node != (wr, wc):
            power[node][0] -= wpower//2
            invpower[node][0] += wpower//2
            if power[node][0] <= 0:
                power.pop(node)
                invpower.pop(node)
        elif node != (wr, wc) and node != (sr, sc):
            power[node][0] += 1
            invpower[node][0] -= 1

    power[(wr, wc)][0], power[(wr, wc)][1], invpower[(wr, wc)][0], invpower[(wr, wc)][1] = wpower, -turn-1, -wpower, turn+1
    if spower-wpower <= 0:
        power.pop((sr, sc))
        invpower.pop((sr, sc))
    else:
        power[(sr, sc)][0], invpower[(sr, sc)][0] = spower-wpower, -spower+wpower

# print(power)
strong = list(invpower.values())
heapify(strong)
print(-heappop(strong)[0])
