def square(n,m,char):
    for i in range(m):
        for j in range(n):
            print(char, end=" ")
        print()


def empty_square(n,m):
    for i in range(m):
        for j in range(n):
            if i == 0 or j == 0 or j == n-1 or i == m-1:
                print("#", end=" ")
            else:
                print(" ", end=" ")
        print()

def first_n(number, n):
    for i in range(number, n+number):
        print(i, end=" ")
    print()

def last_number(number, n):
    for i in range(number - n + 1, number+1):
        print(i, end=" ")
    print()

def table_products(n):
    length = len(str(n*n) + str(n))
    for _ in range(length + 3):
        print(" ",end="")
    for _ in range(n):
        print('-', end=" ")
    print()
    for i in range(1 ,n+1):
        print(i,"|", end=" ")
        for j in range(1, n+1):
            print(i*j, end=" ")
        print()

table_products(5)



last_number(2,10)


first_n(2,10)
empty_square(10,4)
square(5, 3, "?")