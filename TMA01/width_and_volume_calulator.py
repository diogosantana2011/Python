brick_width = int(float(input('Please enter a numerical value for width: ')))
brick_length = int(float(input('Please enter a numerical value for length: ')))
brick_height = int(float(input('Please enter a numerical value for height: ')))

area = brick_length * brick_width
volume = area * brick_height

print(f'The area of the brick is: {area}')
print(f'The volume of the brick is: {volume}')