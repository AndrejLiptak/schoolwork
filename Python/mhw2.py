def print_t(size):
    for i in range(size):
        print('T', end="")
    print()
    for j in range(size - 1):
        for i in range(size):
            if i == size // 2:
                print('T', end="")
            else:
                print('.', end="")
        print()
