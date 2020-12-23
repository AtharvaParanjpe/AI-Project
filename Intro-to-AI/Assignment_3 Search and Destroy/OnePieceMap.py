import numpy as np
import random

class OnePieceMap:
    def __init__(self, d):      
        #probabilities for each terrain
        self.d = d
        self.terrainType = {
            0 : 0.1,
            1 : 0.3,
            2 : 0.7,
            3 : 0.9
        }

        p_flat = 0.2
        p_hilly = p_flat + 0.3
        p_forest = p_hilly + 0.3
        p_cave = p_forest + 0.2

        self.__target =  (random.randint(0, d-1), random.randint(0, d-1)) ##(1, 0)
        
        # initializing the search terrain to 0  values
        self.terrain = np.zeros((d, d)) ##[[2, 2, 1],[1, 0, 2],[3, 1, 1]]

        self.total_cells = d*d
        self.visited = np.ones((d, d))*-1

        # assigning terrain types with the following values - 
        # flat : 0
        # hilly : 1
        # forest : 2
        # cave : 3
        for i in range(self.d):
            for j in range(self.d):
                x = random.random()
                if x <= p_flat:
                    self.terrain[i][j] = 0
                elif x <= p_hilly and x>p_flat:
                    self.terrain[i][j] = 1
                elif x <=p_forest and x>p_hilly:
                    self.terrain[i][j] = 2
                elif x>p_forest and x <=p_cave: 
                    self.terrain[i][j] = 3
        # self.terrain = np.ones((self.d,self.d))
        # print(self.terrain)


    def whether_the_cell_the_target( self, index):
        if index == self.__target:
            return self.__the_uncertain_answer(index[0],index[1])
        return False  


    def __the_uncertain_answer(self, i, j):
        random_number = random.random()
        if random_number<=self.terrainType[self.terrain[i][j]]:
            return False
        return True

        