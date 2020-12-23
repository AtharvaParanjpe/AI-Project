import numpy as np
import random
from Environment import *
from BasicAgent import *

class ITAgent(BasicAgent):
	# Agent developed by Indian and Taiwan Engineer
    def __init__(self, board):
        BasicAgent.__init__(self, board)
        self.sure = 10
        self.init_p = 0.99
        self.prob = np.zeros((self.d, self.d))+self.init_p
    def update_when_mine(self,i,j):     
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                value = int(self.visited[xx][yy])
                if value in range(0,8):
                    self.update_when_safe(xx,yy)
        return True
    def update_when_safe(self,i,j):
        clue = self.visited[i][j]
        n_hid = self.number_of_hid_for_p(i,j)
        if n_hid != 0:            
            if n_hid == clue-self.number_of_revealed_mines(i,j):
                self.mark(i,j)
            elif n_hid == (self.number_of_surroundings(i,j)-clue)-self.number_of_revealed_safes(i,j):
                self.reveal(i,j)
            else: 
                self.update_prob(i,j)
                self.update_safe_neighbors(i,j)
    def update_safe_neighbors(self, i, j):
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                if self.visited[xx][yy] in range(0,8):
                    clue = self.visited[xx][yy]
                    n_hid = self.number_of_hid_for_p(xx,yy)
                    if n_hid != 0:             
                        if n_hid == clue-self.number_of_revealed_mines(xx,yy):
                            self.mark(xx,yy)
                        elif n_hid == (self.number_of_surroundings(xx,yy)-clue)-self.number_of_revealed_safes(xx,yy):
                            self.reveal(xx,yy)   
        return True
    def update_prob(self,i,j):
        clue = self.visited[i][j]
        n_hid = self.number_of_hid_for_p(i,j)
        if n_hid > 0:
            p = float(float(clue-self.number_of_revealed_mines(i,j))/float(n_hid))
            for n in self.neighbors:
                x,y = n
                xx = i+x
                yy = j+y
                if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                    # if self.visited[xx,yy] ==-1:
                    #     if self.number_of_revealed_safes(xx,yy) == 1:
                    #         self.prob[xx][yy] = p
                    if self.prob[xx][yy] == self.init_p:
                        self.prob[xx][yy] = p
    def number_of_hid_for_p(self,i,j):
        # Get the number of hiddens around the location (i,j) in the visisted 2d array
        n_of_hids = 0
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                if self.prob[xx][yy] <= self.init_p:
                    n_of_hids = n_of_hids+1
        return n_of_hids
    def mark(self,i,j):
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                value = int(self.visited[xx][yy])
                if value == -1:
                    self.visited[xx][yy] = self.identified_mine
                    self.prob[xx][yy] = self.sure
                    self.update_when_mine(xx,yy)
    def reveal(self,i,j): 
        for n in self.neighbors:
            x,y = n
            xx = i+x
            yy = j+y
            if not ((xx<0) or (yy<0) or (xx>=self.d) or (yy>=self.d)):
                value = int(self.visited[xx][yy])
                if value == -1:
                    self.select_a_cell(xx, yy)	

    def select_a_cell(self, i, j):
        # Select a cell(i,j)
        # Output:   the selection is a mine -> change the value of "visited" to tracked_mine and return false
        #           the selection is not a mine -> change the value of "visited" to the number of surrouned mines and return True
        if self.visited[i][j] == -1:
            result = self.board.TraversalTheCell(i, j)
            self.prob[i][j] = self.sure
            if result is False:
                self.visited[i][j] = self.tracked_mine
                self.update_when_mine(i,j)
                return (i,j)    
            else:
                self.visited[i][j] = result
                self.update_when_safe(i,j)
                return (i,j)
    def select_a_best_cell(self):
        # Select a random cell, until which is not visited before
        # Output:   the selection is a mine -> change the value of "visited" to tracked_mine and return false
        #           the selection is not a mine -> change the value of "visited" to the number of surrouned mines and return True
        while(True):
            [i,j] = self.extract_loc_of_min_p()
            self.select_a_cell(i, j)
            # print(i,j)
            # print(self.visited)
            # print(self.prob)
            return (i,j)

    def extract_loc_of_min_p(self):
        result = np.where(self.prob == np.min(self.prob)) 
        return [result[0][0], result[1][0]]

    def select_cells(self):
        # Select cells until visitign all cells 
        while(np.any(self.visited == -1)):  
            self.select_a_best_cell()
        return self.score()