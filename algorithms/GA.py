import numpy as np 
import sys 
import random 
from HC import randomTour, swap, cost
import math

#returns a list of pop_size number random traversals
def getPopulation(matrix, pop_size, n):
    return [randomTour(matrix, n)[1] for _ in range(pop_size)]


def edgeMap(matrix, p1, p2):
    ...


#returns each generation. so that main can run simAn on many gens. 
def simAn(matrix, n, pop_size, mut_chance, population):
    
    #select 2 random parents 
    p1 = random.randint(0, pop_size - 1)
    p2 = random.randint(0, pop_size - 1)
    while p1 == p2:
        p2 = random.randint(0, pop_size - 1)
    
    #create the edgemap for the parents. 
    edge_map = edgeMap(matrix, p1,p2)


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
