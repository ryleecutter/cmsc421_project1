import seaborn as sns
import pandas as pd
import numpy as np
import time
import sys



def timer():
    realtime = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    CPUtime = time.clock_gettime_ns(time.CLOCK_PROCESS_CPUTIME_ID)
    return realtime, CPUtime




def main():
    algo = np.loadtxt(sys.argv[1]) # should go: python evaluator.py algo matrix
    
    match algo:
        case "Astar":
            ...
        case "GA":
            ...
        case "HC":
            ...
        case "NN":
            ...
        case "NN2O":
            ...
        case "RRNN":
            ...
        case "SimAn":
            ...
        case _:
            "error match case"




if __name__ == "__main__":
    main()