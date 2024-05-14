def distance(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2

# up - right - down - left - upleft - upright - downleft - downright
directions = [[-1,0], [0,1], [+1,0], [0,-1], [-1,-1], [-1,+1], [1,-1],[+1,+1]]
class Board:
    def __init__(self, n):
        self.n = n
        self.board = [[[] for _ in range(n)] for _ in range(n)]

    def leave(self, id, r, c):
        self.board[r-1][c-1].remove(id)

    def came(self, id, r, c):
        self.board[r-1][c-1].append(id)

    def notInBoard(self, r, c):
        ridx, cidx = r - 1, c - 1
        if ridx < 0 or ridx >= self.n or cidx < 0 or cidx >= self.n:
            return True
        return False

    def who(self, r, c):
        if self.notInBoard(r, c):
            return False
        elif len(self.board[r-1][c-1])==0:
            return "empty"
        return self.board[r-1][c-1][0]

    def showBoard(self):
        for i in range(self.n):
            print(self.board[i])
        print()

class Creature():
    def __init__(self, id, r, c, power):
        self.id = id    # rudolph id = -1
        self.r = r
        self.c = c
        self.power = power
        self.alive = True

    def move(self, key, step=1, reverse=False):
        board.leave(self.id, self.r, self.c)
        direction = directions[key]
        if not reverse:
            self.r += step * direction[0]
            self.c += step * direction[1]
        else :
            self.r -= step * direction[0]
            self.c -= step * direction[1]

        if board.notInBoard(self.r, self.c) and self.id != -1:
            self.alive = False
        else:
            board.came(self.id, self.r, self.c)
class Santa(Creature):
    def __init__(self, id, r, c, power, distance):
        super().__init__(id, r, c, power)
        self.point = 0
        self.iced = 0
        self.distance = distance

    def updateDistance(self, distance):
        self.distance = distance

    def moveSanta(self, rr, rc, power):
        if self.iced > 0:
            self.iced -= 1

        else :
            distances = []
            for i in range(4):
                direction = directions[i]
                newr = self.r + direction[0]
                newc = self.c + direction[1]
                if board.who(newr, newc)=="empty" or board.who(newr, newc)==-1 :
                    distances.append(distance(rr, rc, newr, newc))
                else :
                    distances.append(100000000)

            key = distances.index(min(distances))
            if distances[key] < distance(self.r, self.c, rr, rc):
                self.move(key)

            if self.r == rr and self.c == rc:
                self.collision_by_santa(key, power)
    def getPoint(self, point=1):
        self.point += point

    def collision_by_rudolph(self, key, power):
        self.iced = 2
        self.getPoint(power)

        self.interaction(key, power, reverse=False)
    def collision_by_santa(self, key, power):
        self.iced = 1
        self.getPoint(power)

        self.interaction(key, power, reverse=True)

    def interaction(self, key, power, reverse=False):
        if reverse:
            newr = self.r - directions[key][0] * power
            newc = self.c - directions[key][1] * power
        else:
            newr = self.r + directions[key][0] * power
            newc = self.c + directions[key][1] * power

        if board.notInBoard(newr, newc):
            board.leave(self.id, self.r, self.c)
            self.alive = False
        elif board.who(newr, newc) == "empty":
            self.move(key, power, reverse=reverse)
        else :
            santas.sort(key=lambda s: s.id)
            interactSanta = santas[board.who(newr, newc)-1]
            interactSanta.interaction(key, 1, reverse=reverse)
            self.move(key=key, step=power, reverse=reverse)

class Rudolph(Creature):
    def __init__(self, r, c, power):
        super().__init__(-1, r, c, power)

    def moveRudolph(self, power):
        santas.sort(key=lambda s: (-s.alive, s.distance, -s.r, -s.c))
        close_santa = santas[0]
        sr, sc = close_santa.r, close_santa.c

        distances = []
        for i in range(8):
            direction = directions[i]
            newr = self.r + direction[0]
            newc = self.c + direction[1]
            distances.append(distance(sr, sc, newr, newc))

        key = distances.index(min(distances))
        self.move(key)
        if sr == self.r and sc == self.c:
            close_santa.collision_by_rudolph(key, power)


# start the code

N, M, P, C, D = map(int, input().split())

board = Board(N)

r, c = map(int, input().split())
rudolph = Rudolph(r=r, c=c, power=C)
board.came(-1, r, c)

santas = []
for _ in range(P):
    sid, sr, sc = map(int, input().split())
    santas.append(Santa(id=sid, r=sr, c=sc, power=D, distance=distance(rudolph.r, rudolph.c, sr, sc)))
    board.came(sid, sr, sc)

for _ in range(M):
    santas.sort(key=lambda s: s.alive)
    if not santas[len(santas)-1].alive:
        break
    rudolph.moveRudolph(C)
    santas.sort(key=lambda s : s.id)
    for santa in santas:
        if not santa.alive:
            continue
        santa.moveSanta(rudolph.r, rudolph.c, D)
        santa.updateDistance(distance(rudolph.r, rudolph.c, santa.r, santa.c))
    for santa in santas:
        if santa.alive:
            santa.getPoint()
    #board.showBoard()

santas.sort(key= lambda s:s.id)
for santa in santas:
    print(santa.point, end=" ")