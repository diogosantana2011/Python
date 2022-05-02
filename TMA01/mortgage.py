# Mortgage

# Input: Anual interest, a float %
rate = 0.5

# Input: Monthly payment, a positive integer, based on currency
payment = 200

# Input/Output: Mortgage, a positive number, same currency
mortgage = 1000

print('Outstading mortgage: ', mortgage)

# Below causes -inf
# while (not mortgage == 0 or mortgage < 0):
#     interest = mortgage * rate /12
#     mortgage = mortgage + interest - payment
#     print(f'Outstanding mortgage: {mortgage}')

# Why?

# Above loop iterates over 
# mortgage and while it is not 0
# So iteration will go on even until it 
# becomes negative. Once negative, it 
# will remain negative as the interest is negative, 
# and payment will continue to decrease