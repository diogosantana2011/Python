# 22D TMA03 Q2

"""
This flashcard program allows the user to ask for a glossary entry.
In response, the program randomly picks an entry from all glossary
entries. It shows the entry. After the user presses return, the
program shows the definition of that particular entry.
The user can repeatedly ask for an entry and also
has the option to quit the program instead of seeing
another entry.
"""

from random import *
import csv

# *** Modify the body of the show_flashcard function so that it
# implements yout algorithm from part i. Also modify the docstring
# for the program and the docstring for the function, to take 
# account of the changes and their effect. ***

def show_flashcard():
    """ Show the user a random key/value and 
        when the user presses return; display its 
        respective key/value.        
    """
    # Random selection
    selection = randint(0, 10) 
    random_key = choice(list(glossary))
    random_value = glossary.get(random_key)
    
    if selection in range(0, 5):
        print('What is the definition for the entry - ', random_key)
        input('Press return to see the definition: ')
        print(glossary[random_key])
    else:
        print('What is the entry for the definition - ', random_value)
        input('Press return to see the entry: ')
        print(random_key)

# Set up the glossary

# glossary = {'word1':'definition1',
#             'word2':'definition2',
#             'word3':'definition3'}

def file_to_dictionary(filename):
    """
    Return a dictionary with contents of file
    """
    file = open(filename, 'r')
    reader = csv.reader(file)
    dictionary = {}
    
    for row in reader:
        dictionary[row[0]] = row[1]
    return dictionary

filename = 'TM112_Glossary.txt'
glossary = file_to_dictionary(filename)

# The interactive loop

exit = False
while not exit:
    user_input = input('Enter s to show a flashcard and q to quit: ')
    if user_input == 'q':
        exit = True
    elif user_input == 's':
        show_flashcard()
    else:
        print('You need to enter either q or s.')