# Draw three triangles
## using turtle

from turtle import *
import turtle as ws

# Remove duplicate code:
## Add draw triangle funct
def draw_triangle():
    """
        This function creates an equilateral triangle 
        with side of length 40 units.
    """
    # Hardcoded range, vs input param
    for sides in range(0, 3):
        forward(40)
        left(120)

draw_triangle()

# Move to position for second triangle
penup()
forward(100)
pendown()

# Draw triangle
draw_triangle() 
    
penup()
left(180)  
forward(100)
right(90)
forward(100)
right(90)
pendown()

# Draw triangle
draw_triangle()
    
ws.exitonclick()