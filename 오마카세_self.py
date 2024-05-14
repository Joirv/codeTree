class Query():
    def __init__ (self, cmd, t=-1, x=-1, name="", n=-1):
        self.cmd = cmd
        self.t = t
        self.x = x
        self.name = name
        self.n = n

queries = []

L, Q = map(int, input().split())

names = set()
positions = dict()
foods = dict()

entrance_time = dict()
exit_time = dict()

for i in range(Q):
    command = input().split()
    cmd = int(command[0])

    if cmd == 100:
        # 스시 추가
        t, x, name = int(command[1]), int(command[2]), command[3]
        queries.append( Query(cmd=cmd, t=t, x=x, name=name) )

        if name not in foods.keys():
            foods[name] = []
        foods[name].append(Query(cmd=cmd, t=t, x=x, name=name))
    elif cmd == 200:
        # 사람 추가
        t, x, name, n = int(command[1]), int(command[2]), command[3], int(command[4])
        queries.append( Query(cmd=cmd, t=t, x=x, name=name, n=n) )

        names.add(name)
        positions[name] = x
        entrance_time[name] = t
    else:
        # 사진 촬영
        t = int(command[1])
        queries.append( Query(cmd=cmd, t=t) )

for name in names :
    exit_time[name] = 0
    for sushi in foods[name]:
        sushi_eaten_t = -1

        if sushi.t < entrance_time[name]:
            now_sushi_at = (sushi.x + (entrance_time[name]-sushi.t))%L
            sushi_eaten_t = entrance_time[name] + (positions[name]-now_sushi_at)%L
        else :
            sushi_eaten_t = sushi.t + (positions[name]-sushi.x)%L
        queries.append(Query(cmd=111, t=sushi_eaten_t))

        exit_time[name] = max(exit_time[name], sushi_eaten_t)

    queries.append(Query(cmd=222, t=exit_time[name]))

queries.sort(key=lambda q: (q.t, q.cmd))

num_human, num_sushi = 0, 0
for q in queries :
    if q.cmd == 100:
        num_sushi += 1
    elif q.cmd == 200:
        num_human += 1
    elif q.cmd == 111 :
        num_sushi -= 1
    elif q.cmd == 222 :
        num_human -= 1
    else :
        print(num_human, num_sushi)