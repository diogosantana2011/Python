from turtle import *
import turtle

ws = turtle.Screen()
start_x_pos = -320
start_y_pos = 0

def draw_shape(x, y):
    penup()
    setposition(x, y) 
    pendown()

    forward(40)
    left(45)

# Individual shape
# for spoke in range(1, 9):
#     draw_shape(start_x_pos, start_y_pos) 

# Range +1 to count also 5th shape 
# Otherwise range woudl stop at 4
for shape in range(1, 6):
    start_x_pos += 100
    start_y_pos += 0
      
    for spoke in range(1, 9):
        draw_shape(start_x_pos, start_y_pos) 
        
ws.exitonclick()       