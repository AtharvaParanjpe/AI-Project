import numpy as np
import random
from Environment import *

class BonusAgent():
    identified_mine = 9
    tracked_mine = -9
    neighbors = {(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)}
    def __init__(self, board):
        # Generate an agent, which knows the basic info of the board(Not includ the exact location of mines.)
        # This agent also has an attribute, "visited", to record where it has visited on the board 
        self.board = board
        self.d = int(board.d)
        self.visited = np.zeros((self.d, self.d))-1
        # values in visited[][]:
        # -1: did not visited
        #  (0~8): (number of mines around it)
        # tracked_mine: it is where bomb is and we did not know about that
        # identified_mine: it is where we know bomb is
        # other numbers: something wrong
    def select_a_random_cell(self):
        # Select a random cell, until which is not visited before
        # Output:   the selection is a mine -> change the value of "visited" to tracked_mine and return false
        #           the selection is not a mine -> change the value of "visited" to the number of surrouned mines and return True
        while(True):
            i = random.randint(0,self.d-1)
            j = random.randint(0,self.d-1)
            if self.visited[i][j] == -1:
                result = self.board.TraversalTheCell(i, j)
                if result is False:
                    self.visited[i][j] = self.tracked_mine  
                    self.__update_when_mine(i,j)
                    return (i,j)    
                else:
                    self.visited[i][j] = result  
                    self.__update_when_safe(i,j)
                    return (i,j)


    def select_a_cell(self, i, j):
        # Select a cell(i,j)
        # Output:   the selection is a mine -> change the value of "visited" to tracked_mine and return false
        #           the selection is not a mine -> change the value of "visited" to the number of surrouned mines and return True
        if self.visited[i][j] == -1:
            result = self.board.TraversalTheCell(i, j)
            if result is False:
                self.visited[i][j] = self.tracked_mine
                self.__update_when_mine(i,j)
                return False    
            else:
                self.visited[i][j] = result
                self.__update_when_safe(i,j)
                return True
    def __update_when_mine(self,i,j):
        return True
    def __update_when_safe(self,i,j):
        ## checking for 80 percent probability
        randomVal = random.randint(1,100)
        print(randomVal)
        if self.visited[i][j] == self.tracked_mine:
            return False
        elif self.visited[i][j] in range(0,8) and randomVal>20 :
            clue = self.visited[i][j]
            n_hid = self.number_of_hiddens(i,j)
            if n_hid != 0:             
                if n_hid == clue-self.number_of_revealed_mines(i,j):
                    self.__mark(i,j)
                elif n_hid == (8-clue)-self.number_of_revealed_safes(i,j):
                    self.__reveal(i,j)
                else:
                    self.select_a_random_cell()
        return False 
    def __mark(self,i,j):
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                value = int(self.visited[xx][yy])
                if value == -1:
                    self.visited[xx][yy] = self.identified_mine
    def __reveal(self,i,j):
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                value = int(self.visited[xx][yy])
                if value == -1:
                    self.select_a_cell(xx, yy)
    def number_of_hiddens(self,i,j):
        # Get the number of hiddens around the location (i,j) in the visisted 2d array
        n_of_hids = 0
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                value = int(self.visited[xx][yy])
                if value == -1:
                    n_of_hids = n_of_hids+1
        return n_of_hids
    def number_of_revealed_safes(self,i,j):
        # Get the number of revealed safe cells around the location (i,j) in the visisted 2d array
        n_of_safes = 0
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                # print("XX:" +str(xx)+ " YY: "+str(yy))
                value = int(self.visited[xx][yy])
                # print("Value: "+ str(value))
                if value in range(0, len(self.neighbors)):
                    n_of_safes = n_of_safes+1
        return n_of_safes
    def number_of_revealed_mines(self,i,j):
        # Get the number of revealed mine cells around the location (i,j) in the visisted 2d array
        n_of_mines = 0
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                value = int(self.visited[xx][yy])
                if value == self.tracked_mine:
                    n_of_mines = n_of_mines+1
                elif value == self.identified_mine:
                    n_of_mines = n_of_mines+1
        return n_of_mines
    def number_of_surroundings(self,i,j):
        # Get the number of revealed mine cells around the location (i,j) in the visisted 2d array
        n_of_surroundings = 0
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                n_of_surroundings = n_of_surroundings+1
        return n_of_surroundings

    def select_cells(self):
        # Select cells until visitign all cells 
        while(np.any(self.visited == -1)):  
            for i in range(0, self.d):
                for j in range(0, self.d):
                    self.select_a_cell(i,j)
        return self.score()
    def score(self):
        # Get the score of the visited array. If there are more identified mine in the visited array, then we have higher score. The score is measured by the Board instance.
        mine_list = []
        for (i,j) in zip(*np.where(self.visited == self.identified_mine)):
            mine_list.append((i,j))
        return self.board.score(mine_list)