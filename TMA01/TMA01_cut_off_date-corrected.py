# Problem: Check how old you are on 5 May 2022

# Input: day of birthday as an integer from 1 to 31

# Input: month of birthday as an integer from 1 to 12

# Input: year of birthday as an integer from 1922 to 2010

# day = 5
# month = 9
year = 1998

day = int(input('Enter the day of your birth: '))
month = int(input('Enter the month of your birth: '))

# Calculate age based only on year

age = 2022 - year

# Adjust for month
if month > 5:
    age = age -1

elif month == 5 and day > 5:
    age = age - 1
    
print('On 5 May 2022 I am age' , age , 'years old')