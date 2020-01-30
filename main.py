def fib(n):
    a, b = 0, 1
    for m in range(n):
        print(a)
        a, b = b, a + b


fib(100)
