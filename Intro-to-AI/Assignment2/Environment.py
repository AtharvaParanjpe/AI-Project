import numpy as np
import random

class board():
    def __init__(self, d, n_percent):
        # Generate a board, n_percent of which are mines. 
        self.d = d
        self.__board = np.zeros((d,d))
        self.__n = int(d*d*n_percent/100)
        self.mineID = -100
        for x in range(0,self.__n):
            i = random.randint(0,d-1)
            j = random.randint(0,d-1)
            self.__board[i][j] = self.mineID

    def TraversalTheCell(self, i, j):
        # This is the function for agents to use for telling the result of uncovering the board(i,j).
        # Input: i,j means the board(i,j)
        # Output:   board(i,j) is mine -> return False
        #           board(i,j) is not a mine -> return the number of mines surrounding board(i,j)
        if self.__board[i][j] == self.mineID:
            return False
        return self.__DetectSurroundingMines(i, j)

    def __GetTheCell(self, i, j):
        # This is the function for board itsown to use for telling whether the board(i,j). is a mine or not.
        # Input: i,j means the board(i,j)
        # Output:   board(i,j) is mine -> return False
        #           board(i,j) is not a mine -> return True
        if self.__board[i][j] == self.mineID:
            return False
        return True

    def __DetectSurroundingMines(self, i, j):
        # This is the function for board itsown to use for telling how many mines surrounding the board(i,j).
        # Input: i,j means the board(i,j)
        # Output: the number of mines surrounding board(i,j)
        s = [   (i-1,j-1), (i-1, j), (i-1,j+1), 
                (i,j-1), (i,j+1), 
                (i+1,j-1), (i+1, j), (i+1,j+1)]
        cnt = 0
        for x in s:
            (ii, jj) = x
            if (ii>=0) and (jj>=0) and (ii<=self.d-1) and (jj<=self.d-1):
                if self.__GetTheCell(ii,jj) is False:
                    cnt = cnt+10
        return cnt

    def PrintTheCell(self, i, j):
        # Print the value of the board(i,j).
        print(self.__board[i][j])

    def PrintTheBoard(self):
        # Print the board
        print(np.where(self.__board == self.mineID, False, True))