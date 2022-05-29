# Problem: Compute grades for TMA Module with 4 TMAs

# Input: a list of 4 ints
marks = [100, 0, 100, 100]

# Tests
# Original value: 50, 60, 10, 0
# 3 or 4 TMAs with lowest marks: 0,0,0,0
# 3 TMAs, mean < 30: 30, 0, 29, 30
# 4 TMAs, mean of best is resit minimum: 30,30,29,30
# 3 TMAS, mean is resit if maximum: 39, 38, 40, 0
# 4 TMAS, 1 fail, 3 pass marks: 40, 20, 40, 40
# 3 TMAS, non-borderline case: 0, 55, 47, 67
# 3 TMAS, highest marks: 100, 0, 100, 100


## Sub-problem: Find lowest marks
lowest = marks[0]
for mark in marks: 
    if mark < lowest:
        lowest = mark

## Compute mean of best 3 marks
total = 0
for mark in marks: 
    total = total + mark
total = total - lowest
mean = total / 3

# DEBUG:
# print(mean) = should result in 40
# print(total) = should result in 120

### Compute grade for that mean
if mean < 30:
    grade = 'Fail'
elif mean < 40:
    grade = 'Resit'
else:
    grade = 'Pass'
print('The grade is: ', grade)