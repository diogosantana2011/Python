temperatures = [-1, 1, 0, -1, 0, 1, -1]
days = 0

# Tests
# Minimum output: 1,0,1,1,0,1,1
# Maximum output: -1,-1,-1,-1,-1,-1,-1
# Middle output: -1, 1, 0, -1, 0, 1, -1
# original value: 4, -5, 3, 1, 0, 3, -2

for temperature in temperatures:
    if temperature < 0:
        days = days + 1
        
print('The temperature was below 0 for: ', days, 'days')