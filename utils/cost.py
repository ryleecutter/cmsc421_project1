import numpy as np 
import sys
import random



#takes matrix and path

def cost(matrix, path):
    sum=0
    for i in range(len(path)-2):
            sum += matrix[path[i]][path[i+1]]   
    return sum
