N = int(input())  
res = ''

if N == 0:
    res = "0"
else:
    while N > 0:
        res = str(N & 1) + res
        N >>= 1
print(res)