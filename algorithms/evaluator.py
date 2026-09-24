import seaborn as sns
import pandas as pd
import numpy as np
import time
import sys
import pdb 

#need to save data from each size matrix into the same dataframe, should be 10 inputs (_,_,_) for each size n 
#this way i can get the true median of the data size for cpu, real, cost
def saveData():
    #for each run save as (med cost, avg cpu, avg real)
    
    ...

def timer():
    realtime = time.time_ns()
    CPUtime = time.process_time_ns()
    return realtime, CPUtime

def times(matrix, func, iterations):
    r, c = timer()
    medcost = []
    for i in range(iterations):
        path, cost = func(matrix)
        medcost.append(cost)
    re, ce = timer()
    
    return r-re/iterations , c-ce/iterations, path, medcost[len(medcost)//2]

#runs the matrix and calculates the times/stores the data in a dataframe.
#times = number of runs. useful if cpu time = 0
def runthis(matrix, algo, iterations):
    match algo:
            case "AStar":
                from AStar import run_astar
                func = run_astar
            case "GA":
                from GA import run_GA 
                func = run_GA
            case "HC":
                from HC import run_HC
                func = run_HC 
            case "NN":
                from NN import run_nn
                func = run_nn
            case "NN2Opt":
                from NN2Opt import run_NN2Opt
                func = run_NN2Opt 
            case "RRNN":
                from RRNN import run_RRNN
                func = run_RRNN 
            case "SimAn":
                from SimAn import run_SimAN
                func = run_SimAN    
            case _:
                "error match case"
  # 
    avgreal, avgcpu, path, cost = times(matrix, func ,iterations)
    print(f"\niterations: {iterations}")
    print(f"average cost: {cost}\n(last) path: {path}")
    print(f"clock time: {avgreal * .001} \ncpu time: {avgcpu * .001}\n") #nanoseconds -> microseconds
    return avgreal, avgcpu

def main():
    algo = sys.argv[1] # should go: python evaluator.py algo matrix
    matrix = sys.argv[2]
    iterations = 10 #how many times to run the algo on this matrix. 
    
    runthis(matrix, algo, iterations)




if __name__ == "__main__":
    main()