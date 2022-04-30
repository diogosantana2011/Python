#Draw a person
from turtle import *
import turtle

ws = turtle.Screen()

#Draw head
for sides in range(1, 5):
    forward(20)
    left(90)

#Torso position
forward(10)
right(90)

#Draw Torso
forward(40)

#Arms position
left(180)
forward(20)
right(90)

#Draw arms
forward(40)
right(180)
forward(80)
right(180)
forward(40)

#Legs position
right(90)
forward(20)

# Draw legs
left(30)
forward(40)
right(180)
forward(40)
left(120)
forward(40)

ws.exitonclick()