# sort_numbers_v2.py

def sort_numbers_v2(numbers):
    if not isinstance(numbers, list):
        raise ValueError("Input should be a list")
    for i in numbers:
        if not isinstance(i, int) and not isinstance(i, float):
            raise ValueError("List items should be an integer or a float")
    return sorted(numbers)
