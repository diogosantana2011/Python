import numpy as np

def correlation(x, y):
    corr = print(np.corrcoef(x, y))
    return corr

correlation(
    [78.9, 75.8, 77.3, 74.2, 78.1, 72.8, 77.6, 77.9],
    [56.7, 53.1, 56.1, 55.9, 54.1, 48.6, 59.4, 54.0]
)

# OR
# list1 = [78.9, 75.8, 77.3, 74.2, 78.1, 72.8, 77.6, 77.9]
# list2 = [56.7, 53.1, 56.1, 55.9, 54.1, 48.6, 59.4, 54.0]

# corr = np.corrcoef(list1, list2)
# print(corr)