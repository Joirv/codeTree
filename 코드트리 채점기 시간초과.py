from heapq import *

Q, N, u0 = None, None, None
queries = []

########################################
######### inital setting 1 #############

# way 1
def readByTxt():
    global Q, N, u0, queries
    f = open('input.txt', 'r')

    Q = int(f.readline())
    fLine = f.readline().split()
    N, u0 = int(fLine[1]), fLine[2]

    queries = []
    for _ in range(Q - 1):
        queries.append(f.readline().split())

    f.close()

# way 2
def readByCommand():
    global Q, N, u0, queries
    Q = int(input())

    # first querie : 100, N, u0
    fLine = input().split()
    N, u0 = int(fLine[1]), fLine[2]

    queries = []
    for _ in range(Q - 1):
        queries.append(input().split())

########################################

readByTxt()

########################################
######### inital setting 2 #############

wait, waitU = [], set()
heappush(wait, (0, 0, u0))  # (priority, t, url)
waitU.add(u0)

working = [False for _ in range(N)]
workingDomain = [None for _ in range(N)]
workingStartTime = [None for _ in range(N)]

domainSafeTime = dict()     # 해당 도메인의 안전 시간


########################################
######### inital setting 3 #############

def printOut(command):
    global wait, waitU, working, workingDomain, workingStartTime

    print(f"wait({len(wait)}): {wait}")
    print(f"waitU({len(waitU)}): {waitU}")
    print(f"working({len(working) - working.count(False)}): {working}")
    print(f"workingDomain({len(workingDomain) - workingDomain.count(None)}): {workingDomain}")
    print(f"workingStartTime({len(workingStartTime) - workingStartTime.count(None)}): {workingStartTime}")
    print()
    print(command)


########################################
############## Queries #################
for turn in range(len(queries)):
    command = queries[turn]
    cmd = int(command[0])

    if int(command[1])==23132:
        printOut(command)

    # 채점 요청 - wait에 작업 목록 추가
    if cmd == 200:
        t, p, u = int(command[1]), int(command[2]), command[3]

        if u in waitU:
            continue
        heappush(wait, (p, t, u))
        waitU.add(u)

    # 채점 시도 - wait에 있던 작업 채점 시작
    elif cmd == 300:
        t = int(command[1])

        # 작업할 수 있는 채점기가 없다면 요청 무시
        if False not in working:
            continue

        notNow = []
        current, curDomain, curNum = None, None, None
        while len(wait) > 0 and not current:
            current = heappop(wait)
            curDomain, curNum = current[2].split('/')[0], int(current[2].split('/')[1])

            # 현재 작업 중인 채점에 같은 도메인이 있는지 확인
            if curDomain in workingDomain:
                notNow.append(current)
                current, curDomain, curNum = None, None, None
                continue

            # 마지막으로 작업된 같은 도메인 중, 안전 시간이 지났는지 확인
            haveToStop = False
            if curDomain in domainSafeTime.keys():
                if domainSafeTime[curDomain] > t:
                    haveToStop = True
            if haveToStop:
                notNow.append(current)
                current, curDomain, curNome = None, None, None
                continue

        # 작업할 수 있는 애가 있다면
        if current:
            jidx = working.index(False)
            working[jidx] = True
            workingDomain[jidx] = curDomain
            workingStartTime[jidx] = t
            waitU.discard(current[2])

        # 작업 pass 하고 넘어간 것들 다시 추가
        if len(notNow) > 0:
            for task in notNow:
                heappush(wait, task)
        # if t <= 19510 and t >= 19462:
        #     breakpoint()
    # 채점 종료
    elif cmd == 400:
        t, jname = int(command[1]), int(command[2])
        jidx = jname - 1

        # 쉬는 중이라면 요청 무시
        if not working[jidx]:
            continue

        domain, sTime, eTime = workingDomain[jidx], workingStartTime[jidx], t
        maxSafeTime = 0
        if domain in domainSafeTime.keys():
            maxSafeTime = domainSafeTime[domain]
        domainSafeTime[domain] = max(maxSafeTime, sTime + 3 * (eTime - sTime))

        working[jidx] = False
        workingDomain[jidx], workingStartTime[jidx] = None, None

    # else:
    #     print(len(wait))
