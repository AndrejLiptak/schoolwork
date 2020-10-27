def statistics():
    fours = 0
    pocet = 0
    hody = 0
    while fours < 6:
        hody += 1
        hodene = dice()
        print(hodene)
        if hodene == 4:
            fours += 1
        pocet += hodene
    return round(pocet / hody, 2)
