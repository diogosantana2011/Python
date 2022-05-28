integer = int(input('Please enter a numeric value to evaluate to True/False: '))

def truth_value(integer):
    """Convert an integer into a truth value."""
    # Convert 0 into False and all other integers,
    # including 1, into True
    if integer != 0:
        truth_value = True
    else:
        truth_value = False
    return truth_value

print(f'The value you have entered ({integer}) is: ', truth_value(integer))