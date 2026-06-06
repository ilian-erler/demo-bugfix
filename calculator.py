def divide(a, b):
    if b == 0:
        return None
    return a / b

def average(numbers):
    if len(numbers) == 0:
        return None
    return sum(numbers) / len(numbers)

def first_element(lst):
    if len(lst) == 0:
        return None
    return lst[0]