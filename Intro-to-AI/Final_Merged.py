from tkinter import *
import math
import copy
import random
import numpy as np
import time
from random import shuffle, randrange
#import seeker
from collections import deque
		
class theMaze:

	## INITIALIZE THE VARIABLES FOR ALGORITHMS
	def __init__( self, rows, columns):
		self.root = Tk()
		self.box = dict()
		self.width = math.ceil(300/rows) #root.winfo_screenwidth()
		self.height = math.ceil(300/columns) # root.winfo_screenheight()
		self.roots = Canvas(self.root, height = rows*self.height, width = columns* self.width, bg="#666666", highlightthickness=0, bd = 0)
		self.frame = {}
		self.pathMap = {}

		self.rows = rows
		self.columns = columns
		self.mapstate = np.ones((self.rows, self.columns))
		
		self.make_rand_maze(0.2)
		self.roots.pack(fill = "both", expand = True)
		self.root.title("AI Maze")   
		self.dfs = Button(self.root,text='DFS',command=self.depthFirstSearch)   
		self.dfs.pack(side='bottom')
		self.bfs = Button(self.root,text='BFS',command=self.breadthFirstSearch)
		self.bfs.pack(side='bottom')
		self.bi_bfs = Button(self.root,text='Bi-BFS',command=self.bi_directional_BFS)
		self.bi_bfs.pack(side='bottom')
		self.aStarEuc = Button(self.root,text='A*euc',command=self.a_star_euc)
		self.aStarEuc.pack(side='bottom')
		self.aStarMan = Button(self.root,text='A*man',command=self.a_star_man)
		self.aStarMan.pack(side='bottom')
		
		self.reset = Button(self.root,text='Reset',command=self.resetButton)
		self.reset.pack(side='bottom')
		self.fringe = None
		self.goal = self.mapstate[self.rows-1, self.columns-1]
		
	
	## GENERATE THE RANDOM MAZE WITH PROBABILITY
	def make_rand_maze(self, prob):
		rand = np.random.rand(self.rows, self.columns)
		self.mapstate = np.where(rand<prob, 0, 1)
		self.mapstate[0,0] = 1
		self.mapstate[self.rows-1, self.columns-1] = 1
		self.mapstateCopy = np.copy(self.mapstate)
		
		self.update_the_whole_maze()

	## UPDATE THE MAZE BY ROW,COL
	def update_the_maze_simple(self, row,col):
		if self.mapstate[row,col] == 0:
			self.drawBox("black", row, col)
		elif self.mapstate[row,col] == 1:
			self.drawBox("white", row, col)
		elif self.mapstate[row,col] == 2:
			self.drawBox("green", row, col)
		elif self.mapstate[row,col] == 3:
			self.drawBox("orange", row, col)
		else:
			self.drawBox("grey", row, col)

	## UPDATE THE ENTIRE MAZE
	def update_the_whole_maze(self):
		for i in range(self.rows):
			for j in range(self.columns):
				self.update_the_maze_simple(i, j)
		self.mapstateCopy = np.copy(self.mapstate)

	## DRAW THE COLORS FOR THE BOXES
	def drawBox(self, color, r,c):
		# the r and c both starts from zero
		index = self.rows*(r)+c
		self.frame[index] = Frame(self.roots,width=self.width,height=self.height,bg=color)
		self.frame[index].pack_propagate(0)
		self.box[index] = Label(self.frame[index], text=index, borderwidth=5, background=color, width = self.width, height = self.height , fg = "grey", font=("Courier", math.ceil(self.height/2)))
		self.box[index].pack(fill="both", expand=True,side='left')
		self.frame[index].place(x=(c)*self.width,y=(r)*self.height)
		self.roots.pack(fill = "both", expand = True)
	

	## HELPER FUNCTION TO CHECK IF A NODE WAS VISITED
	def wasAlreadyVisited(self,xIndex,yIndex,visitVal):
		if(self.mapstate[xIndex,yIndex]!=visitVal):
			return True;
		else:
			return False

	## HELPER FUNCTION FOR DFS TO PUSH THE NEIGHBOURS THAT WERE NOT VISITED AND ARE NOT BLOCKED
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

	## DEPTH FIRST SEARCH IMPLEMENTATION USING LIST AS A STACK
	def depthFirstSearch(self):
		s = time.time()
		self.fringe = []
		# self.pathMap[[0,0]] = [-1,-1]
		self.fringe.append([0,0])
		self.pathMap[(0,0)] = [-1,-1]
		
		while(len(self.fringe)>0):
			element = self.fringe.pop()
			if(element[0]==self.rows-1 and element[1] == self.columns-1):
				self.mapstate[element[0],element[1]] = 2;
				self.update_the_maze_simple(element[0],element[1])
				while(self.pathMap[(element[0],element[1])]!=[-1,-1]):
					x,y = self.pathMap[(element[0],element[1])]
					element = (x,y)
					self.mapstate[x,y] = 2;
					self.update_the_maze_simple(x,y)										

				break;
			self.fringe,self.pathMap = self.pushNeighboursIfNotVisited(element[0],element[1],self.fringe,self.pathMap,3)
			self.mapstate[element[0],element[1]] = 3;
			self.update_the_maze_simple(element[0],element[1])
		print("DFS %s", time.time()-s)

	## BREADTH FIRST SEARCH USING LIST AS A QUEUE
	def breadthFirstSearch(self):   
		s = time.time()
		self.q = deque()
		self.q.append((0, 0))
		self.visited = []
		self.max_rows, self.max_cols = self.rows, self.columns
		while(len(self.q) > 0):
			self.x, self.y = self.q.popleft()        
			if((self.rows-1,self.columns-1) in self.visited):
				break
			self.visited.append((self.x, self.y))
			# if(self.x, self.y is self.rows-1, self.columns-1):
			#     break
			self.mapstate[self.x, self.y] = 3
			self.update_the_maze_simple(self.x, self.y)
			for coord in [(self.x + 1, self.y), (self.x, self.y + 1), (self.x - 1, self.y), (self.x, self.y - 1)]:
				if coord not in self.q and coord not in self.visited:
					a, b = coord
					if a >= 0 and b >= 0 and a < self.rows and b < self.columns:
						if self.mapstate[a, b]!=0:
							self.q.append(coord)
		if (self.rows-1, self.columns-1) in self.visited:         
			traced = []
			self.x1, self.y1 = self.rows-1, self.columns-1
			self.mapstate[self.x1, self.y1] = 2
			self.update_the_maze_simple(self.x1, self.y1)
			traced.append((self.x1, self.y1))
			while((0, 0) not in traced):
				neighbours = [(self.x1 + 1, self.y1), (self.x1, self.y1 + 1), (self.x1 - 1, self.y1), (self.x1, self.y1 - 1)]
				ind = []
				act_neighbours = []
				for next in neighbours:
					if next in self.visited:
						act_neighbours.append(next)
						ind.append(self.visited.index(next))
				self.x1, self.y1 = act_neighbours[ind.index(min(ind))]
				self.mapstate[self.x1, self.y1] = 2
				self.update_the_maze_simple(self.x1, self.y1)
				traced.append((self.x1, self.y1))
			print(traced)
		print(self.visited)
		print("BFS %s", time.time()-s)
	
	
	## IMPLEMENTATION START FOR A* ALGORITHM



	def a_star_euc(self):
		# Function: A* algorithm with the heuristic, the Euclidean Distance
		s = time.time()
		self.a_star("euc")
		print("euc %s", time.time()-s)
	def a_star_man(self):
		# Function: A* algorithm with the heuristic, the Manhattan Distance
		s = time.time()
		self.a_star("man")
		print("man %s", time.time()-s)
	def a_star(self, heuristic):
		fstate = np.ones((self.rows, self.columns))
		fstate = fstate*(math.pow(2,15)-1)       
		w = self.rows
		h = self.columns
		class node():
			# the node is a data structure, containing n, which is the location of the node, and p, which is the location of the node's parent
			def __init__(self, px, py, x, y):
				self.n = [x,y]
				self.p = [px,py]
		class aListWithState():
			# aListWithState is a list of "nodes" 
			def __init__(self):
				self.list = []
			def add(self, px, py, x, y, f):
				n = node(px, py, x, y)
				self.list.append(n)
				fstate[x,y] = f
			def popMin(self):
				# this method will output the node with smallest f
				# f is the predicted cost of the node 
				# f = g + h 
				fs = []
				for node in self.list:
					x, y = node.n
					fs.append(fstate[x,y])
				index = fs.index(min(fs))
				node = self.list.pop(index)
				return node.n, node.p

		def get_the_f(qx, qy, x, y):
			return get_the_g(qx, qy, x, y)+get_the_h(x,y)
		def get_the_g(qx, qy, x, y):  
			return distance(qx, qy, x, y)
		def get_the_h(x, y):
			return distance(x, y, w-1, h-1)
		def distance(qx, qy, x, y):
			if "man" in heuristic:
				return manhattan_distance(qx, qy, x, y)
			elif "euc" in heuristic:
				return euclidean_distance(qx, qy, x, y)
			else:
				return False

		def manhattan_distance(qx, qy, x, y):
			xD = math.fabs(qx-x)
			yD = math.fabs(qy-y)
			return xD+yD

		def euclidean_distance(qx, qy, x, y):
			xD2 = math.pow(qx-x,2)
			yD2 = math.pow(qy-y,2)
			return math.pow(xD2+yD2,1/2)
		
		def best_route(theList):
			nList = []
			pList = []
			bestRoute = []
			for node in theList:
			    nList.append(node.n)
			    pList.append(node.p)
			n = nList.pop()
			oldP = pList.pop()
			bestRoute.insert(0,n)
			while len(nList)>0:
			    while oldP!=n and len(nList)>0:
			        n = nList.pop()
			        p = pList.pop() 
			    bestRoute.insert(0,n)
			    oldP = p
			for node in bestRoute:
				x,y = node
				self.mapstate[x,y] = 2
				self.update_the_maze_simple(x,y)
				print(node)
			return bestRoute
		# openlist will be the list of nodes, the A* algorithm are insterested in, but did not visit, yet.
		# closedlist will be the list of nodes, the A* algorithm has visited
		openList = aListWithState()
		closedList = aListWithState()
		openList.add(-1, -1, 0, 0, 0)
		self.fringe = []
		self.fringe.append([0,0])

		while(len(openList.list)>0):
			q, parents = openList.popMin()
			qx, qy = q
			pqx, pqy = parents
			d = [(qx - 1, qy), (qx, qy + 1), (qx + 1, qy), (qx, qy - 1)]
			shuffle(d)
			for (xx, yy) in d:
				if xx==w-1 and yy==h-1:
					closedList.add(pqx,pqy,qx,qy,fstate[qx,qy])
					self.fringe.append([qx,qy])
					self.mapstate[qx,qy] = 3
					self.update_the_maze_simple(qx,qy)
					closedList.add(qx,qy,xx,yy,fstate[qx,qy])
					self.fringe.append([xx,yy])
					self.mapstate[xx,yy] = 3
					self.update_the_maze_simple(xx,yy)
					print("A* algorithm completed!")
					return best_route(closedList.list)
				if xx<0 or xx>=w or yy<0 or yy>=h:
					continue
				if self.mapstate[xx,yy]==0:
					continue
				f = get_the_f( qx, qy, xx, yy)
				if fstate[xx,yy] <= f:
					continue
				else:
					fstate[xx,yy] = f
				if [xx,yy] in openList.list:
					continue
				openList.add(qx,qy,xx,yy,f)
			closedList.add(pqx,pqy,qx,qy,fstate[qx,qy])
			self.fringe.append([qx,qy])
			self.mapstate[qx,qy] = 3
			self.update_the_maze_simple(qx,qy)


		print("A* algorithm failed!")
		closedList.add(pqx,pqy,qx,qy,fstate[qx,qy])
		self.fringe.append([qx,qy])
		self.mapstate[qx,qy] = 3
		self.update_the_maze_simple(qx,qy)
		return False            
	
	## IMPLEMENTATION END FOR A* ALGORITHM


	## IMPLEMENTATION FOR BI-DIRECTIONAL BREADTH-FIRST SEARCH
	def bi_directional_BFS(self):
		self.fringe = []
		self.fringe.append([0,0])
		
		pathMapFromStart = {}
		pathMapFromStart[(0,0)] = [-1,-1]

		## PARENT MAP TO TRACK THE PATH TO GOAL
		pathMapFromGoal = {}
		pathMapFromGoal[(self.rows-1,self.columns-1)] = [-1,-1]
		## QUEUE FROM GOAL NODE
		reverseFringe = []  
		reverseFringe.append([self.rows-1,self.columns-1])
		
		## started by pushing the first node in the fringe
		while(len(self.fringe)>0 and len(reverseFringe)>0):
			element = self.fringe[0]
			self.fringe.remove(element)
			elementFromGoal = reverseFringe[0]
			reverseFringe.remove(elementFromGoal)

			if(self.mapstate[element[0],element[1]]==4):
				elementFromGoal = copy.copy(element)
				self.mapstate[element[0],element[1]]=2
				self.update_the_maze_simple(element[0],element[1])

				## GENERATION OF THE PATH FOR BI-BFS
				while(pathMapFromStart[element[0],element[1]]!=[-1,-1]):
					x,y = pathMapFromStart[element[0],element[1]]
					element = (x,y)
					self.mapstate[x,y] = 2
					self.update_the_maze_simple(x,y)
				
				while(pathMapFromGoal[elementFromGoal[0],elementFromGoal[1]]!=[-1,-1]):
					x,y = pathMapFromGoal[elementFromGoal[0],elementFromGoal[1]]
					elementFromGoal = (x,y)
					self.mapstate[x,y] = 2
					self.update_the_maze_simple(x,y)
				break;
			
			self.fringe,pathMapFromStart = self.pushNeighboursIfNotVisited(element[0],element[1],self.fringe,pathMapFromStart,3)
			reverseFringe,pathMapFromGoal = self.pushNeighboursIfNotVisited(elementFromGoal[0],elementFromGoal[1],reverseFringe,pathMapFromGoal,4)
			self.mapstate[element[0],element[1]] = 3;
			self.update_the_maze_simple(element[0],element[1])
			self.mapstate[elementFromGoal[0],elementFromGoal[1]] = 4
			self.update_the_maze_simple(elementFromGoal[0],elementFromGoal[1])
	
	## RESET BUTTON USED TO UPDATE THE UI
	def resetButton(self):
		# print(self.mapstate)
		for r in range(0, self.rows):
			for c in range(0, self.columns):
				if self.mapstate[r,c] != self.mapstateCopy[r,c]:
					self.mapstate[r,c] = self.mapstateCopy[r,c]
					self.update_the_maze_simple(r,c)			


## START OF THE MAIN CODE
def main():
	maze = theMaze(20, 20)
	maze.root.mainloop()

if __name__ == '__main__':
	main()