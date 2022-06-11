# Return length of a list
def list_length(a_list):
    """
    Return the length of a list
    """
    length = 0
    for item in a_list:
        length = length + 1
    return length

# Test Length of lists
def test_list_length():
    """
    Test the list_length() function.
    """
    assert list_length([]) == 0
    assert list_length([1]) == 1
    assert list_length([1, 1]) == 2
    assert list_length([1, 1, 3]) == 3
    assert list_length([1, 2, 3, 4]) == 4
    assert list_length([1, 2, 3, 4, 6]) == 5

test_list = list_length([1, 2, 3, 4, 5])
test_list_length()