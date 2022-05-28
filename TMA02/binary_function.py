def truth_value(integer):
    """Convert an integer into a truth value."""
    # Convert 0 into False and all other integers,
    # including 1, into True
    if integer == 0:
        truth_value = False
    else:
        truth_value = True
    return truth_value

def integer_0_or_1(truth_value):
   """Convert a truth value into 0 or 1."""
   # Convert True into 1 and False
   # into 0
   if truth_value == True:
       integer = 1
   else:
       integer = 0

   return integer

def and_binary(A, B):
    """Convert given truth table into result."""
    if A != B or A & B == 0:
        return 0
    else:
        return 1

print('Test 1 results in: ', and_binary(0, 0))
print('Test 2 results in: ', and_binary(0, 1))
print('Test 3 results in: ', and_binary(1, 0))
print('Test 4 results in: ', and_binary(1, 1))