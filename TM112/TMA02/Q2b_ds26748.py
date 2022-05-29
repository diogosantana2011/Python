# Problem: calculate and 
## print out the GPA rounded to 2 decimal places

# Input: a list of of whole positive numbers 
student_results = ['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
## in the range of (0, n+1) where n is 4
student_grades = []

for grade in student_results:
    if grade == 'A': 
        student_grades = student_grades + [4]
    elif grade == 'B':
         student_grades = student_grades + [3]
    elif grade == 'C':
        student_grades = student_grades + [2]
    elif grade == 'D':
        student_grades = student_grades + [1]
    elif grade == 'F':
        student_grades = student_grades + [0]

# Sub-problem: compute sum of a list of ints    
length = 0
for item in student_grades:
    length = length + 1

# DEBUG
# Should = 12 if student_results = ['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
# print(length)

# Sub-problem: compute the sum of the grades
total = 0
for number in student_grades:
    total = total + number
# DEBUG
# Should = 12 if student_results = ['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
# print(length)

# OUTPUT: compute mean of student_gpa   
student_gpa = total / length
print(f'''
    The student results were: {student_results}
    These resulted in grades: {student_grades}  
    Which resulted in GPA: {round(student_gpa, 2)}
    ''')