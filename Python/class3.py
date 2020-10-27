import math


def factorial_a(n):
    total = 1
    if n == 0:
        return 1
    for i in range(2, n + 1):
        total *= i
    return total


def factorial_b(n):
    if n == 0:
        return 1
    total = 1
    i = 2
    while i <= n:
        total *= i
        i += 1
    return total


def digit_sum(n):
    sum_n = 0
    while n > 0:
        sum_n += n % 10
        n //= 10
    return sum_n


def repeated_digits_sum(n):
    while n // 10 > 0:
        n = digit_sum(n)
    return n


def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def is_devisor(n, k):
    return n % k == 0


def devisors(n):
    for i in range(1, n + 1):
        if is_devisor(n, i):
            print(i, end=" ")


def devisors_count(n):
    count = 1
    for i in range(1, (n // 2) + 1):
        if is_devisor(n, i):
            count += 1
    return count


def is_prime(n):
    if n == 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def primes_less_than(limit):
    if limit in range(3):
        print('Nie su')
        return
    for i in range(2, limit):
        if is_prime(i):
            print(i, end=" ")


def kth_prime(k):
    prime_count = 0
    n = 1
    while prime_count < k:
        n += 1
        if is_prime(n):
            prime_count += 1
    return n


def primes(count):
    currect_count = 0
    n = 1
    while currect_count < count:
        n += 1
        if is_prime(n):
            print(n, end=" ")
            currect_count += 1


def prime_twins(count):
    currect_count = 0
    n = 2
    while currect_count < count:
        n += 1
        if is_prime(n) and is_prime(n + 2):
            print("({}, {})".format(n, n + 2), end=" ")
            currect_count += 1


def pi():
    n = 1
    total = 0
    for i in range(1, 1000, 2):
        total += n * 1 / i
        n *= -1
    return total * 4


def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


def e(n):
    my_e = 0
    number = 0
    # while round(my_e,n) != round(math.e,n):
    for i in range(10):
        my_e += 1 / factorial(number)
        number += 1
    return my_e


def sinus(x):
    total = 0
    sign = 1
    for i in range(1, 100, 2):
        total += sign * (x ** i / factorial(i))
        sign *= -1
    return round(total, 5)


def convert_10_to_2(n):
    binary = ""
    while n != 0:
        binary = str(n % 2) + binary
        n //= 2
    return binary


def convert_2_to10(n):
    decimal = 0
    position = 0
    for b in n[::-1]:
        decimal += int(b) * (2 ** position)
        position += 1
    return decimal


def convert_10_to_x(n, symbols):
    size = len(symbols)
    final = ""
    while n != 0:
        final = symbols[(n % size)] + final
        n //= size
    return final


def convert_x_to_10(n, symbols):
    decimal = 0
    position = 0
    size = len(symbols)
    for b in n[::-1]:
        decimal += symbols.index(b) * (size ** position)
        position += 1
    return decimal


def convert_x_to_y(n, symbols1, symbols2):
    return convert_10_to_x(convert_x_to_10(n, symbols1), symbols2)


print(convert_x_to_y("2C", "0123456789ABCDEF", "$*&!"))
# print(convert_x_to_10("2B", "0123456789ABCDEF"))
# print(convert_10_to_x(42, "0123456789ABCDEF"))
# print(convert_10_to_x(42, "0123456789"))
# print(convert_10_to_x(42, "0123"))
# print(convert_2_to10("110110"))
# print(convert_10_to_2(8))
# print(sinus(math.pi / 2))
# print(math.sin(math.pi / 2))
# print(factorial_a(5))
# print(factorial_b(5))
# print(digit_sum(1345))
# print(repeated_digits_sum(99989788879879))
# print(lcm(23, 42))
# devisors(1024)
# print(devisors_count(1024))
# primes_less_than(100)
# print()
# print(kth_prime(100))
# primes(10)
# print()
# prime_twins(10)
# print()
# print(pi())
