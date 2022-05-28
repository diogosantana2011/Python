from turtle import *
import turtle

ws = turtle.Screen()
numshapes = 5
start_x_pos = -320
start_y_pos = 0

# Range +1 to count also 5th shape 
# Otherwise range woudl stop at 4
for shape in range(1, numshapes+1):
    start_x_pos += 100
    for sides in range(1, 9):
        penup()
        goto(start_x_pos, start_y_pos)
        pendown()
        
        forward(40)
        left(45)

# Individual shape
# for sides in range(1, 9):
#         penup()
#         goto(start_x_pos, start_y_pos)
#         pendown()
        
#         forward(40)
#         left(45)
ws.exitonclick()       