class Node:
    def __init__(self, id, parent, power):
        self.id = id
        self.parent = parent
        self.power = min(power, 20)
        self.alarmSet = set()

    def setNode(self, parent, power):
        self.parent = parent
        self.power = min(power, 20)

    def addNode(self, node):
        self.alarmSet.add(node)

    def deleteNode(self, node):
        self.alarmSet.discard(node)

    def setAlarmSet(self):
        currentNode = self

        num = 0
        while currentNode.id > 0:
            if self.power >= num:
                currentNode.addNode(self)
            else:
                break
            if currentNode.power < 0:
                break
            currentNode = currentNode.parent
            num += 1

    def onoff(self):
        self.power = -self.power
        # on -> off
        if self.power < 0:
            currentNode = self.parent
            while currentNode.id > 0:
                for node in self.alarmSet:
                    currentNode.deleteNode(node)
                currentNode = currentNode.parent

        # off -> on
        else:
            originalSet = set(self.alarmSet)
            for node in originalSet:
                node.setAlarmSet()

    def updatePower(self, power):
        originalPower = self.power
        if self.power > 0:
            currentNode = self.parent
            while currentNode.id > 0:
                currentNode.deleteNode(self)
                currentNode = currentNode.parent

        self.power = power
        self.setAlarmSet()

        if originalPower < 0:
            self.onoff()

    def setParent(self, parent):
        self.parent = parent

    def changeParent(self, other):
        power1, power2 = self.power, other.power
        if power1 > 0: self.onoff()
        if power2 > 0: other.onoff()

        temp = other.parent
        other.setParent(self.parent)
        self.setParent(temp)

        if power1 > 0: self.onoff()
        if power2 > 0: other.onoff()

    def numAlarm(self):
        return len(self.alarmSet)-1 if len(self.alarmSet) > 0 else 0


#################
N, Q = map(int, input().split())

prepare = list(map(int, input().split()))
commands = [list(map(int, input().split())) for _ in range(Q-1)]

nodes = [Node(i, None, 1) for i in range(N+1)]
# print(nodes)
for i in range(N):
    parent = nodes[prepare[i + 1]]
    power = prepare[N + i + 1]
    nodes[i+1].setNode(parent, power)

for node in nodes:
    node.setAlarmSet()

for command in commands:
    cmd = command[0]
    nodeId = command[1]
    node = nodes[nodeId]

    if cmd == 200:
        node.onoff()

    elif cmd == 300:
        node.updatePower(command[2])
    elif cmd == 400:
        otherNodeId = command[2]
        otherNode = nodes[otherNodeId]
        node.changeParent(otherNode)
    else:
        print(node.numAlarm())
