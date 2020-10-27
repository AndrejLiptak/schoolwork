def count_letters(text):
    count = 0
    for ch in text:
        if ch not in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
            count += 1
    return count


def custom_sort(array):
    """Selection sort"""
    for i in range(len(array) - 1):
        smallest = i
        for j in range(i + 1, len(array)):
            if count_letters(array[j]) < count_letters(array[smallest]):
                smallest = j
        array[i], array[smallest] = array[smallest], array[i]
