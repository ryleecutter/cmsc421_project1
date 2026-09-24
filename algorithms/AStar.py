import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "aima"))
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree as mst 
import sys
import utils
from HC import cost


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
        
    def __str__(self):
        return f"current: {self.current} \n visited: {self.visited} \n g cost: {self.g} \n h cost: {self.h} \n f cost: {self.f} \n parent: {self.parent.current if self.parent is not None else 'none'} \n starting city: {self.start} \n n = {self.n}"
    __repr__ = __str__
    #define a heuristic cost. 
    def heuristic(self, matrix):
        unvisited = self.unvisited()
        if len(unvisited) == 0:
            self.h = matrix[self.current][self.start]
        else:
            l = list(unvisited)
            mst_cost = self.sumMST(mst(matrix[np.ix_(l, l)]))
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
    path.reverse()
    path.append(state.start)
    return path


def main():
    #import pdb; pdb.set_trace()
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
    while fringe:
        partialstate = fringe.pop()   
        #check goal
        if len(partialstate.visited) == n:
            best_path = path(matrix, partialstate)
            print(f"best cost: {cost(matrix,best_path)}")
            print(f"best path: {best_path}")
            return best_path #returns the path of the traversal
        #generate successors
        for x in partialstate.unvisited():
            y = State(current=x, visited=partialstate.visited | {x}, 
                    g= partialstate.g + matrix[partialstate.current][x], 
                    n=n, 
                    parent=partialstate, start=partialstate.start, h=-1)
            y.heuristic(matrix)
            y.fx()
            fringe.append(y)
        





if __name__ == "__main__":
    main()