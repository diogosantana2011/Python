## The next line sets my_list to a list of the input data 
my_list = list(map(int, input('Enter a for a list, in format \',Number,\': \n').split(','))) 

## The input value 
# my_list = [1, 2, 3, 4] 

# first_plus_last = [my_list[0] + my_list[-1]]

for i in my_list:
    first_plus_last = my_list[0] + my_list[-1]
    
print(first_plus_last)