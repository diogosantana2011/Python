# Problem: Calculate GPAS: Version 2
## calculate and print out 
### the GPA rounded to 2 decimal places

# Input: a list of grades, postive whole numbers
# grade_marking = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
# # student_results = ['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
grades = ['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
grade_marking = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
# points = 0
# length = len(grades)
student_grades = []
points = 0 

for grade in grades:
    while 'W' in grades:
        grades.remove('W')
        print(grades)
    if grades != []:
        points += grade_marking[grade]
    gpa = points / len(grades)
        
print('GPA is: ', round(gpa, 2))