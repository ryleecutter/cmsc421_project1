import numpy as np
import sys 

import NN 

matrix = np.loadtxt(sys.argv[1])
path, cost = NN(matrix)

distance = lambda city1, city2: matrix[city1][city2] #gives edge cost from one city to another

def twoOpt(oldRoute1, oldRoute2): #oldRoute1, oldRoute2 are tuples (city1, city2). 
    cost1 = distance(oldRoute1[0],oldRoute1[1])
    cost2 = distance(oldRoute2[0],oldRoute2[1])
    #need to consider oldRoute1[0] -> oldRoute2[0] and oldRoute1[1] -> oldRoute2[1]
    # is asking: is going from city1 -> city3, city2->city4 better than original? if so will need to reverse all intermediate cities.   
    newCost1 = distance(oldRoute1[0], oldRoute2[0])
    newCost2 = distance(oldRoute1[1],oldRoute2[1])
    
    timeDelta = newCost1 + newCost2 - (cost1 + cost2) 
    #return new cost so that the modifier can change or not change. 
    return timeDelta
    
def modifier(path, cost):
    3
    #takes the path and 