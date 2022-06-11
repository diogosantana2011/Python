# Draw three triangles
## using turtle

from turtle import *
import turtle as ws

# Input:
numshapesinput = int(input('Please enter numnber of triangles to draw: '))

# Remove duplicate code:
## Add draw triangle funct
def draw_triangle(numshapes):
    f"""
        This function creates a triangle 
        at position-x: 0, position-y: 0
        of 40 units length and 120 left angle.
    """
    for sides in range(0, numshapes):
        forward(40)
        left(120)

# Draw triangle
draw_triangle(numshapesinput)

# Move to position for second triangle
penup()
forward(100)
pendown()

# Draw triangle
draw_triangle(numshapesinput)

penup()
left(180)  
forward(100)
right(90)
forward(100)
right(90)
pendown()

# Draw triangle
draw_triangle(numshapesinput)
    
ws.exitonclick()