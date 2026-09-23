import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree as mst 
import sys
import random
from HC import cost
from functools import partial
from aima import utils

#returns total weight of best mst
def sumMST(sparse):
    ...

#returns the min dist from state to some city in unvisited.
def minDist(matrix, unvisited, state):
    ...

def hn(matrix, state):
    # h(n) = mst(unvisited cities) + mindist(unvisited, start) + mindist(current, unvisited)
    # unvisited to start bcause it must connect at the end back to start. 
    # current to unvisited to connect the current sequence to the mst. 
    unvisited = state.unvisited #just storing cuz its used multiple times - lookup time
    
    return sumMST(mst(unvisited)) + minDist(matrix, unvisited, state.start) + minDist(matrix, unvisited, state.current)

def fn():
    ...

def memoize():
    ...

def main():
    matrix = np.loadtxt(sys.argv[1])
    n = matrix.shape[0] # num rows
    
    #create visited
    visited = set()
    h = hn(matrix, state)#takes matrix and state which is from the fringe: contains all info we need. 
    
    f = fn()
    f = memoize() #save msts so we dont have to recompute same states continuously. 
    fringe = utils.PriorityQueue('min', ...) # need to define f. 

    #lets first create our heuristic function. 
    




if "__name__" == "__main__":
    main()