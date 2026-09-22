import numpy as np 
import sys 
import random 
from HC import randomTour, swap, cost
import math

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
            edgemap[p2[j+1]].add(-p2[j])
            edgemap[p2[j]].remove(p2[j+1])
            edgemap[p2[j]].add(-p2[j+1])
        else:
            edgemap[p2[j]].add(p2[j+1])
            edgemap[p2[j+1]].add(p2[j])  
    
    return edgemap

#needs to go through every index in edge_map and remove current city. should be fast with set. O(n)
def removeCity(edge_map, current_city):
    for x in edge_map:
        x.discard(current_city)
        x.discard(-current_city)
    


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
    fewest = [0]
    for i in range(n):
        if len(edge_map[i]) == len(edge_map[fewest[0]]) and i not in child: #they are same amnt of edges so add to fewest list.
            fewest.append(i) 
        else: 
            if len(edge_map[i]) < len(edge_map[fewest[0]]) and i not in child: #found city with less edges, reset fewest list, add new city
                fewest = [i]
    return np.random.choice(fewest) if len(fewest) > 1 else fewest[0]

#returns the city with the fewest connected edges in current_city's set.
def fewestCurrent(edge_map, current_city):
    currset = edge_map[current_city]
    if len(currset) == 0:
        return -1
    priority_cities = [c for c in currset if c < 0]
    
    if priority_cities:
        next_city = min(priority_cities, key=lambda c: len(edge_map[abs(c)])) #negative vlaues so only look for smallest edge with those. 
    else:
        next_city = min(currset, key=lambda c: len(edge_map[abs(c)])) #no priorties so we check these normally. and find smallest amnt of edges.        
    return next_city
        

#returns each generation. so that main can run simAn on many gens. 
def GA(matrix, n, pop_size, mut_chance, population):
    
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
        if current_city == -1:
            current_city = fewestEdges(edge_map, n, child)
        child.append(current_city) 
        removeCity(edge_map, current_city)
    child.append(child[0])
    
    #mutate child w/ prob mut_chance
    ...
    return child
         
    
def combineGenerations(population, children):
    ...

def main():
    
    matrix = np.loadtxt(sys.argv[1])
    n = matrix.shape[0] #amnt of row
    
    ##### HYPERPARAMETERS #####
    mut_chance = 0 #the prob of mutating a child after creation
    pop_size = 0  #the amount of possible parents for next generation
    gen_num = 0 #how many full generations
    children_gen = 0 #how many chilren per generation
     ########################
    children = [] #list of children to be combined with pop after each gen. 
    
    
    population = getPopulation(matrix, pop_size, n) #initial random population. 
     #creates population of random traversals, parents.
    for j in range(gen_num):#this many generations
        
        for i in range(children_gen): #make this many children per generation
            children.append(GA(matrix, n, pop_size, mut_chance, population))
        
        population = combineGenerations(population, children)
    



if __name__ == "__main__":
    main()
