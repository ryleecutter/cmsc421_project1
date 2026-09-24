import numpy as np
import sys 
import time
import NN 




def twoOpt(matrix, path, i, j):

    cost1 = matrix[path[i]][path[i+1]] #old edges
    cost2 = matrix[path[j]][path[j+1]] 

    
    newCost1 = matrix[path[i]][path[j]]#new edges
    newCost2 = matrix[path[i+1]][path[j+1]]

    return newCost1 + newCost2 - (cost1 + cost2)

    
    
#takes the path and total current cost. 
def improve(path, matrix):
    n=len(path)
    #need to loop through every possible edge pairing to find a possible edge swap pairing.
    #but needs to stop when there is no imporvement. so needs boolean? 
    improvement = True
    while improvement:
        improvement = False
        for i in range(1, n-3): 
            for j in range(i+2, n-1): # last city ( connects back to first city )
                timeDelta = twoOpt(matrix,path,i,j)
                if timeDelta < 0:
                    #new edges are less. reverse intermediary nodes.
                   path[i+1:j+1] = path[i+1:j+1][::-1]
                   improvement = True
    return path

def run_NN2Opt(matrix):
    
    if isinstance(matrix, str):
            matrix = np.loadtxt(matrix)
    #if len(sys.argv) > 2:
     #   print("wrong inputs: python NN2Opt.py matrix.txt")
     #   sys.exit(1)
    
    
    path, cost = NN.run_nn(matrix)
    newPath = improve(path,matrix)
    newCost = sum(matrix[newPath[i]][newPath[i+1]] for i in range(len(newPath)-1))
    return newPath, newCost
    


if __name__ == "__main__":
    matrix = np.loadtxt(sys.argv[1])
    # Real time (wall clock)
    start_real = time.time_ns()

    # CPU time (process CPU)
    start_cpu = time.process_time_ns()

    
    path, cost = run_NN2Opt(matrix)

    end_real = time.time_ns()
    end_cpu  = time.process_time_ns()

    print("cost:", cost)
    print("path:", path)
    print("Real time (ns):", end_real - start_real)
    print("CPU time (ns):", end_cpu - start_cpu)

       
       


