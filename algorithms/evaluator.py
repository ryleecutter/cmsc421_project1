import seaborn as sns
import pandas as pd
import numpy as np
import time
import sys
import pdb 
import os
    

def timer():
    realtime = time.time_ns()
    CPUtime = time.process_time_ns()
    return realtime, CPUtime

def times(matrix, func, iterations):
    r, c = timer()
    medcost = []
    for i in range(iterations):
        path, cost, expanded = func(matrix)
        medcost.append(cost)
    re, ce = timer()

    return abs(r-re)/iterations , abs(c-ce)/iterations, path, np.median(medcost), expanded

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
    avgreal, avgcpu, path, medcost, expanded = times(matrix, func ,iterations)
    print(f"\niterations: {iterations}")
    print(f"average cost: {medcost}\n(last) path: {path}")
    print(f"clock time: {avgreal * .001} \ncpu time: {avgcpu * .001}\n") #nanoseconds -> microseconds
    return {
        "n": len(path)-1, #rows
        "avg_real": avgreal,
        "avg_cpu": avgcpu,
        "med_cost": medcost,
        "matrix": matrix,
        "expanded nodes": expanded,
    }

def printer(algo,start,stop,step):
     for i in range(start,stop+1,step):
            for j in range(0,10):
                matrix = f"matrices/{i}_random_adj_mat_{j}.txt"
                iterations = 1#how many times to run the algo on this matrix. 
                
                
                row_df = pd.DataFrame()
                result = runthis(matrix, algo, iterations)
                row_df = pd.concat([row_df, pd.DataFrame([result])], ignore_index=True)
    
                row_df.to_csv(f"{algo}resultsexpanded.csv", mode="a", header= not os.path.exists(f"{algo}resultsexpanded.csv"))

def main():
    algo = sys.argv[1] # should go: python evaluator.py algo matrix
    #0_random -> 10_random changes by 1 
    printer(algo, 5, 10, 1)
    #15_random -> 30_random changes by 5 
    printer(algo, 15, 30, 5)
    #40_random -> 50_random changes by 10
    #printer(algo,30,50,10)


if __name__ == "__main__":
    main()