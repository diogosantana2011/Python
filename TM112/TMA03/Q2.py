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

# *** Modify the body of the show_flashcard function so that it
# implements yout algorithm from part i. Also modify the docstring
# for the program and the docstring for the function, to take 
# account of the changes and their effect. ***

def show_flashcard():
    """ Show the user a random key and ask them
        to define it. Show the definition
        when the user presses return.    
    """
    random_key = choice(list(glossary))
    print('Define: ', random_key)
    input('Press return to see the definition')
    print(glossary[random_key])

# Set up the glossary
glossary = {'word1':'definition1',
            'word2':'definition2',
            'word3':'definition3'}


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