import numpy as np
import sys 


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
    possible = [(j for j in range(n) if j not in traversed)][0]
    
    while possible.size() > 0: 
        rand = np.random.randint(possible.size())
        #need to add to path 
        path.append(rand)
        traversed.add(rand)
        total_cost += matrix[current][rand]
        current = rand
        possible.remove(current)
        
    path.append(start)
    total_cost += matrix[current][start]
    return (total_cost, path)

#takes matrix, path.
#returns the new cost and path. 
def swap(matrix, path):
    tpath = path
    n = len(tpath)
    if n < 4:
        print("must be >= 4")
        return 99999, path
    validrange = range(1,n-2)
    i,j = np.random.sample(validrange,2)
    #now have two random indices.
    #swap and then return with cost
    newCost1 = matrix[path[i]][path[j]]#new edges' cost
    newCost2 = matrix[path[i+1]][path[j+1]]
    
    tpath[i+1:j+1] = tpath[i+1:j+1][::-1] #new path with all intermediates swpaped.
    
    return (newCost1 + newCost2,tpath)
    
#returns the best (cost : float, path : List) 
def HC(matrix, n, num_swaps, improvement_ratio):
    #need to find the random tour to start our path
    current_cost, current_path = randomTour(matrix, n)
    #now that i have some solution, i need to select some i,j to swap
    for i in range(num_swaps): #perform swaps this many times     
        cost,path = swap(matrix, current_path)
        if cost/current_cost < improvement_ratio: 
            current_cost = cost
            current_path = path
    return (current_cost,current_path)
    
    
    
    

def main():
    
    #need hyperparameter for num restarts and number of swaps to try before no improvemnt
    num_restarts = 3
    num_swaps = 15
    improvement_ratio = .9975 #the amount in which the cost should be less than path, .95 = 5% less.
    
    
    #need to define a variable which is the best cost and best traversal
    best_path = (99999999, [])  #arbitary cost
    #need to read in matrix
    matrix = np.loadtxt(sys.argv[1])
    n = matrix.shape[0] # num of row
    #define how many times hillclimbing will run
    
    for i in range(num_restarts):
        it_cost, it_path = HC(matrix, n, num_swaps, improvement_ratio) #best path from this iteration
        if it_cost < best_path[0]:
            best_path[0] = it_cost
            best_path[1] = it_path #new best path
    
    print(f"best cost: {best_path[0]}")
    print(f"best path: {best_path[1]}")
        

if __name__ == "__main__":
    main()