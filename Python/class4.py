import random


def how_many(n):
    my_min = 100
    my_max = 0
    sumary = 0
    for _ in range(n):
        x = random.randint(0, 100)
        my_max = max(my_max, x)
        my_min = min(my_min, x)
        print(x, end=" ")
        sumary += x
    average = sumary / n
    print()
    print("Minimum:{0:>6}".format(my_min))
    print("Maximum:{0:>6}".format(my_max))
    print("Average:   ", average)


def print_row(size, position):
    print("home", end="  ")
    for i in range(1, size+1):
        print('*' if i == position else '.', end="  ", sep="  ")
    print("pub")


def drunkman_simulator(size, num_steps, start_pos, probability, output):
    if probability < 0 or probability > 1:
        return "ERROR, pravdepodobnost mozes zadat len v intervale <0,1>"
    if start_pos == 0:
        position = size // 2 +1
    else:
        position = start_pos
    if output:
        print_row(size, position)
    for i in range(num_steps):
        step = random.randint(1, 100)
        if step <= probability * 100:
            position -= 1
        else:
            position += 1
        if output:
            print_row(size, position)
        if position == 1 or position == size:
            break
    if position == 1:
        if output:
            print("Drunk guy got home safely in {} steps".format(i+1))
        return True
    elif position == size:
        if output:
            print("Drunk guy is happily drinking some fine beer in the pub after {} steps".format(i+1))
        return False
    else:
        if output:
            print("Drunk guy fell asleep on the street")
        return False

def drunkman_analysis(size, steps, count):
    got_home = 0
    for _ in range(1, count + 1):
        if drunkman_simulator(size, steps, False):
            got_home += 1
    print("Arriving home in {}% of cases".format(round((got_home / count) * 100, 2)))

#drunkman_analysis(11,100, 100)
print(drunkman_simulator(11,100, 0, 0.5, True))