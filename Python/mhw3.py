def series(n):
    total = 1
    for i in range(58,n+1,256):
        total *= i
    return total


def cifs(n):
    total = 0
    for i in range(len(str(n))):
        total += (n % 10) * (i+1)
        n = n // 10
    return total
