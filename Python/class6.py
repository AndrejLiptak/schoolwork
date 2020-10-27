from typing import List, Optional
from random import randint


def avg(marks: List[int]) -> float:
    assert len(marks) != 0, "No mark given!"
    return sum(marks) / len(marks)


def find_max(lst: List[int]) -> int:
    assert len(lst) != 0, "si chobot"
    maximum = lst[0]
    for value in lst:
        if maximum < value:
            maximum = value
    return maximum


def guess_number(n: int) -> Optional[int]:
    assert n >= 1, "Number must be bigger then 0"
    number = randint(1, n)
    guessed = 0
    attempt = 0
    while guessed != number:
        attempt += 1
        print("Attempt ", attempt)
        guessed = int(input("Type your guess: "))
        if guessed < number:
            print("My number is higher")
        elif guessed > number:
            print("My number is lower")
        else:
            print("Correct !")
        print()
    return attempt


def find_my_number(ran: int) -> int:
    lower = 1
    upper = ran
    while lower != upper:
        mid = (upper + lower) // 2
        ishigher = input("Is your number higher then {}".format(mid))
        if ishigher == "y":
            lower = mid + 1
        else:
            upper = mid
    print("Your number is ", lower)
    return lower


def binary_search(needle, haystack):
    lower = 0
    upper = len(haystack) - 1
    steps = 0
    while lower <= upper:
        steps += 1
        mid = (upper + lower) // 2
        if haystack[mid] == needle:
            return steps
        elif needle < haystack[mid]:
            upper = mid - 1
        else:
            lower = mid + 1
    return steps

def create_random_list(length):
     return sorted([randint(1,length) for i in range(length)])

def analyse_search(lenght,repetitions = 1000):
    sum_of_steps = 0
    for _ in range(repetitions):
        random_list = create_random_list(lenght)
        sum_of_steps += binary_search(randint(1,lenght * 2), random_list)
    return round(sum_of_steps / repetitions, 2)

print(analyse_search(100))
