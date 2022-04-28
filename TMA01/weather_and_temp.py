from turtle import *

temp = [0,0,0,0,0,0,0]
total = 0
for loop in range(0, 7):
    # Determine temperature
    temp[loop] = int(input('Please enter the temperature for the day. (Mon-Sun)\n'))
    # Process temperature
    total = total + temp[loop]
    # CHART
    # Draw the graph
    # Draw the x-axis
    goto(120, 0)

    # Draw the y-axis
    goto(0, 0)
    goto(0, 60)
    goto(0, 0)
    for loop in range(0, 7):
        # Plot temp for that day
        goto(20*loop, 2*temp[loop])
        
# Works out the average
average = total/7
print(f'The average temperature for the week is {round(average, 2)}')