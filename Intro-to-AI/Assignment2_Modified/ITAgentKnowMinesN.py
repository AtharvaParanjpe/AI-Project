import numpy as np
import random
from Environment import *
from ITAgent import *

class ITAgentKnowMinesN(ITAgent):
    def __init__(self, board):
        ITAgent.__init__(self, board)
        self.n_of_mines = self.board.GetNumOfMines()
        self.p = self.n_of_mines/(self.d*self.d)
        self.prob = np.zeros((self.d, self.d))+self.init_p

    def update_all_prob(self):
        if self.n_of_all_hids()>0:
            p = float((self.n_of_all_mines())/self.n_of_all_hids())
            self.p = p
            if p == 1:              
                for i in range(0,self.d):
                    for j in range(0,self.d):
                        if self.prob[i][j]!=10:
                            self.visited[i][j] = self.identified_mine
                            self.prob[i][j] = self.sure 
        return True
    def n_of_all_mines(self):
        x = self.n_of_mines-np.count_nonzero(self.visited == self.identified_mine)
        x = x - np.count_nonzero(self.visited == self.tracked_mine)
        return x
    def n_of_all_hids(self):
        return np.count_nonzero(self.visited == -1)
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
                self.update_all_prob()
                return (i,j)    
            else:
                self.visited[i][j] = result
                self.update_when_safe(i,j)
                self.update_all_prob()
                return (i,j)
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
                    self.update_all_prob()