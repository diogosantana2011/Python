# Problem: Calculate GPAS: Version 2
## calculate and print out 
### the GPA rounded to 2 decimal places

# Input: a list of grades, postive whole numbers
grades = ['C', 'C', 'A', 'B', 'D', 'F', 'F', 'F', 'W', 'F', 'W', 'F', 'F']
grade_marking = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
points = 0 

for grade in grades:
    while 'W' in grades:
        grades.remove('W')
        print(grades)
    if grades != []:
        points += grade_marking[grade]
    gpa = points / len(grades)
        
print('GPA is: ', round(gpa, 2))