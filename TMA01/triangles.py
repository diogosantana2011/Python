# Triangles
from turtle import *
import turtle

ws = turtle.Screen()

# Triangle 1
for sides in range(1,4):
    forward(60)
    left(120)
    
# Move to position 
penup()
forward(100)
pendown()

# Triangle 2
for sides in range(1,4):
    forward(40)
    left(120)
    
# Move to position
penup()
left(180)
forward(100)
right(90)
forward(100)
right(90)
pendown()    

# Triangle 3
for sides in range(1,4):
    forward(40)
    left(120)
    
ws.exitonclick()