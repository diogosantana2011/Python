# Draw three triangles
## using turtle

from turtle import *
import turtle as ws
from figure_drawing_functions import *

# Draw triangle
draw_triangle(40)

# Move to position for second triangle
penup()
forward(100)
pendown()

# Draw triangle
draw_triangle(40) 
    
penup()
left(180)  
forward(100)
right(90)
forward(100)
right(90)
pendown()

# Draw triangle
draw_triangle(40)
    
ws.exitonclick()