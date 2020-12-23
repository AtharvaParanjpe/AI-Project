import numpy as np
import random
from Environment import *
from BasicAgent import *

class ITAgent(BasicAgent):
	# Agent developed by Indian and Taiwan Engineer
    def __update_when_mine(self,i,j):
        return True
    
    
    def __update_when_safe(self,i,j):
        if self.visited[i][j] == self.tracked_mine:
            return False
        elif self.visited[i][j] in range(0,8):
            clue = self.visited[i][j]
            n_hid = self.number_of_hiddens(i,j)
            if n_hid != 0:             
                if n_hid == clue-self.number_of_revealed_mines(i,j):
                    print("MARKED!!!")
                    self.__mark(i,j)
                elif n_hid == (8-clue)-self.number_of_revealed_safes(i,j):
                    print("REVEALED!!!")
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
