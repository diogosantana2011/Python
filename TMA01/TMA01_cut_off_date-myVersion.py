 # Input: day of birthday as an integer from 1 to 31

# Input: month of birthday as an integer from 1 to 12

# Input: year of birthday as an integer from 1922 to 2010
day = int(input('Enter the day of your birth: '))
day_range = 1, 31

month = int(input('Enter the month of your birth: '))
month_range = 1, 12

year = int(input('Enter the year of your birth: '))
year_range = 1922, 2021

if day not in range(1, 32):
    print(f'Please enter a day in the range of {day_range}')
elif month not in range(1, 13):
    print(f'Please enter a month in the range of {month_range}')
elif year not in range(1922, 2021):
    print(f'Please enter a year in the range of {year_range}')
else:
    # Calculate age based only on year
    age = 2022 - year

    # Adjust for month

    if month > 5 :
        age = age - 1
    if month == 5 and day <= 5:
        age = age - 1
    print('On 5 May 2022 I am age' , age , 'years old')
    

