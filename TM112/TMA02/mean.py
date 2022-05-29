# Problem: Find mean temperature

# Input
temperatures = [5, 0, -3, 7, 8, 5, 0]

# Sub-problem: compute sum of a list of numbers
total = 0
for temperature in temperatures:
    total = total + temperature

# Sub-problem: compute sum of a list of ints
length = 0
for temperature in temperatures:
    length = length + 1

# Output: mean, an int
mean = total / length
print('The mean of: ', temperatures ,'is', mean)    
