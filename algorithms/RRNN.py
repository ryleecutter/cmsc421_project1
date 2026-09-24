import numpy as np 
import sys
import time



def getPossible(matrix, current, k, visited):
    possible = [(matrix[current][j], j)
                       for j in range(len(matrix)) if j not in visited] #returns every possible index in current row, where the city isnt already used.
    
    possible.sort(key = lambda city: city[0]) #just using city cost, as matrix[current][j] returns edge cost.

    return possible[:k] #returns up until k, sorted from min -> k min (cost, index)


#returns some traversal and cost
def RRNN(matrix, k, n): 
    start = np.random.randint(n-1) #random start
    visited = {start} #lookup
    path = [start] #real path
    total_cost = 0
    current = start
    #we have a function which returns the possible given the current node. 
    #need to go through until size(path) == len(matrix), then add final node to first node. 
    while len(path) < len(matrix):
        
        #find the possible values
        possible = getPossible(matrix, current, k, visited) #returns list.
        rand = np.random.randint(len(possible))
        current = possible[rand][1]
        total_cost += possible[rand][0] #finds the cost of that node from current current -> possible[rand]
        visited.add(current) #adds the node which is randomly selected from the k choices
        path.append(current) #adds to path
        
    #reconnect. 
    total_cost += matrix[current][start]
    path.append(start)
    return path, total_cost
    


def run_RRNN(matrix):
    #define k and num_repeats
    
    ###########        Hyperparameters      ##########
    k = 5
    num_repeats = 15
    ###########                             ##########
    
    
    n = matrix.shape[0] #get length of row
    
    best_path = [] #storage for actual best path.
    best_cost = 99999999999999 #some arbitrary val
    
    for i in range(0, num_repeats): #repeats RRNN num_repeats times. 
        path, cost = RRNN(matrix, k, n) #current traversal, cost
        if cost < best_cost:
            best_path = path #update based on total cost.
            best_cost = cost
    #found the best path given k and num_repeats w/ different random starting node.
    return best_path, best_cost
        
        
        
    
    
    
    


if __name__ == "__main__":
    matrix = np.loadtxt(sys.argv[1])
    # Real time (wall clock)
    start_real = time.time_ns()

    # CPU time (process CPU)
    start_cpu = time.process_time_ns()

    
    path, cost = run_RRNN(matrix)

    end_real = time.time_ns()
    end_cpu  = time.process_time_ns()

    print("cost:", cost)
    print("path:", path)
    print("Real time (ns):", end_real - start_real)
    print("CPU time (ns):", end_cpu - start_cpu)

       