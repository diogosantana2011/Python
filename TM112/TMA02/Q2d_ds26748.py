# Problem: Calculate GPAS: Version 2
## calculate and print out 
### the GPA rounded to 2 decimal places

# Input: a list of grades, postive whole numbers
student_results = ['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
student_grades = []

for result in student_results:
    # Calculate Grade
    if result == 'A': 
        student_grades = student_grades + [4]
    elif result == 'B':
         student_grades = student_grades + [3]
    elif result == 'C':
        student_grades = student_grades + [2]
    elif result == 'D':
        student_grades = student_grades + [1]
    elif result == 'F':
        student_grades = student_grades + [0]
    
    # Calculate GPA: 
    for grade in student_grades:
        total = 0
        for number in student_grades:
            total = total + number

        length = 0
        for item in student_grades:

            length = length + 1
        gpa = total / length 

# print(student_grades)
# print(student_results)
# print(total)
# print(length)
print('GPA is: ', round(gpa, 2))
    