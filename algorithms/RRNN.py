import numpy as np 
import sys




def getPossible(matrix, current, k, visited):
    possible = [(matrix[current][j], j)
                       for j in range(len(matrix)) if j not in visited] #returns every possible index in current row, where the city isnt already used.
    
    possible.sort(key = lambda city: city[0]) #just using city cost, as matrix[current][j] returns edge cost.

    return possible[::k] #returns up until k, sorted from min -> k min

#returns some traversal and cost
def RRNN(matrix, k, n): 
    start = np.random.randint(n) #random start
    visited = {start} #lookup
    path = [start] #real path
    
     
    

def main():
    #define k and num_repeats
    
    ###########        Hyperparameters      ##########
    k = 1
    num_repeats = 5
    ###########                             ##########
    
    
    matrix = np.loadtxt(sys.argv[1]) #receive matrix
    
    n = matrix.shape[0] #get length of row
    
    best_path = [] #storage for actual best path.
    best_cost = 99999999999999 #some arbitrary val
    
    for i in range(0, num_repeats): #repeats RRNN num_repeats times. 
        path, cost = RRNN(matrix, k, n) #current traversal, cost
        if cost < best_cost:
            best_path = path #update based on total cost.
            best_cost = cost
    #found the best path given k and num_repeats w/ different random starting node.
    print(f"best path: {best_path}")
    print(f"best cost: {best_cost}")
        
        
        
    
    
    
    



if __name__ == "__main__":
    main()



