from random import randint, random

def treasure_hunter(width, steps):
    t_locationx = randint(1,width)
    t_locationy = randint(1, width)
    posx = 0
    posy = 0
    for _ in range(steps):
        x = randint(1,4)
        if x == 1:
            if posx  < width:
                posx += 1
        elif x == 2:
            if posy  < width:
                posy += 1
        elif x == 3:
            if posx > 0:
                posx -= 1
        elif x == 4:
            if posy > 0:
                posy -= 1
        if t_locationx == posx and t_locationy == posy:
            print(t_locationx, t_locationy, sep=" ")
            print(posx, posy, sep=" ")
            return True
    print(t_locationx, t_locationy, sep=" ")
    print(posx, posy, sep=" ")
    return False


def random_student(n, count):
    half_test = 0
    for _ in range(count):
        test = 0
        for i in range(n):
            correct = randint(1, 4)
            guess = randint(1, 4)
            if correct == guess:
                test += 1
        if test >= n // 2:
            half_test += 1
    return half_test / count

print(random_student(2, 1000))
