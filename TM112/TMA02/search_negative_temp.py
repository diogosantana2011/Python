# Problem: find a negative temperature

# Tests
# No item satisfies condition: 1,2,3,4,5,6,7
# all items satisfy condition: -1,-2,-3,-4,-5,-6,-7
# some items satisfy condition: 1,-2,3,-4,5,-6,7
# original value: 4,5,3,1,0,3,-2

# Input
temperatures = []
# Output
negative = None
for temperature in temperatures:
    if temperature < 0:
        negative = temperature
print(temperatures, 'have negative temperatures', negative)

