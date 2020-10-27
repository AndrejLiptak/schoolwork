def multiply_vector(matrix, vector):
    result = []
    for row in range(len(matrix)):
        result.append(0)
        for es in range(len(matrix[row])):
            result[row] += matrix[row][es] * vector[es]
    return result


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
    return (f == '(' and s == ')') or (f == '[' and s == ']') or (f == '{' and s == '}')


def parenthesis_check(value):
    stack = []
    for val in value:
        if val in "([{":
            push(stack, val)
        elif is_empty(stack) or not is_same(top(stack), val):
            return False
        else:
            pop(stack)
    if not is_empty(stack):
        return False
    return True


def most_frequent_set(lst):
    items = set(lst)
    best = [-1, -1]
    for item in items:
        occurrence = lst.count(item)
        if occurrence > best[1]:
            best = [item, occurrence]
    return best


def most_frequent(lst):
    book = {}
    for val in lst:
        if val in book:
            book[val] = book.get(val) + 1
        else:
            book[val] = 1
    return book


def most_frequent_dict(text):
    freq = {}
    text = "".join(ch.lower() for ch in text if ch.isalpha())
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    s = (sorted(freq.items(), key=lambda x: x[1], reverse=True))
    for ch, val in s:
        print(ch, '=', val, sep=" ")
