import numpy as np 
import sys
import random
from HC import randomTour, swap, cost
import math
import time

#takes in the matrix, the amount of cities, alpha : cooling rate, initial temperature, the max iterations
#returns the best (cost, path)
#fitness measure is the TOTAL TRAVERSAL COST.
def simA(matrix, n, alpha, temp, iters):
    
    cost, path = randomTour(matrix, n)#find a random traversal 
     
    #check if cost is better or if it is randomly selected to be the new path.
    
    for i in range(iters):
        newcost, newpath = swap(matrix, path)#find a neighboring solution, makes copy so doesnt change. 
        p = math.exp(-(newcost - cost) / temp)  #calc probability
        if newcost < cost or random.uniform(0,1) < p: #random.random returns 0 <= x <= 1 uniformly
            path = newpath
            cost = newcost  #update the best solution
            #calc new temp to lessen proabbility
            temp = alpha * temp
    return (cost,path)


def run_SimAN():
    matrix = np.loadtxt(sys.argv[1]) #input matrix
    n = matrix.shape[0] #find number of rows 
    
    #HYPERPARAMETERS
    alpha = .98  #0-1 , .9-.99 .9 is extremely fast, .95 is fast, .99 is slow.
    initTemp = 9 #5-20, 10 is better than 5.
    maxIters = 1300 #500+ is good.
    #################
    
    bestcost,bestpath = simA(matrix, n, alpha, initTemp, maxIters)
    return bestpath, bestcost

if __name__ == "__main__":
    # Real time (wall clock)
    start_real = time.time_ns()

    # CPU time (process CPU)
    start_cpu = time.process_time_ns()

    
    path, cost = run_SimAN()

    end_real = time.time_ns()
    end_cpu  = time.process_time_ns()

    print("cost:", cost)
    print("path:", path)
    print("Real time (ns):", end_real - start_real)
    print("CPU time (ns):", end_cpu - start_cpu)

       