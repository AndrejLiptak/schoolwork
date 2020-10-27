import turtle


def hanoi(n, start, target, aux):
    if n > 0:
        hanoi(n-1, start, aux, target)
        print(start + ' -> ' + target)
        hanoi(n-1, aux, target, start)

def sequence(n):
    if n == 0:
        return 5
    else:
        return 2*sequence(n-1) -1

def twist(n):
    if n > 0:
        print('TWIST')
        twist(n-1)

def list_sum(l):
    if l:
        return l[0] + list_sum(l[1:])
    return 0

def binary_search(value,numebrs):
    pass

def min_rec(numbers, left, right):
    if left == right:
        return numbers[left]
    else:
        left_min = min_rec(numbers, left, (right + left) // 2)
        right_min = min_rec(numbers, ((right + left) // 2) + 1,right)
        return min(left_min, right_min)


def min_max(numbers):
    return min_rec(numbers, 0, len(numbers) -1)

def quicksort(numbers):
    if len(numbers) == 1 or len(numbers) == 0:
        return numbers
    else:
        pivot = numbers[0]
        left_num = list(filter(lambda x : x <= pivot, numbers[1:]))
        right_num = list(filter(lambda x : x > pivot, numbers[1:]))
        left_part = quicksort(left_num)
        right_part = quicksort(right_num)
        return left_part + [pivot] + right_part

def korch(julia, len, n):
    if n == 0:
        julia.forward(len)
    else:
        korch(julia, len // 3, n-1)
        julia.left(60)
        korch(julia, len // 3, n-1)
        julia.right(120)
        korch(julia, len//3,n-1)
        julia.left(60)
        korch(julia, len//3, n-1)

def sieripinski(depth, len):




julia = turtle.Turtle()
korch(julia, 400, 3)
turtle.done()
