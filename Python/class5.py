def find_max(lst):
    maximum = lst[0]
    for value in lst:
        if maximum < value:
            maximum = value
    print(maximum)


def find_min(lst):
    minimum = lst[0]
    for value in lst:
        if minimum > value:
            minimum = value
    print(minimum)


def list_sum(lst):
    total = 0
    for value in lst:
        total += value
    print(total)


def nonzero_product(numbers):
    product = 1
    for value in numbers:
        if value != 0:
            product *= value
    print(product)


def double_all(numbers):
    for pos in range(len(numbers)):
        numbers[pos] *= 2
    print(numbers)


def create_double(numbers):
    result = map(lambda x: x * 2, numbers)
    print(list(result))


def linear_search(value, lst):
    for val in lst:
        if val == value:
            return True
    return False


def flatten(lists):
    my_list = []
    for lst in lists:
        for value in lst:
            my_list.append(value)
    print(my_list)


def reverse_extended(string, ch, value):
    return (ch * value).join(string[::-1])


def value(word):
    word = word.upper()
    values = []
    for char in word:
        values.append(ord(char) - ord('A') + 1)
    return sum(values)


def ceasar(word, move):
    word = word.upper()
    cypher = ""
    for char in word:
        cypher += chr((((ord(char) + move) - ord('A')) % 26) + ord('A'))
    return cypher


find_max([1, 2, 3, 4, 2, 3, 18, 1])
find_min([6, 7, 3, 2, ])
list_sum([2, 3, 1, 5])
nonzero_product([1, -2, 3, 0, 5])
create_double([1, 2, 3])
double_all([1, 2, 3])
print(linear_search(2, [1, 3, 2, 4]))
flatten([[1, 2, 3], [5, 1, 2], [4, 1]])
print(reverse_extended("hello", '#', 2))
print(value("hello"))
print(ceasar("Python", 2))
