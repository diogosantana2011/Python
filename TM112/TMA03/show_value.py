# Do not change the following line
test_dictionary = { 
    1:'a', 
    2:'b', 
    3:'c', 
    4:'d'} 

# Enter your function (and nothing else) below this line

def show_value(key, dictionary):
    """
    Will print definition of key passed as param,
    or state key is invalid and not in dict.
    """
    if key not in dictionary:
        print(str(key) + ' is not a valid key.')
    else:
        print('The defenition for key ' + str(key) + ' is', dictionary.get(key))
        
show_value(1, test_dictionary)
show_value(5, test_dictionary)
show_value(3, test_dictionary)
show_value(25, test_dictionary)