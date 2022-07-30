"""
Echo program.
"""

print('See your input repeated, until you type `quit` or `stop`.')

exit = False
while not exit:
    user_input = input('Type your input here: ')
    if user_input == 'quit' or user_input == 'stop':
        exit = True
    else:
        print(user_input)
    