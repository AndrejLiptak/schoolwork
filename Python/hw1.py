import turtle
import math


def hook_star(count, ray_length, hook_length):
    julia = turtle.Turtle()
    for i in range(count):
        julia.forward(ray_length)
        julia.right(60)
        julia.forward(hook_length)
        julia.backward(hook_length)
        julia.left(60)
        julia.backward(ray_length)
        julia.left(360 / count)


def flag_with_triangle(width, height, triangle_ratio):
    julia = turtle.Turtle()
    triangle_base_angle = math.degrees(math.atan((width * triangle_ratio)
                                                 / (height / 2)))
    for _ in range(2):
        julia.forward(width)
        julia.left(90)
        julia.forward(height)
        julia.left(90)
    julia.left(90)
    julia.right(triangle_base_angle)
    julia.forward(math.sqrt((width * triangle_ratio) ** 2 + (height / 2) ** 2))
    julia.left(triangle_base_angle * 2)
    julia.forward(math.sqrt((width * triangle_ratio) ** 2 + (height / 2) ** 2))


def common_multiples(count, num_a, num_b):
    least_common_multiple = 0
    j = max(num_a, num_b)
    while least_common_multiple == 0:
        if j % num_a == 0 and j % num_b == 0:
            least_common_multiple = j
        j += 1
    for i in range(count):
        print(least_common_multiple * (i + 1), end=" ")


def heel_i(size):
    heel = 'I' * (round(size / 4) * 2 + 1)
    print("{0:.^{1}}".format(heel, size))


def print_i(size):
    heel_i(size)
    for _ in range(size - 2):
        print("{0:.^{1}}".format('I', size))
    heel_i(size)


def table_min(size):
    width = (len(str(size))) + 1
    print("{0:>{1}}".format('|', width + 1), end="")
    for number in range(1, size + 1):
        print("{0:>{1}}".format(number, width), end="")
    print()
    for column in range(width * (size + 1) + 2):
        if column == width:
            print("+", end="")
        else:
            print("-", end="")
    print()
    for row in range(1, size + 1):
        print("{0:>{1}}".format(row, width - 1), end=" |")
        for column in range(1, size + 1):
            print("{0:>{1}}".
                  format(row if column > row else column, width), end="")
        print()


def multi_prime_divisor(num, power):
    i = 1
    while num >= i:
        i += 1
        if num % (i ** power) == 0:
            print(i, end=" ")
        while num % i == 0:
            num //= i
