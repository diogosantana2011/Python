""" 
TM112 Library code for TMA02 Q5.
08/10/2017
"""
import math

def median(alist):
    """ Calculates the median of a list of numbers.
The list must not be empty.
"""

    number_of_values = len(alist)
    sorted_list = sorted(alist)

    # Two cases, depending on whether the number of values is odd or even.
    quotient = number_of_values // 2
    remainder = number_of_values % 2
 
    if (remainder == 1):
        result = sorted_list[quotient]
    else:
        result = (sorted_list[quotient - 1] + sorted_list[quotient]) / 2
    return result
        
    
def test_median():
    assert median([2]) == 2
    assert median([4, 3]) == 3.5
    assert median([3, 1, 8, 4, 7, 6, 4, 2, 5, 9]) == 4.5
    assert median([7, 2, 6, 2, 5, 3, 1, 0, 8, 6, 6, 4, 9]) == 5

# Unit test
test_median()

def mean(list):
    """Return mean of list"""
    sum = 0
    count = 0
    for item in list:
        sum = sum + item
        count = count + 1
    return sum / count

def test_mean():
    list = [1, 2, 3, 4, 5]
    assert(mean(list) == 3)
    
# Unit test
test_mean()

def corr_coef(list_x, list_y):
    """ Return correlation between values in list_x and list_y.

    Lists must be of equal length.
    
    """
    
    x_bar = mean(list_x)
    y_bar = mean(list_y)
    sxy = 0
    sxx = 0
    syy = 0
    for index in range(len(list_x)):
        x = list_x[index]
        y = list_y[index]
        sxy = sxy + (x - x_bar) * (y - y_bar)
        sxx = sxx + (x - x_bar) * (x - x_bar)
        syy = syy + (y - y_bar) * (y - y_bar)
    return sxy / math.sqrt(sxx * syy)

def test_corr_coef():
    # Data from M140 Unit 9 Example 5
    list1 = [78.9, 75.8, 77.3, 74.2, 78.1, 72.8, 77.6, 77.9]
    list2 = [56.7, 53.1, 56.1, 55.9, 54.1, 48.6, 59.4, 54.0]
    assert round(corr_coef(list1, list2), 2) == 0.64
    
# Unit test
test_corr_coef()
    
