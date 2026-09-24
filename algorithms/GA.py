import numpy as np 
import sys 
import random 
from HC import randomTour, swap, cost
from functools import partial
import time

#returns a list of pop_size number random traversals
def getPopulation(matrix, pop_size, n):
    return [randomTour(matrix, n)[1] for _ in range(pop_size)]


#edgeMap will take in the two parents
#returns a map where the key is a city and the value is a set with 
#directly adjacent nodes in the parent traversals
#should note that the edges which are in both should be prioritized, somehow. 
#perhaps a value in the set which we check everytime 
#note: since using edgemap[p1[i]]... p1[i] will be a city, so then edgemap's indices will hold the cities in order. with 0 index with 1st city.
#if p1[0] = 4, then edgemp[4] = 4's adjacency list. so we can treat edgemap's index directly as the city.
def edgeMap(p1, p2, n):
    #need two structures;
    #direct neighbor list from both
    edgemap = [set() for _ in range(n)] #list with set, same indices as given in matrix
    for i in range(n-1):
        edgemap[p1[i]].add(p1[i+1]) #add edges to edge map. set doesnt allow duplicates so safe.
        edgemap[p1[i+1]].add(p1[i])
    #needs to first check if edgemap contains the edge already. if it does, update to negative city.
    for j in range (n-1):
        if p2[j] in edgemap[p2[j+1]]:
            edgemap[p2[j+1]].remove(p2[j])
            edgemap[p2[j+1]].add(-(p2[j]+1)) #holy testing cooked me. this so index 0 is fixed.
            edgemap[p2[j]].remove(p2[j+1])
            edgemap[p2[j]].add(-(p2[j+1]+1))
        else:
            edgemap[p2[j]].add(p2[j+1])
            edgemap[p2[j+1]].add(p2[j])  
    
    return edgemap


def decodeCity(c):
    return abs(c) - 1 if c < 0 else c   

#needs to go through every index in edge_map and remove current city. should be fast with set. O(n)
def removeCity(edge_map, current_city):
    
    edge_map[current_city].clear() #we can quickly look and see its empty because we dont want to go to it since its already visited.
    
    for x in edge_map:
        x.discard(current_city)
        x.discard(- (current_city+1))
        
    


def parents(population, pop_size):
    #select 2 random parents 
    r1 = random.randint(0, pop_size - 1)
    r2 = random.randint(0, pop_size - 1)
    while r1 == r2:
        r2 = random.randint(0, pop_size - 1)
    return population[r1], population[r2]

#takes the current map and amnt of items in list and then 
#finds option with fewest edges, if tied chooses randomly.
# refer to @fewestCurrent for within the set.
def fewestEdges(edge_map, n, child):
    available = [i for i in range(n) if i not in child]

    if not available:
        return -1

    fewest = [available[0]]
    for i in available[1:]:
        if len(edge_map[i]) == len(edge_map[fewest[0]]) and i not in child: #they are same amnt of edges so add to fewest list.
            fewest.append(i) 
        else: 
            if len(edge_map[i]) < len(edge_map[fewest[0]]) and i not in child: #found city with less edges, reset fewest list, add new city
                fewest = [i]
    return random.choice(fewest) if len(fewest) > 1 else fewest[0]



#returns the city with the fewest connected edges in current_city's set.
def fewestCurrent(edge_map, current_city):
    currset = edge_map[current_city]

    if not currset:
        return -1

    candidates = [c for c in currset if c < 0]

    if not candidates:
        candidates = list(currset)

    min_edges = min(len(edge_map[decodeCity(c)])
                    for c in candidates
                   )

    tied = [c for c in candidates if len(edge_map[decodeCity(c)]) == min_edges]

    return decodeCity(random.choice(tied)) 


def mutation(path):
    tpath = path.copy()
    n = len(tpath)
    validrange = range(1,n-1)
    i,j = random.sample(validrange,2) #when we have enough nodes to have non trivial swaps.
    tpath[i],tpath[j] = tpath[j],tpath[i]
    return tpath #new child

#returns each generation. so that main can run simAn on many gens. 
def GA(n, pop_size, mut_chance, population):
    
    p1,p2 = parents(population, pop_size) #get two parents
    edge_map = edgeMap(p1,p2, n) #if negative then its prioritized: common sequence in both parents
    child = []
    #need to create a child by using ER (enhanced with common edges)
    
    #choose the city with the fewest edges in the edgemap.
    current_city = fewestEdges(edge_map, n, child) #returns city w/ fewest edges
    #add to child[0], as it's the first city. 
    child.append(current_city)
    #remove all occurances of this parent from the edgemap 
    removeCity(edge_map, current_city)
    
    #start the loop for the rest of traversal. 
    for i in range(1, n): #start at 1 because we already found child's first element. 
        current_city = fewestCurrent(edge_map, current_city)
        if current_city == -1: #then select a random city, as there were no edges.
            current_city = fewestEdges(edge_map, n, child)
        child.append(current_city) 
        removeCity(edge_map, current_city)
    child.append(child[0])
    
    #mutate child w/ prob mut_chance
    if random.uniform(0,1) < mut_chance:
       return mutation(child)
    
    return [int(x) for x in child]

         
    


def combineGenerations(matrix,population, children):
    #combine the two then sort them and use half the length 
    #best fit is based on cost of traversal... 
    costfunc = partial(cost, matrix)
    sortedpop = sorted(population + children, key=costfunc) #has both lists sorted together.
    return sortedpop[:len(sortedpop)//2]



def run_GA(matrix):
    if isinstance(matrix, str):
            matrix = np.loadtxt(matrix)
    
    n = matrix.shape[0] #amnt of row
    
    ##### HYPERPARAMETERS #####
    mut_chance = .05 #the prob of mutating a child after creation
    pop_size = 35  #the amount of possible parents for next generation > 1
    gen_num = 100 #how many full generations
    children_gen = 67 #how many chilren per generation
     ########################
    children = [] #list of children to be combined with pop after each gen. 
    
    
    population = getPopulation(matrix, pop_size, n) #initial random population. 
     #creates population of random traversals, parents.
    for j in range(gen_num):#this many generations
        
        for i in range(children_gen): #make this many children per generation
            children.append(GA(n, pop_size, mut_chance, population))
        #after each generation, combine the best fitting. 
        population = combineGenerations(matrix, population, children)
    
    mcost = partial(cost, matrix)
    
    best = sorted(population, key = mcost)
    best_path = best[0]
    best_cost = cost(matrix,best_path)
    return best_path, best_cost
   



if __name__ == "__main__":
    matrix = np.loadtxt(sys.argv[1])
    # Real time (wall clock)
    start_real = time.time_ns()

    # CPU time (process CPU)
    start_cpu = time.process_time_ns()

    
    path, cost = run_GA(matrix)

    end_real = time.time_ns()
    end_cpu  = time.process_time_ns()

    print("cost:", cost)
    print("path:", path)
    print("Real time (ns):", end_real - start_real)
    print("CPU time (ns):", end_cpu - start_cpu)
