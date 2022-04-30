# Produce times table
size = int(input('Enter size you want: '))

for row in range (1, size+1):
    for column in range(1, size+1):
        print(row * column, end =' ')
    # Move to a new line
    print()