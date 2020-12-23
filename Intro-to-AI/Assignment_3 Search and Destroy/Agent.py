from OnePieceMap import *
import matplotlib.pyplot as plt
import random
class Agent:
    
    def __init__(self, one_piece_map):
        self.op_map = one_piece_map
        self.ctr = 0
        self.belief = np.ones((self.op_map.d,self.op_map.d))/(self.op_map.d**2)

    def updateBeliefMatrix(self,index):
        x, y = index
        temp_val = self.belief[x][y]           
        # self.belief += self.belief*probability
        # self.belief[x][y] = temp_val - temp_val*probability
        self.belief = self.belief/(self.belief*self.op_map.terrainType[self.op_map.terrain[x][y]]+ 1-self.belief)
        self.belief[x][y] = temp_val*self.op_map.terrainType[self.op_map.terrain[x][y]]/(temp_val*self.op_map.terrainType[self.op_map.terrain[x][y]]+ 1-temp_val)
        # print(self.belief)

    def RandomExplore(self):
        while(True):
            if np.any(self.belief > 0.10):
                i = random.randint(0,self.op_map.d -1)
                j = random.randint(0,self.op_map.d -1)
                # print(self.op_map.belief)
            else:
                indexAssumedTarget = np.argmax(self.belief)
                i = (indexAssumedTarget // self.op_map.d)
                j = (indexAssumedTarget % self.op_map.d)
            # print("Search " + str((i,j)))
            self.ctr+=1
            if self.op_map.whether_the_cell_the_target((i,j)):
                return (i,j),self.ctr
            else:
                self.updateBeliefMatrix((i, j))
                
        # return (i,j)


# treasure_map = OnePieceMap(50)
# luffy = Agent(treasure_map)
# loc, counter = luffy.RandomExplore()
# print("Counter : " , counter)

avg_array = []
median_arr = []
for j in range(1,20):
    a = []
    for i in range(100):
        treasure_map = OnePieceMap(j)
        luffy = Agent(treasure_map)
        loc, counter = luffy.RandomExplore()
        a.append(counter)
    a.sort()
    median = (a[int(len(a)/2)]+a[1+int(len(a)/2)])/2
    median_arr.append(median)
    avg_array.append(sum(a)/len(a))
t = []
for j in range(1,20):
    t.append(j)

plt.plot(t,avg_array)

plt.show()

# plt.figure()

# plt.plot(t,median_arr)

# plt.show()


# treasure_map = OnePieceMap(3)
# luffy = Agent(treasure_map)
# loc, counter = luffy.RandomExplore()
# print("Treasure is in" + str(loc) , counter)