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
def edgeMap(matrix, p1, p2, n):
    #need two structures;
    #direct neighbor list from both
    edgemap = [set()] * n-1  #list with set, same indices as given in matrix
    for i in range(n-1):
        edgemap[p1[i]].add(p1[i+1]) #add edges to edge map. set doesnt allow duplicates so safe.
        edgemap[p1[i+1]].add(p1[i])
    #needs to first check if edgemap contains the edge already. if it does, update to negative city.
    for j in range (n-1):
        if p2[i] in edgemap[p2[i+1]]:
            edgemap[p2[i+1]].remove(p2[i]).add(-1 * p2[i])
            edgemap[p2[i]].remove(p2[i+1]).add(-1 * p2[i+1])
        else:
            edgemap[p2[i]].add(p2[i+1])
            edgemap[p2[i+1]].add(p2[i])  
    
    return edgemap

#needs to go through every index in edge_map and remove current city. should be fast with set. O(n)
def removeCity(edge_map, current_city):
    for x in edge_map:
        x.discard(current_city)
    


def parents(pop_size, population):
    #select 2 random parents 
    r1 = random.randint(0, pop_size - 1)
    r2 = random.randint(0, pop_size - 1)
    while r1 == r2:
        r2 = random.randint(0, pop_size - 1)
    return population[r1], population[r2]

#takes the current map and amnt of items in list and then 
#finds option with fewest edges, if tied chooses randomly.
#only works for the first city. refer to @____ for within the set.
def fewestEdges(edge_map, n):
    fewest = [999999999]
    for i in range(n):
        if len(edge_map[i]) == len(edge_map[fewest[0]]): #they are same amnt of edges so add to fewest list.
            fewest.append(i) 
        else: 
            if len(edge_map[i]) < len(edge_map[0]): #found city with less edges, reset fewest list, add new city
                fewest.clear.append(i) 
    return np.random.choice(fewest) if len(fewest) > 1 else fewest[0]


#returns each generation. so that main can run simAn on many gens. 
def simAn(matrix, n, pop_size, mut_chance, population):
    
    p1,p2 = parents(matrix, pop_size) #get two parents
    edge_map = edgeMap(p1,p2, n) #if negative then its prioritized: common sequence in both parents
    child = []
    #need to create a child by using ER (enhanced with common edges)
    
    #choose the city with the fewest edges in the edgemap.
    current_city = fewestEdges(edge_map, n) #returns city w/ fewest edges
    #add to child[0], as it's the first city. 
    child[0] = current_city
    #remove all occurances of this parent from the edgemap 
    removeCity(edge_map, current_city)
    
    #find city in current's adj list which has fewest neighbors
    for i in range(1, n): #start at 1 because we already found child's first element.
        ...
         
    
    


def main():
    
    matrix = np.loadtxt(sys.argv[1])
    n = matrix.size[0] #amnt of row
    ##### HYPERPARAMETERS #####
    mut_chance = 0
    pop_size = 0 
    gen_num = 0
     #creates population of random traversals, parents.
    population = getPopulation(matrix, pop_size, n)
    
    simAn(matrix, n, pop_size, mut_chance, population)
    



if __name__ == "__main__":
    main()
