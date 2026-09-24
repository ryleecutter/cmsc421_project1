import seaborn as sns
import pandas as pd
import numpy as np
import time
import sys



def timer():
    realtime = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    CPUtime = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
    return realtime, CPUtime

def times(matrix, func, times):
    real =[]
    cpu = []
    for i in range(times):
        r, c = timer()
        path, cost = func(matrix)
        re, ce = timer()
        real.append(abs(r-re))
        cpu.append(abs(c-ce))
    return sum(real)/times , sum(cpu)/times

#runs the matrix and calculates the times/stores the data in a dataframe.
#times = number of runs. useful if cpu time = 0
def runthis(matrix, algo, times):
    match algo:
            case "Astar":
                from AStar import run_astar
                func = run_astar
                avgreal, avgcpu = times(matrix,func,times)
            case "GA":
                from GA import run_GA 
                func = run_GA
                avgreal, avgcpu = times(matrix,func,times)
            case "HC":
                from HC import run_HC
                func = run_HC
                avgreal, avgcpu = times(matrix,func,times)
            case "NN":
                from NN import NN
                func = NN
                avgreal, avgcpu = times(matrix,func,times)
            case "NN2Opt":
                from NN2Opt import run_NN2Opt
                func = run_NN2Opt
                avgreal, avgcpu = times(matrix,func,times)
            case "RRNN":
                from RRNN import run_RRNN
                func = run_RRNN
                avgreal, avgcpu = times(matrix,func,times)
            case "SimAn":
                from SimAn import run_SimAn
                func = run_astar
                avgreal, avgcpu = times(matrix,func,times)
            case _:
                "error match case"


def main():
    algo = sys.argv[1] # should go: python evaluator.py algo matrix
    matrix = sys.argv[2]
    




if __name__ == "__main__":
    main()