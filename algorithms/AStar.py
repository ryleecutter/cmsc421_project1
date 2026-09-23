import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree as mst 
import sys
import random
from HC import cost
from functools import partial
from aima import utils


#each state is represented by a node with: 
#   current_state
#   start_state
#   g(n) cost
#   #h(n) cost
#   f(n) cost
#   
class State:
    def __init__(self, current:int, visited, g, h, n : int, parent=None, start=None):
        self.current = current
        self.visited = visited
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        self.start = start
        self.n = n
    #define a heuristic cost. 
    def heuristic(self, matrix):
        if len(unvisited) == 0:
            self.h = matrix[self.current][self.start]
        else:
            unvisited = self.unvisited()
            mst_cost = self.sumMST(mst(matrix[np.ix_(unvisited, unvisited)]))
            h1 = minDist(matrix, self.current, unvisited)
            h2 = minDist(matrix, self.start, unvisited)
            self.h = mst_cost + h1 + h2
            self.f = self.g + self.h
    #returns the sum of the best mst.
    def sumMST(self, sparse):
        return np.sum(sparse.toarray())
    #inits the evaluation value
    def fx(self):
        self.f = self.g + self.h
    def unvisited(self):
       return set(range(self.n)) - self.visited

#returns min dist from a city to some city in unvisited
def minDist(matrix, city, unvisited):
    return min(matrix[city][x] for x in unvisited)

def path(matrix, state):
    path = []
    while state.parent != None:
        path.append(state.current)
        state = state.parent
    path.append(state.current)
    return path.reverse()

def main():
    matrix = np.loadtxt(sys.argv[1])
    n = matrix.shape[0] # num rows
        
    
    fringe = utils.PriorityQueue('min', f = lambda state: state.f) #sorts based on f 

    #need the initial cities.
    for i in range(n):
       x = State(current=i, visited={i}, g=0, h=0, n=n, parent=None, start=i)
       x.heuristic(matrix)
       x.fx()
       fringe.append(x)

    #pop from fringe
    partialstate = fringe.pop    
    #check goal
    if len(partialstate.visited) == n:
        return path(matrix, partialstate) #returns the path of the traversal
    #generate successors
    for x in partialstate.unvisited():
         y = State(current=x, visited=partialstate.visited()+set(x), 
                   g= partialstate.g + minDist(matrix,x,partialstate.unvisited() | {x}), 
                   n=n, 
                   parent=partialstate.current, start=partialstate.start)
         y.heuristic(matrix)
         y.fx()
         fringe.append(y)




if "__name__" == "__main__":
    main()