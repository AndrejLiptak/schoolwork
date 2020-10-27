from datetime import datetime, date
from typing import Dict, Tuple, Set, List


# ========================================
# Task 1: Bank (4 points)
# ========================================


def load_file(file_name: str) -> str:
    with open(file_name, 'r') as my_file:
        return my_file.read()


def arguments_num_error(line):
    print("Invalid number of arguments on line {}.".format(str(line)))


def invalid_argument(instruction, line):
    print("Instruction \"{}\" called with an invalid argument on line {}."
          .format(instruction, str(line)))


def create(line_num, line, accounts):
    if len(line) != 3:
        arguments_num_error(line_num)
        return False
    if line[1] in accounts.keys() or int(line[2]) < 0:
        invalid_argument("CREATE", line_num)
        return False
    accounts[line[1]] = int(line[2])
    return True


def add(line_num, line, accounts):
    if len(line) != 3:
        arguments_num_error(line_num)
        return False
    if line[1] not in accounts.keys() or int(line[2]) < 0:
        invalid_argument("ADD", line_num)
        return False
    accounts[line[1]] += int(line[2])
    return True


def sub(line_num, line, accounts):
    if len(line) != 3:
        arguments_num_error(line_num)
        return False
    if line[1] not in accounts.keys() or int(line[2]) < 0:
        invalid_argument("SUB", line_num)
        return False
    accounts[line[1]] -= int(line[2])
    return True


def filter_out(line_num, line, accounts, ):
    if len(line) != 3:
        arguments_num_error(line_num)
        return False
    if int(line[1]) < 0 or (line[2] != "MIN" and line[2] != "MAX"):
        invalid_argument("FILTER_OUT", line_num)
        return False
    if line[2] == "MIN":
        sorted_accounts = sorted(accounts,
                                 key=lambda x: (accounts[x], x))
    else:
        sorted_accounts = sorted(accounts,
                                 key=lambda x: (-accounts[x], x))
    n = 0
    while n < int(line[1]) and accounts:
        del accounts[sorted_accounts[n]]
        n += 1
    return True


def aggregate(line_num, line, accounts):
    if len(line) != 3:
        arguments_num_error(line_num)
        return False
    if line[1] not in accounts or line[2] not in accounts:
        invalid_argument("AGGREGATE", line_num)
        return False
    accounts[line[1]] += accounts[line[2]]
    del accounts[line[2]]
    return True


def nationalize(line_num, line, accounts):
    if len(line) != 3:
        arguments_num_error(line_num)
        return False
    if int(line[1]) < 0 or int(line[2]) < 0:
        invalid_argument("NATIONALIZE", line_num)
        return False
    total = 0
    value = int(line[1])
    n = int(line[2])
    sorted_accounts = sorted(accounts, key=lambda x: (-accounts[x], x))
    if "STATE" in accounts:
        sorted_accounts.remove("STATE")
    else:
        accounts["STATE"] = 0
    for acc in range(min((len(sorted_accounts)), n)):
        if accounts[sorted_accounts[acc]] - value < 0:
            total += accounts[sorted_accounts[acc]]
            accounts[sorted_accounts[acc]] = 0
        else:
            total += value
            accounts[sorted_accounts[acc]] -= value
    accounts["STATE"] += total
    return True


def print_bank(line_num, line, accounts):
    if len(line) != 1:
        arguments_num_error(line_num)
        return False
    sorted_accounts = sorted(accounts, key=lambda x: (-accounts[x], x))
    for name in sorted_accounts:
        print("{}: {}".format(name, accounts[name]))


def interpret_file(file_name: str, accounts: Dict[str, int]) -> None:
    file = load_file(file_name).split("\n")
    for line_num in range(1, len(file) + 1):
        line = file[line_num - 1].split(" ")
        if line[0] == "CREATE":
            successful = create(line_num, line, accounts)
            if not successful:
                return None
        elif line[0] == "ADD":
            successful = add(line_num, line, accounts)
            if not successful:
                return None
        elif line[0] == "SUB":
            successful = sub(line_num, line, accounts)
            if not successful:
                return None
        elif line[0] == "FILTER_OUT":
            successful = filter_out(line_num, line, accounts)
            if not successful:
                return None
        elif line[0] == "AGGREGATE":
            successful = aggregate(line_num, line, accounts)
            if not successful:
                return None
        elif line[0] == "NATIONALIZE":
            successful = nationalize(line_num, line, accounts)
            if not successful:
                return None
        elif line[0] == "PRINT":
            successful = print_bank(line_num, line, accounts)
            if not successful:
                return None
        elif line[0] != "":
            print("Invalid instruction \"{}\" on line {}."
                  .format(line[0], line_num))
            return None


# ========================================
# Task 2: Chat (4 points)
# ========================================

Message = Tuple[datetime, str, str]


def to_datetime(value: str) -> datetime:
    return datetime.utcfromtimestamp(int(value))


def parse_message(line: str) -> Message:
    line = line.split(',')
    return to_datetime(line[0]), line[1], line[2]


def latest_messages(chat: List[Message], count: int) -> List[Message]:
    result = []
    chat.sort(key=lambda x: x[0], reverse=True)
    for mes in range(min(len(chat), count)):
        result.append(chat[mes])
    return result


def messages_at(chat: List[Message], day: date) -> List[Message]:
    result = []
    for mes in chat:
        if day == mes[0].date():
            result.append(mes)
    return result


def senders(chat: List[Message]) -> Set[str]:
    result = set()
    for mes in chat:
        result.add(mes[1])
    return result


def message_counts(chat: List[Message]) -> Dict[str, int]:
    result = {}
    for mes in chat:
        result[mes[1]] = result.get(mes[1], 0) + 1
    return result


def mentions(chat: List[Message], user: str) -> List[str]:
    result = []
    wanted = '@' + user
    for mes in chat:
        if wanted in mes[2]:
            result.append(mes[2])
    return result


# ========================================
# Task 3: Longest Word (2 points)
# ========================================
def in_provided(word, provided, case_insensitive):
    for ch in word:
        if case_insensitive and (ch.upper() not in provided
                                 and ch.lower() not in provided):
            return False
        elif not case_insensitive and ch not in provided:
            return False
    return True


def longest_word(text: str, provided_letters: Set[str],
                 case_insensitive: bool = False) -> str:
    word = ""
    result = ""
    for ch in text:
        if ch.isalnum():
            word += ch
        elif in_provided(word, provided_letters, case_insensitive):
            if len(word) > len(result):
                result = word
            word = ""
        else:
            word = ""
    if len(word) > len(result) and \
            in_provided(word, provided_letters, case_insensitive):
        result = word
    return result


# ========================================
# Task 4: Parentheses Check (2 points)
# ========================================
def pop(stack):
    stack.pop()


def push(stack, value):
    return stack.append(value)


def top(stack):
    return stack[-1]


def is_empty(stack):
    if len(stack) == 0:
        return True
    else:
        return False


def is_same(f, s):
    return (f == '(' and s == ')') or \
           (f == '[' and s == ']') or (f == '{' and s == '}')


def parentheses_check(text: str, output: bool = False) -> bool:
    stack = []
    for val in range(len(text)):
        if text[val] not in "([{)]}":
            continue
        elif text[val] in "([{":
            push(stack, (text[val], val))
        elif is_empty(stack):
            if output:
                print("'{}' at position {} does not"
                      " have an opening paired bracket"
                      .format(text[val], str(val)))
            return False
        elif not is_same(top(stack)[0], text[val]):
            if output:
                print("'{}' at position {} "
                      "does not match '{}' at position {}"
                      .format(top(stack)[0], str(top(stack)[1]),
                              text[val], str(val)))
            return False
        else:
            pop(stack)
    if not is_empty(stack):
        if output:
            print("'{}' at position {} does not have a closing paired bracket"
                  .format(top(stack)[0], top(stack)[1]))
        return False
    return True
