MAX_N = 100001
MAX_D = 22

n, q = 0, 0
a, p, val = [0] * MAX_N, [0] * MAX_N, [0] * MAX_N
noti = [False] * MAX_N
nx = [[0 for _ in range(MAX_D)] for _ in range(MAX_N)]


# 초기 설정 값을 받아옵니다.
def init(inputs):
    global n, a, p, val, nx
    # 부모 채팅과 채팅의 권한 정보를 입력받습니다.
    for i in range(1, n + 1):
        p[i] = inputs[i]

    for i in range(1, n + 1):
        a[i] = inputs[i + n]
        # 채팅의 권한이 20을 초과하는 경우 20으로 제한합니다.
        if a[i] > 20:
            a[i] = 20

    # nx 배열과 val 값을 초기화합니다.
    for i in range(1, n + 1):
        cur = i
        x = a[i]
        nx[cur][x] += 1
        # 상위 채팅으로 이동하며 nx와 val 값을 갱신합니다.
        while p[cur] and x:
            cur = p[cur]
            x -= 1
            if x:
                nx[cur][x] += 1
            val[cur] += 1


# 채팅의 알림 상태를 토글합니다.
def toggle_noti(chat):
    cur = p[chat]
    num = 1
    # 상위 채팅으로 이동하며 noti 값에 따라 nx와 val 값을 갱신합니다.
    while cur:
        for i in range(num, 22):
            val[cur] += nx[chat][i] if noti[chat] else -nx[chat][i]
            if i > num:
                nx[cur][i - num] += nx[chat][i] if noti[chat] else -nx[chat][i]
        if noti[cur]:
            break
        cur = p[cur]
        num += 1
    noti[chat] = not noti[chat]


# 채팅의 권한의 크기를 변경합니다.
def change_power(chat, power):
    bef_power = a[chat]
    power = min(power, 20)  # 권한의 크기를 20으로 제한합니다.
    a[chat] = power

    nx[chat][bef_power] -= 1
    if not noti[chat]:
        cur = p[chat]
        num = 1
        # 상위 채팅으로 이동하며 nx와 val 값을 갱신합니다.
        while cur:
            if bef_power >= num:
                val[cur] -= 1
            if bef_power > num:
                nx[cur][bef_power - num] -= 1
            if noti[cur]:
                break
            cur = p[cur]
            num += 1

    nx[chat][power] += 1
    if not noti[chat]:
        cur = p[chat]
        num = 1
        # 상위 채팅으로 이동하며 nx와 val 값을 갱신합니다.
        while cur:
            if power >= num:
                val[cur] += 1
            if power > num:
                nx[cur][power - num] += 1
            if noti[cur]:
                break
            cur = p[cur]
            num += 1


# 두 채팅의 부모를 교체합니다.
def change_parent(chat1, chat2):
    bef_noti1 = noti[chat1]
    bef_noti2 = noti[chat2]

    if not noti[chat1]:
        toggle_noti(chat1)
    if not noti[chat2]:
        toggle_noti(chat2)

    p[chat1], p[chat2] = p[chat2], p[chat1]

    if not bef_noti1:
        toggle_noti(chat1)
    if not bef_noti2:
        toggle_noti(chat2)


# 해당 채팅의 val 값을 출력합니다.
def print_count(chat):
    print(val[chat])


n, q = map(int, input().split())
inputlist = []
for _ in range(q):
    inputs = list(map(int, input().split()))
    inputlist.append(inputs)

for inputs in inputlist:
    query = inputs[0]
    if query == 100:
        init(inputs)
    elif query == 200:
        chat = inputs[1]
        toggle_noti(chat)
    elif query == 300:
        chat, power = inputs[1], inputs[2]
        change_power(chat, power)
    elif query == 400:
        chat1, chat2 = inputs[1], inputs[2]
        change_parent(chat1, chat2)
    elif query == 500:
        chat = inputs[1]
        print_count(chat)
        breakpoint()