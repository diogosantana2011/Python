""" TM112 22D TMA02 Q5
"""

from tma02_stats import median
from tma02_stats import mean
from tma02_stats import corr_coef

""" You can use one of two approaches:
1)  add suitable code below and then run this file
2)  run this file first then do the calculation in the 
    Python interactive shell.
"""


# Estimated risk of infection following vaccination by single year of age, UK
# 1 December 2020 to 31 May 2021

# Office for National Statistics – Coronavirus (COVID-19) Infection Survey

#  Var: holds data about the years of age.
age  = [16, 17, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                      31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                      41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                      51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                      61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                      71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
        81, 82, 83, 84, 85]

# Var: Estimated risk of infection following vaccination
risk = [1.93, 1.88, 1.82, 1.77, 1.73, 1.68, 1.63, 1.59, 1.54, 1.5,
        1.46, 1.42, 1.38, 1.35, 1.31, 1.28, 1.25, 1.23, 1.2, 1.18,
        1.16, 1.15, 1.13, 1.12, 1.12, 1.11, 1.1, 1.1, 1.1, 1.1, 1.1,
        1.1, 1.11, 1.11, 1.11, 1.11, 1.11, 1.1, 1.1, 1.09, 1.07, 1.06,
        1.04, 1.02, 1, 0.98, 0.96, 0.94, 0.92, 0.91, 0.89, 0.88, 0.87,
        0.86, 0.85, 0.85, 0.84, 0.84, 0.83, 0.83, 0.82, 0.82, 0.81, 0.81,
        0.81, 0.8, 0.8, 0.79, 0.79, 0.79]

# DEBUG: 
# print(len(age))
# print(len(risk))

mean_age = mean(age)
print('The mean age is:', mean_age)

correlation = corr_coef(age, risk)
print('The correlation coeficient is:', correlation)
    

