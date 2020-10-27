from typing import List, Optional


def count(array: List[int], target: int) -> int:
    left, right = left_bound(array, target), right_bound(array, target)
    if left is None or right is None:
        return 0
    return right - left + 1


def left_bound(array: List[int], target: int) -> Optional[int]:
    if not array:
        return None
    lower, upper = 0, len(array) - 1
    while lower <= upper:
        if array[lower] == target:
            return lower
        mid = (lower + upper) // 2
        if target > array[mid]:
            lower = mid + 1
        elif target < array[mid]:
            upper = mid - 1
        else:
            upper = mid
    return None


def right_bound(array: List[int], target: int) -> Optional[int]:
    if not array:
        return None
    lower, upper = 0, len(array) - 1
    while lower <= upper:
        if array[upper] == target:
            return upper
        mid = (lower + upper) // 2
        if target > array[mid]:
            lower = mid + 1
        elif target < array[mid]:
            upper = mid - 1
        else:
            if array[mid + 1] != target:
                return mid
            lower = mid
    return None


def tests() -> None:
    assert count([], 2) == 0
    assert count([1], 1) == 1
    assert count([1, 2], 1) == 1
    assert count([1, 1, 2], 1) == 2
    assert count([1, 2], 2) == 1
    assert count([1, 2, 2], 2) == 2
    assert count([1, 2, 3, 4, 5, 6, 7, 9, 9], 9) == 2
    assert count([1, 2, 3, 4, 5, 6, 7, 8, 9], 9) == 1
    assert count([1, 2, 3, 4, 5, 6, 7, 8, 9], 1) == 1
    assert count([1, 2, 3, 4, 5], 3) == 1
