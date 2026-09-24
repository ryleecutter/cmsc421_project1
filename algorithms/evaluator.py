import seaborn as sns
import pandas as pd
import numpy as np
import time
import sys
import pdb 


def timer():
    realtime = time.time_ns()
    CPUtime = time.process_time_ns()
    return realtime, CPUtime

def times(matrix, func, iterations):
    r, c = timer()
    avgcost = []
    for i in range(iterations):
        path, cost = func(matrix)
        avgcost.append(cost)
    re, ce = timer()
    import pdb; pdb.set_trace()
    return r-re/iterations , c-ce/iterations, path, sum(avgcost)/iterations

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
    iterations = 3 #how many times to run the algo on this matrix. 
    
    runthis(matrix, algo, iterations)




if __name__ == "__main__":
    main()