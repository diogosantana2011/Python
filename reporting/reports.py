"""
    Script to create some type of 
    graph with data outputed from Performance test
    on Jmeter.
"""

# importing the required module
import csv
import matplotlib.pyplot as plt

# Read file
file = open('audit_results.csv')
csv_reader = csv.reader(file)

# Get file headers
header = []
header = next(csv_reader)

# Get file rows
rows = []
for row in csv_reader:
    rows.append(row)
print(header)
print(rows)

# Ideally it should create some type of line graph. 
# Headers: ['timeStamp', 'elapsed', 'label', 'responseCode', 'responseMessage', 'threadName', 'dataType', 'success', 'failureMessage', 'bytes', 'sentBytes', 'grpThreads', 'allThreads', 'URL', 'Latency', 'IdleTime', 'Connect']
# [WIP]