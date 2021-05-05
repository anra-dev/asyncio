def fib(n):
    if n == 1:
        return 1
    if n == 0:
        return 0
    return fib(n-2) + fib(n-1)

def fib_c(n):
    fn1 = 1
    fn2 = 0
    for i in range(n-1):
        fn = fn1 + fn2
        fn2 = fn1
        fn1 = fn
    return fn
