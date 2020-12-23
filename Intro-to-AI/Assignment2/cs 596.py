## Importing built in libraries to compute the desired operations
## namely svd and matrx filling followed by computation of error 
import random 
import numpy as np
from numpy.linalg import matrix_rank,svd
import copy
import math


## Initializing the original matrix
matrix = [[]]

## Logic for creating the matrix :-
## As the desired rank is 3, only 3 columns of the matrix must be linearly independent 
## to each other. So if we generate 3 columns of random numbers and then compute the remaining 2 
## from a linear combination of the inital 3 then we will have a rank 3 matrix.

## Creating an initial matrix with 3 columns and 20 rows.
for i in range(3):
    arr = []
    for j in range(20):
        
        arr.append(random.randint(1,25))
    matrix.append(np.array(arr))
matrix = matrix[1:]

## two constants that are used to generate the remaining two columns
a = 2
b = 3 

## genearting the remaining columns as a linear combination of the previous three
matrix.append(a*matrix[1]+b*matrix[2])
matrix.append(a*matrix[0]+b*matrix[2])

matrix = np.array(matrix)

## matrix was defined as 5 x 20 so have to take a transpose to make it of desired shape
matrix = np.transpose(matrix)

print(matrix)

N = [2,3,4,5]

## creating an instance of the original matrix so that the same matrix can be 
## used for other N's as well
matrixCopy = copy.deepcopy(matrix)

## loop for testing different values of n
for n in N:
    matrix = copy.deepcopy(matrixCopy)
    
    for i in range(n):
        x,y = random.randint(0,19),random.randint(0,4)
        matrix[x][y]=0
    
    print(matrix)
    
    ## rank of the matrix will keep increasing as more number of random 0's are added
    print(matrix_rank(matrix))
    
    ## computing the svd using pre-defined libraries
    u, sigma, vt = svd(matrix, full_matrices = False)
    print(sigma)
    
    print(matrix.shape, u.shape, sigma.shape, vt.shape)
    
    ## equating the last 2 values to 0 for performing the matrix filling operation
    sigma[3],sigma[4] = 0,0
    
    ## diagonalizing sigma to compute the filled matrix
    sigma = np.diag(sigma)
    
    ## 
    matrix_filled = np.dot(np.dot(u,sigma),vt)
    
    ## computation of the error matrix
    error_matrix = matrix - matrix_filled
    
    ## computing the overall error
    finalError = 0
    for x in error_matrix:
        for y in x:
            finalError += y*y
    finalError = math.sqrt(finalError)
    
    print(finalError)
    print("------------------------------------------------------------------------------------------------------------")
    
