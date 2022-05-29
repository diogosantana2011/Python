celsius_values = [-20, -10]
farenheit_values = []

# Tests
# smallest input - empty input: []
# negative, 0, positive inputs: -1, 0, 1
# negative, positive output: -20, -10

for celsius in celsius_values:
    # Conversion from °C to °F ((°C * 1.8) + 32)
    farenheit = celsius * 1.8 + 32
    farenheit_values = farenheit_values + [farenheit]
    
print('The temperatures in Farenheit are: ', farenheit_values)