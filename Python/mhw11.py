from typing import List, Any


def flat_rec(to_flatten, result, depth):
    for i in range(len(to_flatten)):
        if isinstance(to_flatten[i], list):
            flat_rec(to_flatten[i], result, depth + 1)
        else:
            result.append(depth * "/" + str(to_flatten[i]))


def flatten(to_flatten: List[Any]) -> List[Any]:
    result = []
    flat_rec(to_flatten, result, 1)
    return result

def is_mail(word):
    if '@' not in word or ".." in word:
        return False
    splitted = word.split('@')
    if len(splitted) != 2:
        return False
    for let in splitted[0]:
        if not let.isalnum() and let not in "-._":
            return False
    for let in splitted[1]:
        if not let.isalnum() and let not in "-._":
            return False
    if "moc." != splitted[1][:-5:-1] and "ks." != splitted[1][:-4:-1] and "zc." != splitted[1][:-4:-1]:
        return False
    return True


def contains_mail(string):
    string = string.split(' ')
    result = []
    for word in string:
        if is_mail(word):
            result.append(word)
    return result
