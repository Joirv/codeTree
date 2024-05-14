N, Q = map(int, input().split())

parent = [0] * (N+1)
power = [0] * (N+1)
message = [0] * (N+1)
messageTable = [[0 for _ in range(22)] for _ in range(N+1)]   # number of msg which ith node can carry for j-level

def init(command):
    global N, Q, parent, power, message, messageTable

    # set parent & power
    for i in range(1, N+1):
        parent[i] = command[i]
        power[i] = min(command[i+N], 20)

    # set message & messageTable
    for i in range(1, N+1):
        current = i
        p = power[i]

        while current and p>=0:
            messageTable[current][p] += 1
            message[current] += 1

            current = parent[current]
            p -= 1

def onoff(node):
    sign = 1 if power[node] < 0 else -1

    current = parent[node]
    step = 1

    while current:
        for j in range(step, 22):
            message[current] += sign * messageTable[node][j]
            if j > step:
                messageTable[current][j-step] += sign * messageTable[node][j]
        if power[current] < 0:
            break

        current = parent[current]
        step += 1

    power[node] = -power[node]

def updatePower(node, newPower:int):
    # originalPower = power[node]
    # newPower = min(newPower, 20)
    #
    # if originalPower < 0:
    #     power[node] = (-1) * abs(newPower)
    #     messageTable[node][originalPower] -= 1
    #     messageTable[node][newPower] += 1
    #
    # elif originalPower >= 0 and originalPower != newPower:
    #     power[node] = newPower
    #     small, big = min(originalPower, newPower), max(originalPower, newPower)
    #
    #     sign = 1 if originalPower < newPower else -1
    #
    #     current = node
    #     step = 0
    #     while current:
    #         if step < small :
    #             messageTable[current][small-step] -= sign
    #         messageTable[current][big-step] += sign
    #         if step > small and step <= big:
    #             message[current] += sign
    #
    #         if power[current] < 0: break
    #
    #         current = parent[current]
    #         step += 1

    originalPower = power[node]
    newPower = min(newPower, 20)
    power[node] = newPower

    messageTable[node][originalPower] -= 1
    if originalPower > 0:
        current = parent[node]
        step = 1

        while current:
            if originalPower >= step:   message[current] -= 1
            if originalPower > step:    messageTable[current][originalPower - step] -= 1
            if power[current] < 0:  break

            current = parent[current]
            step += 1

    messageTable[node][newPower] += 1
    if originalPower > 0:
        current = parent[node]
        step = 1

        while current:
            if newPower >= step: message[current] += 1
            if newPower > step: messageTable[current][newPower - step] += 1
            if power[current] < 0: break

            current = parent[current]
            step += 1
def changeParent(node1, node2):
    originalPower1, originalPower2 = power[node1], power[node2]

    if originalPower1 > 0: onoff(node1)
    if originalPower2 > 0: onoff(node2)

    parent[node1], parent[node2] = parent[node2], parent[node1]

    if originalPower1 > 0: onoff(node1)
    if originalPower2 > 0: onoff(node2)

def getMessage(node):
    return message[node]-1 if message[node]>0 else 0

#################

commands = [list(map(int, input().split())) for _ in range(Q)]

for command in commands:
    cmd = command[0]
    node = command[1]

    if cmd==100:
        init(command)
    elif cmd == 200:
        onoff(node)
    elif cmd == 300:
        updatePower(node, command[2])
    elif cmd == 400:
        changeParent(node, command[2])
    else:
        print(getMessage(node))

