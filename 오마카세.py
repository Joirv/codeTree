class Query:
    def __init__ (self, cmd, t=-1, x=-1, name="", n=-1):
        self.cmd = cmd
        self.t = t
        self.x = x
        self.name = name
        self.n = n

queries = []
names = set()
position = dict()   # name : position
foods = dict()      # name : [sushi]
entry_time = dict() # name : entry time
exit_time = dict()  # name : exit time

L, Q = map(int, input().split())

for i in range(Q):
    inputs = input().split()
    cmd = inputs[0]

    if cmd == "100":   # 주방장의 초밥 만들기
        t, x, name= int(inputs[1]), int(inputs[2]), inputs[3]
        queries.append(Query(100, t=t, x=x, name=name))

        if name not in foods:
            foods[name] = []
        foods[name].append(Query(100, t=t, x=x, name=name))

    elif cmd == "200": # 손님 입장
        t, x, name, n = int(inputs[1]), int(inputs[2]), inputs[3], int(inputs[4])
        queries.append(Query(200, t=t, x=x, name=name, n=n))

        names.add(name)
        entry_time[name] = t
        position[name] = x

    else:    # 사진 촬영
        t = int(inputs[1])
        queries.append(Query(300, t=t))


for name in names:
    exit_time[name] = -1
    for sushi in foods[name]:
        sushi_removed_t = -1
        if sushi.t < entry_time[name]:
            entry_sushi_x = (sushi.x + entry_time[name] - sushi.t) % L
            sushi_removed_t = entry_time[name] + (position[name]-entry_sushi_x) % L
        else :
            sushi_removed_t = sushi.t + (position[name]-sushi.x)%L

        queries.append(Query(111, t=sushi_removed_t, x=sushi.x, name=name))
        exit_time[name] = max(sushi_removed_t, exit_time[name])
    queries.append(Query(222, t=exit_time[name], x=position[name], name=name))

queries.sort(key=lambda c : (c.t, c.cmd))
# t 순으로 정렬하되, t가 같을 경우 300이 뒤로 가도록

num_human, num_sushi = 0, 0
for i in range(len(queries)):
    if queries[i].cmd == 100 :
        num_sushi += 1
    elif queries[i].cmd == 111 :
        num_sushi -= 1
    elif queries[i].cmd == 200 :
        num_human += 1
    elif queries[i].cmd == 222 :
        num_human -= 1
    else :
        print(num_human, num_sushi)
