N = int(input())
total = 0

while N > 0:
    num = int(input())
    if num > 0:
        total += num
    N -= 1

print(total)