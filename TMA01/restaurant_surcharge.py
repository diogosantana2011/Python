# Restaurant Surcharge

bill = int(input('Please enter the total for the bill: \'e.g 18.45\' '))
people = int(input('Please enter the total number of people: '))
charge = 0.1

if people < 6:
    total = bill
else: 
    total = bill + bill * charge
    
print('The total bill is', "{:.2f}".format(total))