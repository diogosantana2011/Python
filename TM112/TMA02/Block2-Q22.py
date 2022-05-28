user_number = int(input('Please enter a whole number: '))

def add_one(integer): 
    return integer + 1

print(f'The number you have added ({user_number}) to 1, results in: ',  add_one(user_number))
# As per comment on funct.
# We can then call directly on funct.
# add_one(1)