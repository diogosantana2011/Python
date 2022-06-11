# Draw three triangles
## using turtle

from turtle import *
import turtle as ws

numshapes = 3
start_x_pos = 0
start_y_pos = 0

# Draw triangle
for sides in range(0, 3):
    forward(40)
    left(120)
    
# Move to position for second triangle
penup()
forward(100)
pendown()

# Draw triangle
for sides in range(0, 3):
    forward(40)
    left(120)   
    
penup()
left(180)  
forward(100)
right(90)
forward(100)
right(90)
pendown()

# Draw triangle
for sides in range(0, 3):
    forward(40)
    left(120)  
    
ws.exitonclick()