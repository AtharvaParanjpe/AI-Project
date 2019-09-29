from tkinter import *
import math
import copy
import random
import numpy as np
import time
from random import shuffle, randrange
from collections import deque
import matplotlib.pyplot as plt

		
class theMaze:
	## initializing the elements required
	def __init__( self, rows, columns):
		self.root = Tk()
		self.box = dict()
		self.width = math.ceil(300/rows) #root.winfo_screenwidth()
		self.height = math.ceil(300/columns) # root.winfo_screenheight()
		self.roots = Canvas(self.root, height = rows*self.height, width = columns* self.width, bg="#666666", highlightthickness=0, bd = 0)
		self.frame = {}
		self.pathMap = {}
		self.passFailList =[]
		self.rows = rows
		self.columns = columns
		self.mapstate = np.ones((self.rows, self.columns))
		self.flamabilityRate = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
		
		self.make_rand_maze(0.2)
		self.roots.pack(fill = "both", expand = True)
		self.root.title("AI Maze")   
		
		self.fireList = [[0,self.columns-1]]

		self.fireButton = Button(self.root,text='Generate Fire Maze',command=self.dfs_with_fire_for_visualization)
		self.fireButton.pack(side='bottom')

		self.reset = Button(self.root,text='Reset',command=self.resetButton)
		self.reset.pack(side='bottom')
		self.fringe = None
		self.goal = self.mapstate[self.rows-1, self.columns-1]
	
	## generating the maze based on a probability 
	def make_rand_maze(self, prob):
		rand = np.random.rand(self.rows, self.columns)
		self.mapstate = np.where(rand<prob, 0, 1)
		self.mapstate[0,0] = 1
		self.mapstate[self.rows-1, self.columns-1] = 1
		self.mapstate[0,self.columns-1] = 5
		self.mapstateCopy = np.copy(self.mapstate)
		
		self.update_the_whole_maze()

	## update the main matrix to sync with the gui
	def update_the_maze_simple(self, row,col):
		if self.mapstate[row,col] == 0:
			self.drawBox("black", row, col)
		elif self.mapstate[row,col] == 1:
			self.drawBox("white", row, col)
		elif self.mapstate[row,col] == 2:
			self.drawBox("green", row, col)
		elif self.mapstate[row,col] == 3:
			self.drawBox("orange", row, col)
		elif self.mapstate[row,col] == 5:
			self.drawBox("red", row, col)
		else:
			self.drawBox("grey", row, col)

	## refresh operation used for reset and other similar functionalities
	def update_the_whole_maze(self):
		for i in range(self.rows):
			for j in range(self.columns):
				self.update_the_maze_simple(i, j)
		self.mapstateCopy = np.copy(self.mapstate)

	## coloring the box with the desired color for the gui
	def drawBox(self, color, r,c):
		# the r and c both starts from zero
		index = self.rows*(r)+c
		self.frame[index] = Frame(self.roots,width=self.width,height=self.height,bg=color)
		self.frame[index].pack_propagate(0)
		self.box[index] = Label(self.frame[index], text=index, borderwidth=5, background=color, width = self.width, height = self.height , fg = "grey", font=("Courier", math.ceil(self.height/2)))
		self.box[index].pack(fill="both", expand=True,side='left')
		self.frame[index].place(x=(c)*self.width,y=(r)*self.height)
		self.roots.pack(fill = "both", expand = True)
	
	## used to check if a particular element in the matrix was already visited
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

	## DEPTH FIRST SEARCH MODIFIED FOR OPERATING WITH THE FIRE CONDITION
	def depthFirstSearch(self,q):
		s = time.time()
		self.fringe = []
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
								
				return 1
			self.fringe,self.pathMap = self.pushNeighboursIfNotVisited(element[0],element[1],self.fringe,self.pathMap,3)
			
			self.mapstate[element[0],element[1]] = 3
			self.update_the_maze_simple(element[0],element[1])
		print("DFS %s", time.time()-s)
		
		return 0
	

	# HELPER FUNCTION TO CALCULATE THE NEIGHBOURS HAVING FIRE	
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
			self.update_the_maze_simple(i,j)
			self.fireList.append([i,j])
	
	## GENERATES THE FIRE MAZE
	## CALLED IN DFS WITH EACH ITERATION

	def generate_fire_maze(self,q):
		probability = 1-q
		tempList = copy.deepcopy(self.fireList)
		for x in tempList:
			i,j=x
			if(i>0 and self.mapstate[i-1,j]):
				self.helper_fire_maze(i-1,j,probability)
			if(j>0 and self.mapstate[i,j-1]):
				self.helper_fire_maze(i,j-1,probability)
			if(i<self.rows-1 and self.mapstate[i+1,j]):
				self.helper_fire_maze(i+1,j,probability)
			if(j<self.columns-1 and self.mapstate[i,j+1]):
				self.helper_fire_maze(i,j+1,probability)
	

	## CODE USED FOR CALCULATING AVERAGE SUCCESS RATE

	def dfs_with_fire(self):
		self.passFailList = []
		self.flamabilityRate = []
		for q in range(1,101,10) : 
			avgSuccessVariable = 0
			for x in range(20):
				self.resetButton()
				avgSuccessVariable+=self.depthFirstSearch(float(q/100))

			avgSuccessVariable/=20
			self.passFailList.append(avgSuccessVariable)
			self.flamabilityRate.append(float(q/100))

		# plot graph
		plt.xlabel('Flamability Rate')
		plt.ylabel('Success Fail')
		plt.plot(self.flamabilityRate,self.passFailList)
		plt.show()
		


	## TO CHECK GRAPHS FOR INDIVIDUAL RATES UNCOMMENT THE BREAK COMMAND
	## TO ALLOW TKINTER TO VISUALIZE , A SMALLER SUBSET WAS RUN USING SMALLER DIMENSIONS

	def dfs_with_fire_for_visualization(self):
		self.passFailList = []
		for q in self.flamabilityRate:
			self.resetButton()
			avgSuccessVariable=self.depthFirstSearch(q)
			self.passFailList.append(avgSuccessVariable)
			# break 
		
		# plot graph
		plt.xlabel('Flamability Rate')
		plt.ylabel('Success Fail')
		plt.plot(self.flamabilityRate,self.passFailList)
		plt.show()
		
	## RESET THE STATE OF THE MAP FOR EFFECTIVE VISUALIZATION
	def resetButton(self):
		# print(self.mapstate)
		for r in range(0, self.rows):
			for c in range(0, self.columns):
				if self.mapstate[r,c] != self.mapstateCopy[r,c]:
					self.mapstate[r,c] = self.mapstateCopy[r,c]
					self.update_the_maze_simple(r,c)		
		self.fireList = [[0,self.columns-1]]	

def main():
	maze = theMaze(10,10)
	maze.root.mainloop()
	
if __name__ == '__main__':
	main()