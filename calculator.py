def divide(a: float, b: float) -> float:
    """Divide two numbers.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The result of a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The arithmetic mean of the numbers.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)


def first_element(lst: list) -> any:
    """Return the first element of a list.

    Args:
        lst: A list of elements.

    Returns:
        The first element of the list.

    Raises:
        ValueError: If the list is empty.
    """
    if not lst:
        raise ValueError("Cannot get first element of empty list")
    return lst[0]