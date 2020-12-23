import math
import copy
import random
import numpy as np
import time
from random import shuffle, randrange
import matplotlib.pyplot as plt
#import seeker
from collections import deque
        
class theMaze:
	def __init__( self, dim, prob):
		self.rows = dim
		self.columns = dim
		self.mapstate = np.ones((self.rows, self.columns))
		self.make_rand_maze(prob)
		self.fringe = None
		self.goal = self.mapstate[self.rows-1, self.columns-1]
		self.flamabilityRate = []
		self.passFailList = []
		self.fireList = [[0,self.columns-1]]

	def make_rand_maze(self, prob):
		rand = np.random.rand(self.rows, self.columns)
		self.mapstate = np.where(rand<prob, 0, 1)
		self.mapstate[0,0] = 1
		self.mapstate[self.rows-1, self.columns-1] = 1
		self.mapstateCopy = np.copy(self.mapstate)
		self.pathMap = {}

	def wasAlreadyVisited(self,xIndex,yIndex,visitVal):
		if(self.mapstate[xIndex,yIndex]!=visitVal):
			return True;
		else:
			return False

	## helper function for dfs used for pushing neighbours   
	## (x+1,y) and (x,y+1) will be pushed first because they 
	## move towards the desired goal state
	
	def pushNeighboursIfNotVisited(self,xIndex,yIndex,fringe,pathMap,visitVal):
		
		if(yIndex>0):
			if(self.wasAlreadyVisited(xIndex,yIndex-1,visitVal) and self.mapstate[xIndex,yIndex-1]!=0):
				fringe.append([xIndex,yIndex-1])
				pathMap[(xIndex,yIndex-1)] = [xIndex,yIndex]
		
		if(xIndex>0):
			if(self.wasAlreadyVisited(xIndex-1,yIndex,visitVal) and self.mapstate[xIndex-1,yIndex]!=0):
				fringe.append([xIndex-1,yIndex])
				pathMap[(xIndex-1,yIndex)] = [xIndex,yIndex]
		
		
		
		
		if(yIndex<self.rows-1):
		
			if(self.wasAlreadyVisited(xIndex,yIndex+1,visitVal) and self.mapstate[xIndex,yIndex+1]!=0):
				fringe.append([xIndex,yIndex+1])
				pathMap[(xIndex,yIndex+1)] = [xIndex,yIndex]
		
		if(xIndex<self.rows-1):
			if(self.wasAlreadyVisited(xIndex+1,yIndex,visitVal) and self.mapstate[xIndex+1,yIndex]!=0):
				fringe.append([xIndex+1,yIndex])
				pathMap[(xIndex+1,yIndex)] = [xIndex,yIndex]
		
		return fringe,pathMap

	def depthFirstSearch(self,q):
		s = time.time()
		self.fringe = []
		# self.pathMap[[0,0]] = [-1,-1]
		self.fringe.append([0,0])
		self.pathMap[(0,0)] = [-1,-1]
		
		## started by pushing the first node in the fringe
		while(len(self.fringe)>0):
			element = self.fringe.pop()
			self.generate_fire_maze(q)
			# self.visited.append(element)
			if(element in self.fireList):
				return 0
			if(element[0]==self.rows-1 and element[1] == self.columns-1):
				self.mapstate[element[0],element[1]] = 2
				# self.update_the_maze_simple(element[0],element[1])
				while(self.pathMap[(element[0],element[1])]!=[-1,-1]):
					x,y = self.pathMap[(element[0],element[1])]
					
					element = (x,y)
					self.mapstate[x,y] = 2
					# self.update_the_maze_simple(x,y)										
				return 1
			self.fringe,self.pathMap = self.pushNeighboursIfNotVisited(element[0],element[1],self.fringe,self.pathMap,3)
			
			self.mapstate[element[0],element[1]] = 3
			# self.update_the_maze_simple(element[0],element[1])
		print("DFS %s", time.time()-s)
		
		return 0
		
	def calcNeighboursOfElement(self,xIndex,yIndex):
		counter = 0
		if(yIndex>0):
			if(self.mapstate[xIndex,yIndex-1]==5):
				counter+=1
		if(xIndex>0):
			if(self.mapstate[xIndex-1,yIndex]==5):
				counter+=1
		if(xIndex<self.rows-1):
			if(self.mapstate[xIndex+1,yIndex]==5):
				counter+=1
		if(yIndex<self.rows-1):
			if(self.mapstate[xIndex,yIndex+1]==5):
				counter+=1
		return counter

	## helper funcction for fire_maze_generation to avoid redundancy
	def helper_fire_maze(self,i,j,probability):
		counter = self.calcNeighboursOfElement(i,j)
		if(counter==4):
			self.mapstate[i,j] = 5
		else:
			self.mapstate[i,j] = 5 if random.random()<(1-math.pow(probability,counter)) else self.mapstate[i,j]
		if(self.mapstate[i,j]==5 and [i,j] not in self.fireList):
			# self.update_the_maze_simple(i,j)
			self.fireList.append([i,j])
		
	def generate_fire_maze(self,q):
		# print("function called")
		probability = 1-q
		tempList = copy.deepcopy(self.fireList)
			
		# looping can be conditioned to start from top right
		for x in tempList:
			# print(x)
			i,j=x
			## dont update if black
			if(i>0 and self.mapstate[i-1,j]):
				self.helper_fire_maze(i-1,j,probability)
			if(j>0 and self.mapstate[i,j-1]):
				self.helper_fire_maze(i,j-1,probability)
			if(i<self.rows-1 and self.mapstate[i+1,j]):
				self.helper_fire_maze(i+1,j,probability)
			if(j<self.columns-1 and self.mapstate[i,j+1]):
				self.helper_fire_maze(i,j+1,probability)

	def dfs_with_fire(self):
		
		self.passFailList = []
		# create a for loop for q 
		for q in range(1,101,5) : 
			avgSuccessVariable = 0
			for x in range(20):
				self.resetButton()
				avgSuccessVariable+=self.depthFirstSearch(float(q/100))

			avgSuccessVariable/=20
			self.passFailList.append(avgSuccessVariable)
			self.flamabilityRate.append(q/100)
		# plot graph
		plt.plot(self.flamabilityRate,self.passFailList)
		plt.show()
		

	def resetButton(self):
		# print(self.mapstate)
		for r in range(0, self.rows):
			for c in range(0, self.columns):
				if self.mapstate[r,c] != self.mapstateCopy[r,c]:
					self.mapstate[r,c] = self.mapstateCopy[r,c]
		self.fireList = [[0,self.columns-1]]	


maze = theMaze(20,0.2)
maze.dfs_with_fire()
# records = ChooseDimExp("dfs")
# records.extend(ChooseDimExp("a_star_euc"))
# records.extend(ChooseDimExp("a_star_man"))