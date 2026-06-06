from calculator import divide, average, first_element

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    assert divide(10, 0) is None

def test_average():
    assert average([1, 2, 3]) == 2.0

def test_average_empty_list():
    assert average([]) is None

def test_first_element():
    assert first_element([1, 2, 3]) == 1

def test_first_element_empty_list():
    assert first_element([]) is None