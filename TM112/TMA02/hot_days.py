daily_temperatures = []
# Smallest input - empty list: []
# smallest output - No hot days: 31,33 
# largest output - All days are hot: 28, 33, 29, 32, 27
# borderline temperatures: 25, 24, 22
# original input: 28, 30, 31, 30, 31, 32
hot_days = []

for temperature in daily_temperatures:
    if temperature > 30: 
        hot_days = hot_days + [temperature]
print('The hot days had temperatures: ', hot_days)