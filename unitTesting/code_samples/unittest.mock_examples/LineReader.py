import os

def readFromFile(file):
    if not os.path.exists(file):
        raise Exception("Bad File!")
    infile = open(file, 'r')
    line = infile.readline()
    return line