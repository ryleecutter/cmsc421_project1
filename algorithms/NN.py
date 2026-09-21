import numpy as np
import sys 

matrix = np.loadtxt(sys.argv[1])

def NN(matrix):
    n = matrix.shape[0]
    start = np.random.randint(0,n) #uniform dist. random int from 0 -> n-1 (all n)

    visited = {start} #O(1) lookup with dict
    path = [start] #0->n-1->0 path
    cost = 0 
    current = start

    #need to find the minimum neighbor to add to list and cost and path
    #anon function that takes in the row and returns the 
    minneighbor = lambda row, visited: min((row[i], i) for i in range(len(row)) if i not in visited)

    #need to loop over until path is same size as matrix rows.
    while len(path) < n:
        dist, next = minneighbor(matrix[current], visited)
        
        cost = cost + dist #calc cost
        path.append(next) #add to next city to path
        current = next #update city
        visited.add(current) #add to visited.

    cost = cost + matrix[current][start] #need to add cost from last node to start again. 
    path.append(start) #add start back to end of array path. 

    print(f"path: {path}")
    print(f"cost: {cost}")
    

NN(matrix)

       
       
       



