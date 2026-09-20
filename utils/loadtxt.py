import sys
#given text file, parse inputs by space, and rows by \n using graph

def load(path): #take in the file path from command line.
    matrix = [] 
    with open(path) as file: #call open on the file path to access the matrix.
        for line in file: #for each line in the file, thats one row.
            row = [float(x) for x in line.split()] #we have a line, but its string. so make row = an array of split string that float(x) converts into float.
            matrix.append(row) #makes ND array appending each. 
    return matrix #returns a usable matrix.
            