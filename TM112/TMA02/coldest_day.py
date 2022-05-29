# Problem: find the lowest temperature of the week

# Input
temperatures = [5, 0, -3, 7, 8, 5, 0]

# Output
coldest = temperatures[0]
for temperature in temperatures:
    if temperature < coldest:
        coldest = temperature
        
print('The lowest of', temperatures, 'is', coldest)
