# Problem: calculate and 
## print out the GPA rounded to 2 decimal places

# Input: a list of of whole positive numbers 
student_results = ['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
#['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
# test: ['C', 'C', 'A', 'B', 'D', 'F', 'F', 'F', 'W', 'F', 'W', 'F', 'F']
## in the range of (0, n+1) where n is 4
student_grades = []

# Sub-problem: calculate grade based on 
## input from list
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

# Sub-problem: compute sum of a list of ints(student_grades)
## Average should not be taken from student_results, as it includes 'W' withdrawn
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
# Should = 24 if student_results = ['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
# print(total)

# OUTPUT: compute mean of student_gpa   
student_gpa = total / length
print('The student GPA was: ', round(student_gpa, 2))