# Problem: Produce a list that contains 
## points for each academic grade/ find GPA

# Input: a list of grades, postive whole numbers
student_results = ['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
# Test result (expectation): [1, 4, 3, 3, 2, 1, 3, 0, 3, 2, 2]
# Borderline input: ['W', 'F', 'F', 'F', 'W', 'F', 'F', 'F', 'W', 'F', 'W', 'F', 'F'] 
# Test result (expectation): [0, 0, 0, 0, 0, 0, 0, 0, 0]

# Output: a list of grades
## transformed to their respective grade value 
student_gpa = []

for grade in student_results:
    if grade == 'A': 
        student_gpa = student_gpa + [4]
    elif grade == 'B':
         student_gpa = student_gpa + [3]
    elif grade == 'C':
        student_gpa = student_gpa + [2]
    elif grade == 'D':
        student_gpa = student_gpa + [1]
    elif grade == 'F':
        student_gpa = student_gpa + [0]
        
print('From', student_results, 'the corresponding GPA is: ', student_gpa)