import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "aima")) # wont run the code. nice
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree as mst 
import sys
import utils
from HC import cost
import time
#each state is represented by a node with: 
#   current_state
#   start_state
#   g(n) cost
#   #h(n) cost
#   f(n) cost
#   


class State:
    memoize = {}
    def __init__(self, current:int, visited, g, h, n : int, parent=None, start=None):
        self.current = current
        self.visited = visited
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        self.start = start
        self.n = n
        
    def __str__(self):
        return f"current: {self.current} \n visited: {self.visited} \n g cost: {self.g} \n h cost: {self.h} \n f cost: {self.f} \n parent: {self.parent.current if self.parent is not None else 'none'} \n starting city: {self.start} \n n = {self.n}"
    __repr__ = __str__
    
    #define a heuristic cost. 
    #what if i can memoize the heuristic values to avoid 
    # recomputing them for the same state because we only use the set anyway.
    # frozenset the set -> make constant for all? and that way everyone can access. as 
    def heuristic(self, matrix):
        unvisited = self.unvisited()
        if not unvisited: #have we visited all cities?
            self.h = matrix[self.current][self.start]
            self.f = self.g + self.h
            return
        #if we havent, then we can do the heuristic for the unvisited cities.
        #frozenset i think will come in clutch.
        key = frozenset(unvisited) #turns into an immutable object so we can use key
         #new state -> sets have no order, so checks all possibilities
        if key not in State.memoize:
            l = list(unvisited) #
            State.memoize[key] = self.sumMST(mst(matrix[np.ix_(l, l)])) #same as before just added to memoize now
        mst_cost = State.memoize[key]  #either way it is now in memoize. 
        self.h = mst_cost + minDist(matrix, self.current, unvisited) + minDist(matrix, self.start, unvisited)
        self.f = self.g + self.h 
        
            
    #returns the sum of the best mst.
    def sumMST(self, sparse):
         return np.sum(sparse.toarray())
    
    #inits the evaluation value
        
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
    path.reverse()
    path.append(state.start)
    return path


def run_astar(matrix):
    State.memoize.clear()
    expanded =0
    if isinstance(matrix, str):
        matrix = np.loadtxt(matrix)
    
    n = matrix.shape[0] # num rows
        
    
    fringe = utils.PriorityQueue('min', f = lambda state: state.f) #sorts based on f 

    #need the initial city. originally inits all bt changed becase symmetric.
    start = State(current=0, visited={0}, g=0, h=0, n=n, parent=None, start=0)
    start.heuristic(matrix)
    fringe.append(start)

    #pop from fringe
    while fringe:
        partialstate = fringe.pop()   
        #check goal
        if len(partialstate.visited) == n:
            best_path = path(matrix, partialstate)
            
            return best_path, cost(matrix, best_path), expanded #returns the path of the traversal
        #generate successors
        expanded += 1
        for x in partialstate.unvisited():
            y = State(current=x, visited=partialstate.visited | {x}, 
                    g= partialstate.g + matrix[partialstate.current][x], 
                    n=n, 
                    parent=partialstate, start=partialstate.start, h=-1)
            
            y.heuristic(matrix)
            fringe.append(y)
        





if __name__ == "__main__":
    matrix = np.loadtxt(sys.argv[1])
    # weal time 
    start_real = time.time_ns()

    # cpu time 
    start_cpu = time.process_time_ns()

    
    path, cost, it = run_astar(matrix)

    end_real = time.time_ns()
    end_cpu  = time.process_time_ns()

    print("cost:", cost)
    print("path:", path)
    print("Real time (ns):", end_real - start_real)
    print("CPU time (ns):", end_cpu - start_cpu)
