import pandas as pd 
import numpy as np 
import random
class SheepHunter:
    def __init__(self,dim1,dim2):
        self.m = dim1
        self.n = dim2
        self.trackingMatrix = [['-' for j in range(8)] for i in range(8)]
        self.sheepPos, self.dog1Pos , self.dog2Pos = [4,0],[6,3],[0,7]####self.initializeRandomPos(dim1,dim2)

        self.startCorneringD1 = False
        self.startCorneringD2 = False
        self.count = 0
    
    def initializeRandomPos(self,dim1,dim2):
        positions = []
        sheepPos = [np.random.randint(0,dim1-1),np.random.randint(0,dim2-1)]
        # print(sheepPos)
        self.trackingMatrix[sheepPos[0]][sheepPos[1]] = 'S'
        positions.append(sheepPos)
        dog1Pos = [np.random.randint(0,dim1-1),np.random.randint(0,dim2-1)]
        if(dog1Pos in positions):
            while(dog1Pos in positions):
                dog1Pos = [np.random.randint(0,dim1-1),np.random.randint(0,dim2-1)]
        positions.append(dog1Pos)
        dog2Pos = [np.random.randint(0,dim1-1),np.random.randint(0,dim2-1)]
        if(dog2Pos in positions):
            while(dog2Pos in positions):
                dog2Pos = [np.random.randint(0,dim1-1),np.random.randint(0,dim2-1)]
        self.trackingMatrix[dog1Pos[0]][dog1Pos[1]] = 'D'
        self.trackingMatrix[dog2Pos[0]][dog2Pos[1]] = 'D'
        for tM in self.trackingMatrix:
            print(tM)
        print('-------------------------x---------------------------------x------------------------------')
        return sheepPos,dog1Pos,dog2Pos

    def getNeighbors(self,xIndex,yIndex):
        neighbors = []
        if(xIndex>0 and (self.trackingMatrix[xIndex-1][yIndex]!='S' and self.trackingMatrix[xIndex-1][yIndex]!='D')):
            neighbors.append([xIndex-1,yIndex])
        if(xIndex<self.m-1 and (self.trackingMatrix[xIndex+1][yIndex]!='S' and self.trackingMatrix[xIndex+1][yIndex]!='D')):
            neighbors.append([xIndex+1,yIndex])
        if(yIndex>0 and (self.trackingMatrix[xIndex][yIndex-1]!='S' and self.trackingMatrix[xIndex][yIndex-1]!='D' )):
            neighbors.append([xIndex,yIndex-1])
        if(yIndex<self.n-1 and (self.trackingMatrix[xIndex][yIndex+1]!='S' and self.trackingMatrix[xIndex][yIndex+1]!='D') ):
            neighbors.append([xIndex,yIndex+1])
        return neighbors


    def moveSheep(self):
        i,j = self.sheepPos
        # for x in self.trackingMatrix:
        #     print(x)
        self.trackingMatrix[i][j] = '-'
        nearestElements = self.getNeighbors(i,j)
        if (len(nearestElements)>0):
            s = random.choice(nearestElements) 
            self.sheepPos = [s[0],s[1]]
            self.trackingMatrix[s[0]][s[1]] = 'S'
            

    def moveDogs(self):
        if(self.trackingMatrix[0][0]=='S' and self.trackingMatrix[0][1]=='D' and self.trackingMatrix[1][0]=='D' ):
            return "Over"
        s1,s2 = self.sheepPos
        
        if(self.startCorneringD1):
                self.trackingMatrix[self.dog1Pos[0]][self.dog1Pos[1]] = '-'
                self.dog1Pos = [s1+0,s2+1]
                self.trackingMatrix[self.dog1Pos[0]][self.dog1Pos[1]] = 'D'
        if(self.startCorneringD2):
                self.trackingMatrix[self.dog2Pos[0]][self.dog2Pos[1]] = '-'
                self.dog2Pos = [s1+1,s2+0]
                self.trackingMatrix[self.dog2Pos[0]][self.dog2Pos[1]] = 'D'
        if(not self.startCorneringD1 or not self.startCorneringD2):
            self.move_dog1()
            self.move_dog2()
        
    def startGame(self):

        # print('--------------------------------------x--------------------------------------------x-------------------------')
        try:
            while(not self.sheepPos == [0,0] or( not (self.dog1Pos==[0,1] and self.dog2Pos==[1,0]) and not(self.dog1Pos==[1,0] and self.dog2Pos==[0,1]) )):
                self.moveSheep()
                self.moveDogs()
                self.count+=1
                # print('----------------------------------------x-----------------------------------------x----------------------------')
        except :
            print()
        # print(self.count)
        for x in self.trackingMatrix:
            print(x)
        print('----------------------x--------------------------------x-------------------------')



    ## goes to the bottom of the sheep
    def move_dog1(self):
        i,j = self.dog1Pos
        self.trackingMatrix[i][j] = '-'
        if(self.sheepPos[0]+1<self.dog1Pos[0] and self.sheepPos[0]+1>0 and (self.trackingMatrix[self.dog1Pos[0]-1][self.dog1Pos[1]]!='D' and self.trackingMatrix[self.dog1Pos[0]-1][self.dog1Pos[1]]!='S')):
            self.dog1Pos[0]-=1
        elif(self.sheepPos[0]+1>self.dog1Pos[0] and self.sheepPos[0]+1<self.m-1 and (self.trackingMatrix[self.dog1Pos[0]+1][self.dog1Pos[1]]!='D' and self.trackingMatrix[self.dog1Pos[0]+1][self.dog1Pos[1]]!='S' )):
            self.dog1Pos[0]+=1
        elif(self.sheepPos[0]+1==self.dog1Pos[0]):
            if(self.sheepPos[1]<self.dog1Pos[1] and self.sheepPos[1]>=0 and (self.trackingMatrix[self.dog1Pos[0]][self.dog1Pos[1]-1]!='D' and self.trackingMatrix[self.dog1Pos[0]][self.dog1Pos[1]-1]!='S' )):
                self.dog1Pos[1]-=1
            elif(self.sheepPos[1]>self.dog1Pos[1] and self.sheepPos[1]<self.m and (self.trackingMatrix[self.dog1Pos[0]][self.dog1Pos[1]+1]!='D' and self.trackingMatrix[self.dog1Pos[0]][self.dog1Pos[1]+1]!='S')):
                self.dog1Pos[1]+=1
            else:
                self.startCorneringD1 = True
        # print("Dog1: " ,self.dog1Pos)
        self.trackingMatrix[self.dog1Pos[0]][self.dog1Pos[1]] = 'D'

    ## goes to the right of the sheep
    def move_dog2(self):
        i,j = self.dog2Pos
        self.trackingMatrix[i][j] = '-'
        if(self.sheepPos[1]+1<self.dog2Pos[1] and self.sheepPos[1]+1>0 and (self.trackingMatrix[self.dog2Pos[0]][self.dog2Pos[1]-1]!='D' and self.trackingMatrix[self.dog2Pos[0]][self.dog2Pos[1]-1]!='S')):
            self.dog2Pos[1]-=1
        elif(self.sheepPos[1]+1>self.dog2Pos[1] and self.sheepPos[1]+1<self.m-1 and (self.trackingMatrix[self.dog2Pos[0]][self.dog2Pos[1]+1]!='D' and self.trackingMatrix[self.dog2Pos[0]][self.dog2Pos[1]+1]!='S' )):
            self.dog2Pos[1]+=1
        elif(self.sheepPos[1]+1==self.dog2Pos[1] ):
            if(self.sheepPos[0]<self.dog2Pos[0] and self.sheepPos[0]>=0 and (self.trackingMatrix[self.dog2Pos[0]-1][self.dog2Pos[1]]!='D' and self.trackingMatrix[self.dog2Pos[0]-1][self.dog2Pos[1]]!='S' )):
                self.dog2Pos[0]-=1
            elif(self.sheepPos[0]>self.dog2Pos[0] and self.sheepPos[0]<self.m and (self.trackingMatrix[self.dog2Pos[0]+1][self.dog2Pos[1]]!='D' and self.trackingMatrix[self.dog2Pos[0]+1][self.dog2Pos[1]]!='S')):
                self.dog2Pos[0]+=1
            else:
                self.startCorneringD2 = True
        # print("Dog2: " ,self.dog2Pos)
        self.trackingMatrix[self.dog2Pos[0]][self.dog2Pos[1]] = 'D'

    
       


hunter = SheepHunter(8,8)
hunter.startGame()
average = []
for i in range(20):
    hunter.startGame()
    average.append(hunter.count)
print(sum(average)/len(average))
 