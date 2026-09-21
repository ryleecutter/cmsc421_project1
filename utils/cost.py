import numpy as np 
import sys
import random



#takes matrix and path

def cost(matrix, path):
    sum=0
    for i in range(len(path)-2):
        for j in range(i+1,len(path)-1):
            sum += matrix[i][j]   
    return sum
