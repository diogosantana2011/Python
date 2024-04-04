"""
Echo program.
"""

print('See your input repeated, until you type `quit`, `exit` or `stop`.')

exit = False
while not exit:
    interrupt = ['quit', 'stop', 'exit']
    user_input = input('Type your input here: ')
    exit = True if user_input in interrupt else print(user_input)
    