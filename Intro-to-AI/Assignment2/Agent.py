import numpy as np
import random
from Environment import *

class agent():
    def __init__(self, board):
        # Generate an agent, which knows the basic info of the board(Not includ the exact location of mines.)
        # This agent also has an attribute, "visited", to record where it has visited on the board 
        self.board = board
        self.d = int(board.d)
        self.visited = np.zeros((self.d, self.d))-1

    # Select a random cell, until which is not visited before
    # Output:   the selection is a mine -> change the value of "visited" to -100 and return false
    #           the selection is not a mine -> change the value of "visited" to the number of surrouned mines and return True
    def SelectARandomCell(self):
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
        while(np.any(self.visited == -1)):
            self.SelectARandomCell()
        print(self.visited)
        self.board.PrintTheBoard()
