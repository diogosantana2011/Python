# Grading system
# marks var
marks = int(float(input('Please enter the students grade: ')))

if marks > 60 and marks < 80:
    grade = 'merit'
elif marks >= 40 and marks <= 60:
    grade = 'pass'
elif marks >= 80:
    grade = 'merit'
else:
    grade = 'fail'
    
print(f'Your grade is {grade}')