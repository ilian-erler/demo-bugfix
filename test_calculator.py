from calculator import divide, average, first_element

def test_divide():
    assert divide(10, 2) == 5

def test_average():
    assert average([1, 2, 3]) == 2.0

def test_first_element():
    assert first_element([1, 2, 3]) == 1