N = int(input())  

if N < 0:
    total = sum(range(-1, N - 1, -1))
elif N > 0:
    total = sum(range(1, N + 1))
else:
    total = 0

print(total)