# Problem: Calculate GPAS: Version 2
## calculate and print out 
### the GPA rounded to 2 decimal places

# Input: a list of grades, postive whole numbers
grade_marking = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
student_results = ['D', 'A', 'B', 'B', 'C', 'D', 'B', 'F', 'W', 'B', 'W', 'C', 'C']
student_grades = []
gpa = 0

total = 0
for number in student_grades:
    total = total + number

length = 0
for item in student_grades:
    length = length + 1
    
while length:
    result = grade_marking[student_grades] * total
    gpa += result

print('GPA is: ', round(gpa, 2))
    