from turtle import *

# Draw triangle
def draw_triangle(length):
    """
        This function creates an equilateral triangle 
        with side of length {length} units.
    """
    # Hardcoded range, vs input param
    for sides in range(0, 3):
        forward(length)
        left(120)