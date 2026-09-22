import numpy as np
import sys 
import random 


# returns (cost: float, path: List)
def randomTour(matrix, n):
    #could do random start -> random node not in traversed ... -> back to start, calc cost.
    start = np.random.randint(n) #random int [0,n)
    current = start
    traversed = {current}
    path = [current]
    total_cost = 0
    #just gonna find all possible cities
    #then random over that k 
    possible = [j for j in range(n) if j not in traversed]
    
    while len(possible) > 0: 
        rand = np.random.randint(len(possible))
        #need to add to path 
        path.append(possible[rand])
        traversed.add(possible[rand])
        total_cost += matrix[current][possible[rand]]
        current = possible[rand]
        possible.remove(possible[rand])
        
    path.append(start)
    total_cost += matrix[current][start]
    return (total_cost, path)

def cost(matrix, path):
    sum=0
    for i in range(len(path)-2):
        sum += matrix[path[i]][path[i+1]]   
    return sum

#takes matrix, path.
#is called 
#returns the new cost and path. 
def swap(matrix, path):
    tpath = path.copy()
    n = len(tpath)
    validrange = range(1,n-1)
    i,j = random.sample(validrange,2) #when we have enough nodes to have non trivial swaps.
    tpath[i],tpath[j] = tpath[j],tpath[i]
    return (cost(matrix,tpath), tpath)
    
    
    
#returns the best (cost : float, path : List) 
def HC(matrix, n):
    #need to find the random tour to start our path
    current_cost, current_path = randomTour(matrix, n)
    #now that i have some solution, i need to select some i,j to swap
    improvement = True
    while improvement:
        improvement = False#perform swaps this many times     
        cost,path = swap(matrix, current_path)
        if cost < current_cost:
            improvement = True
            current_cost = cost
            current_path = path
        #now need to greedily select the best. 
    return (current_cost,current_path)
    
    
    
    
    

def main():
    
    #need hyperparameter for num restarts 
    num_restarts = 3
    
    
    #need to define a variable which is the best cost and best traversal
    best_cost = 9999999999  #arbitary cost
    best_path = []
    #need to read in matrix
    matrix = np.loadtxt(sys.argv[1])
    n = matrix.shape[0] # num of row
    #define how many times hillclimbing will run
    
    for i in range(num_restarts):
        it_cost, it_path = HC(matrix, n, num_swaps, improvement_ratio) #best path from this iteration
        if it_cost < best_cost:
            best_cost = it_cost
            best_path = it_path #new best path
    
    print(f"best cost: {best_cost}")
    print(f"best path: {best_path}")
        

if __name__ == "__main__":
    main()