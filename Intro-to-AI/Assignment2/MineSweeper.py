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
    def PrintTheBaord(self):
        # Print the board
        print(np.where(self.__board == self.mineID, False, True))

class agent():
    def __init__(self, board):
        # Generate an agent, which knows the basic info of the board(Not includ the exact location of mines.)
        # This agent also has an attribute, "visited", to record where it has visited on the board 
        self.board = board
        self.d = int(board.d)
        self.visited = np.zeros((self.d, self.d))-1
    def SelectARandomCell(self):
        # Select a random cell, until which is not visited before
        # Output:   the selection is a mine -> change the value of "visited" to -100 and return false
        #           the selection is not a mine -> change the value of "visited" to the number of surrouned mines and return True
        while(True):
            i = random.randint(0,self.d-1)
            j = random.randint(0,self.d-1)
            if self.visited[i][j] == -1:
                result = self.board.TraversalTheCell(i, j)
                if result is False:
                    self.visited[i][j] = -100 
                    return False    
                else:
                    self.visited[i][j] = result 
                    return True
            break
    def SelectRandomCells(self):
        # Select random cells until selecting the cell, which is a mine
        while(True):
            if self.SelectARandomCell() is False:
                break
        print(self.visited)
        self.board.PrintTheBaord()

# Generate a board b
b = board(10,20)
# Generate an agent
agent = agent(b)
# The agent do a random selections on the board
agent.SelectRandomCells()