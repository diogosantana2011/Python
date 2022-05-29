# rate = 0.5

# payment = 200

# mortgage = 1000

rate = int(float(input('Please enter the value of your rate: ')))

payment = int(input('Please enter the value of your monthly payment: '))

mortgage = int(input('Please enter the value of your monthly mortage: '))
outstanding = []

outstanding = outstanding + [mortgage]
while mortgage > 0:
    interest = mortgage * rate /12
    mortgage = mortgage + interest - payment
    outstanding = outstanding + [mortgage]
    print('Outstanding Mortgage, Month by month: ', outstanding)


