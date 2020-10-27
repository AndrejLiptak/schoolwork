import random
from typing import Optional, List, Tuple

game_plan = List[List[str]]


def new_playground(height: int, width: int) -> game_plan:
    return [[" " for _ in range(width)] for _ in range(height)]


def get(playground: game_plan, row: int, col: int) -> str:
    return playground[row][col]


def drop(playground: game_plan, col: int, symbol: str) -> bool:
    dropped = False
    row = len(playground) - 1
    while not dropped and row >= 0:
        if playground[row][col] == " ":
            playground[row][col] = symbol
            dropped = True
        row -= 1
    return dropped


def draw(playground: game_plan) -> None:
    for row in range(len(playground)):
        print("   ", end="")
        for _ in range(len(playground[0])):
            print("+---", end="")
        print("+")
        print(" " + chr(ord('A') + row), end=" ")
        for col in range(len(playground[0])):
            print("|", end="")
            print("{0: ^3}".format(get(playground, row, col)), end="")
        print("|")
    print("   ", end="")
    for _ in range(len(playground[0])):
        print("+---", end="")
    print("+")
    print("    ", end="")
    for n in range(len(playground[0])):
        print("{0: ^4}".format(n), end="")
    print()


def check_win(s: str) -> Tuple[bool, bool]:
    x_won = False
    o_won = False
    for i in range(len(s) - 3):
        if s[i] == s[i + 1] == s[i + 2] == s[i + 3]:
            if s[i] == 'X' and (i + 4 == len(s) or s[i + 4] != 'X') \
                    and (i - 1 == -1 or s[i - 1] != 'X'):
                x_won = True
            elif s[i] == 'O' and (i + 4 == len(s) or s[i + 4] != 'O') \
                    and (i - 1 == -1 or s[i - 1] != 'O'):
                o_won = True
    return x_won, o_won


def horizontal_check(playground: game_plan, max_height: int) \
        -> Tuple[bool, bool]:
    horiz_x, horiz_o = False, False
    row = len(playground) - 1
    while row >= max_height and row >= 0:
        horiz_string = ""
        for col in range(len(playground[0])):
            horiz_string += playground[row][col]
        line_x, line_o = check_win(horiz_string)
        if line_x and not horiz_x:
            horiz_x = True
        if line_o and not horiz_o:
            horiz_o = True
        row -= 1
    return horiz_x, horiz_o


def vertical_check(playground: game_plan) -> Tuple[bool, bool]:
    ver_x, ver_o = False, False
    for col in range(len(playground[0])):
        ver_string = ""
        row = len(playground) - 1
        while playground[row][col] != " " and row >= 0:
            ver_string += playground[row][col]
            row -= 1
        line_x, line_o = check_win(ver_string)
        if line_x and not ver_x:
            ver_x = True
        if line_o and not ver_o:
            ver_o = True
    return ver_x, ver_o


def diagonal_check(playground: game_plan, max_height: int) \
        -> Tuple[bool, bool]:
    diag_x, diag_o = False, False
    if len(playground) > 3 and len(playground[0]) > 3 \
            and len(playground) - max_height >= 5:
        # diagonals starting at the bottom
        row = len(playground) - 1
        for col in range(len(playground[0]) - 3):
            r = row
            c = col
            diag_string = ""
            while c <= len(playground[0]) - 1 and r > max_height:
                diag_string += playground[r][c]
                r -= 1
                c += 1
            line_x, line_o = check_win(diag_string)
            if line_x and not diag_x:
                diag_x = True
            if line_o and not diag_o:
                diag_o = True
        # other diagonals on the side
        for row in range(len(playground) - 2, max_height + 3, -1):
            r = row
            c = 0
            diag_string = ""
            while c <= len(playground[0]) - 1 and r > max_height:
                diag_string += playground[r][c]
                r -= 1
                c += 1
            line_x, line_o = check_win(diag_string)
            if line_x and not diag_x:
                diag_x = True
            if line_o and not diag_o:
                diag_o = True
        # opposite diagonals
        row = len(playground) - 1
        for col in range(len(playground[0]) - 1, 2, -1):
            r = row
            c = col
            diag_string = ""
            while c >= 0 and r > max_height:
                diag_string += playground[r][c]
                r -= 1
                c -= 1
            line_x, line_o = check_win(diag_string)
            if line_x and not diag_x:
                diag_x = True
            if line_o and not diag_o:
                diag_o = True
        for row in range(len(playground) - 2, max_height + 3, -1):
            r = row
            c = len(playground[0]) - 1
            diag_string = ""
            while c >= 0 and r > max_height:
                diag_string += playground[r][c]
                r -= 1
                c -= 1
            line_x, line_o = check_win(diag_string)
            if line_x and not diag_x:
                diag_x = True
            if line_o and not diag_o:
                diag_o = True
    return diag_x, diag_o


def who_won(playground: game_plan) -> Optional[str]:
    x_won = False
    o_won = False
    # determine highest row that have symbol in it,
    # so the function will only check relevant rows and diagonals
    max_height = len(playground) - 1
    while ("X" in playground[max_height] or "O" in playground[max_height]) \
            and max_height >= 0:
        max_height -= 1
    # horizontal check
    horiz_x, horiz_o = horizontal_check(playground, max_height)
    if horiz_x and not x_won:
        x_won = True
    if horiz_o and not o_won:
        o_won = True
    # vertical check
    ver_x, ver_o = vertical_check(playground)
    if ver_x and not x_won:
        x_won = True
    if ver_o and not o_won:
        o_won = True
    # diagonal check
    diag_x, diag_o = diagonal_check(playground, max_height)
    if diag_x and not x_won:
        x_won = True
    if diag_o and not o_won:
        o_won = True
    # final check
    if x_won and o_won:
        return "invalid"
    elif x_won:
        return "X"
    elif o_won:
        return "O"
    elif " " not in playground[0]:
        return "tie"
    return None


def strategy_drop(playground: game_plan, col: int, symbol: str) \
        -> Tuple[int, bool]:
    dropped = False
    row = len(playground) - 1
    while not dropped and row >= 0:
        if playground[row][col] == " ":
            playground[row][col] = symbol
            dropped = True
            return row, dropped
        row -= 1
    return -1, dropped


def strategy(playground: game_plan, symbol: str) -> int:
    copy = [x[:] for x in playground]
    if symbol == "X":
        enemy_symbol = "O"
    else:
        enemy_symbol = "X"
    dont_lose = -1
    for col in range(len(playground[0])):
        row, is_viable_drop = strategy_drop(copy, col, symbol)
        if is_viable_drop:
            pc_win = who_won(copy)
            if pc_win == symbol:
                return col
            # check if losing can be prevented
            copy[row][col] = enemy_symbol
            if who_won(copy) == enemy_symbol:
                dont_lose = col
            copy[row][col] = " "
    if dont_lose != -1:
        return dont_lose
    col = random.randint(0, len(playground[0]) - 1)
    while playground[0][col] != " ":
        col = random.randint(0, len(playground[0]) - 1)
    return col


def game(height: int, width: int) -> None:
    plan = new_playground(height, width)
    draw(plan)
    inp = ""
    while inp != "y" and inp != "n":
        inp = input("Do you want to go first? y/n ")
        if inp != "y" and inp != "n":
            print("Type y if you want to go first, n if second")
    if inp == "y":
        player_turn = True
        pc_turn = False
    else:
        player_turn = False
        pc_turn = True
    while who_won(plan) != "X" and who_won(plan) != "O" \
            and who_won(plan) != "tie":
        if player_turn:
            draw(plan)
            player_c = input("Choose column ")
            if player_c.isdigit() and 0 <= int(player_c) < len(plan[0]):
                if not drop(plan, int(player_c), "X"):
                    print("Select column which is not full!")
                    continue
            else:
                print("Please only type numbers in range 0-{0}"
                      .format(len(plan) - 1))
                continue
        if pc_turn:
            drop(plan, strategy(plan, "O"), "O")
        if pc_turn:
            player_turn = True
            pc_turn = False
        else:
            player_turn = False
            pc_turn = True
    draw(plan)
    if who_won(plan) == "X":
        print("Congratulations! You won!")
    elif who_won(plan) == "O":
        print("GAME OVER!! You lost! Better luck next time")
    else:
        print("It`s a tie!")
