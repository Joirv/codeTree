from heapq import *



x = {1: [0, 1, 2], 2: [0, 0, 0]}
x[2][0] = 1
print(x)

stack = [1,2,3,4]
print(stack.pop(-1))
print(stack)

stackk = [1]
print(stackk.pop(-1))
print(stackk)
print(5%2)

kk = {1: 0, 2: 1}
print(kk)
node = (1,2)
for i in node:
    if kk[i]==1:
        kk.pop(i)
print(kk)