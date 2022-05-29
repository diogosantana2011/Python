# rate = 0.5

# payment = 200

# mortgage = 1000

rate = int(float(input('Please enter the value of your rate: ')))

payment = int(input('Please enter the value of your monthly payment: '))

mortgage = int(input('Please enter the value of your monthly mortage: '))

print('Outstanding Mortgage: ', mortgage) 

while not (mortgage == 0 or mortgage > 0):
    interest = mortgage * rate /12
    mortgage = mortgage + interest - payment
    print('Outstanding Mortgage: ', mortgage)


