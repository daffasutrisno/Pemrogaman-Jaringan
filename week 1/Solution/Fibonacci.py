def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

N = int(input())
if N <= 1:
    print(fibonacci(N))
else:
    print(fibonacci(N - 1))