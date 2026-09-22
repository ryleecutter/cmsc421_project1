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
def edgeMap(matrix, p1, p2, n):
    #need two structures;
    #direct neighbor list from both
    edgemap = [set()] * n  #list with set, same indices as given in matrix
    for i in range(n-1):
        edgemap[p1[i]].add(p1[i+1]) #add edges to edge map. set doesnt allow duplicates so safe.
        edgemap[p1[i+1]].add(p1[i])
        edgemap[p2[i]].add(p2[i+1])
        edgemap[p2[i+1]].add(p2[i])
    
            
    


#returns each generation. so that main can run simAn on many gens. 
def simAn(matrix, n, pop_size, mut_chance, population):
    
    #select 2 random parents 
    p1 = random.randint(0, pop_size - 1)
    p2 = random.randint(0, pop_size - 1)
    while p1 == p2:
        p2 = random.randint(0, pop_size - 1)
    
    #create the edgemap for the parents. 
    edge_map = edgeMap(matrix, p1,p2, n)


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
