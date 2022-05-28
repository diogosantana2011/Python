# user_input = str(input('Please enter True/False: '))

# def truth_value(user_input):
#     # If value is True, results in 1
#     # If value is False, results in 0
#     if user_input == 'True' or user_input == 'true':
#         truth_value = 1
#     elif user_input == 'False' or user_input == 'false':
#         truth_value = 0
#     return truth_value

# print(f'The value you have entered ({user_input}) is: ', truth_value(user_input))

# TEST

def integer_0_or_1(user_input):
    """Convert an integer into a truth value."""
    # If value is True, results in 1
    # If value is False, results in 0
    if user_input == True:
        truth_value = 1
    elif user_input == False:
        truth_value = 0
    return truth_value
           
print(integer_0_or_1(True))