hour = int(input('Please enter the hour value:\n'))

if hour in range(0,12):
    string = 'am'
elif hour == 12:
    hour = '12'
    string = 'pm - midday'
elif hour == 24:
    hour = '12'
    string = 'am - midnight'
elif hour in range(12, 24):
    hour = hour-12
    string = 'pm'
    
print(f'The hour entered is: {hour} {string}')
