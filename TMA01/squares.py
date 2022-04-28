from turtle import *
number_of_shapes = 4

for shape in range(1, number_of_shapes + 1):
    for sides in range(1, 5):
        forward(40)
        right(90)
        
        penup()
        forward(50)
        pendown()