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

readByCommand()

########################################
######### inital setting 2 #############

domain = u0.split('/')[0]
waitByDomain = dict()
waitByDomain[domain] = []
heappush(waitByDomain[domain], (0, 0, u0))

waitU = set()
waitU.add(u0)

working = [False for _ in range(N)]
workingDomain = [None for _ in range(N)]    # 현재 해당 채점기에서 작업중인 도메인

idleDomain = set()  # 작업 중이 아닌 도메인
idleDomain.add(domain)

workingStartTime = [None for _ in range(N)]

domainSafeTime = dict()     # 해당 도메인의 안전 시간
domainSafeTime[domain] = 0

ans = 1

########################################
######### inital setting 3 #############

def printOut(command):
    global waitU, working, workingDomain, workingStartTime, ans, domainSafeTime, waitByCommand

    print(f"ans: {ans}")
    print(f"waitByDomain: {waitByDomain}")
    print(f"waitU({len(waitU)}): {waitU}")
    print(f"working({len(working) - working.count(False)}): {working}")
    print(f"workingDomain({len(workingDomain) - workingDomain.count(None)}): {workingDomain}")
    print(f"idleDomain: {idleDomain}")
    print(f"DomainSafeTime: {domainSafeTime}")
    print()
    print(command)


########################################
############## Queries #################
for turn in range(len(queries)):
    command = queries[turn]
    cmd = int(command[0])

    #printOut(command)
    # 채점 요청 - wait에 작업 목록 추가
    if cmd == 200:
        t, p, u = int(command[1]), int(command[2]), command[3]
        domain = u.split('/')[0]

        if u in waitU:
            continue

        if domain not in waitByDomain.keys():
            waitByDomain[domain] = []

        heappush(waitByDomain[domain], (p, t, u))
        ans += 1
        waitU.add(u)

        domain = u.split('/')[0]
        if domain not in workingDomain:
            idleDomain.add(domain)
        if domain not in domainSafeTime.keys():
            domainSafeTime[domain] = 0

    # 채점 시도 - wait에 있던 작업 채점 시작
    elif cmd == 300:
        t = int(command[1])

        # 작업할 수 있는 채점기가 없다면 요청 무시
        if False not in working:
            continue

        current, candidates = None, []
        for dm in idleDomain:
            if len(waitByDomain[dm]) > 0 and domainSafeTime[dm] <= t:
                heappush(candidates, waitByDomain[dm][0])

        # 작업할 수 있는 애가 있다면 작업 상태 변경
        if len(candidates) > 0:
            current = heappop(candidates)
            curDomain = current[2].split('/')[0]

            heappop(waitByDomain[curDomain])
            ans -= 1

        # # 작업할 수 있는 애가 있다면 작업 상태로 변경하기
        if current:
            jidx = working.index(False)
            working[jidx] = True
            workingDomain[jidx] = curDomain
            workingStartTime[jidx] = t
            waitU.discard(current[2])
            idleDomain.discard(current[2].split('/')[0])

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

        if domain not in workingDomain:
            idleDomain.add(domain)

    else:
        print(ans)