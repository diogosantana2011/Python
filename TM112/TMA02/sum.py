# Problem: Compute sum of a list of numbers
numbers = [3.0, -4.5, 2.9]

# Tests
# empty list: []
# 1 item: 0 
# borderline output: -4, 4
# bordelines output: 4, -3
# borderline output: -4, 3
# floating-point values: 3.0, -4.5, 2.9
# original value: 4, -1

total = 0
for number in numbers:
    total = total + number
    
print('The sum of', numbers, 'is', total)
