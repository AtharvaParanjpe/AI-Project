from tkinter import *
import math
import random
import numpy as np
import time
from random import shuffle, randrange

class seeker:
    def __init__(self, m):
        self.mymap = m.mapstate
        print(self.mymap)
        self.locx, self.locy = 1, 1
        self.records = []
        self.record_the_location(self.locx, self.locy)
    def movUp(self):
        if self.locy > 1:
            if self.record_the_location(self.locx, self.locy-1):
                self.locy = self.locy-1
                return True
        return False
    def movDown(self):
        if self.locy < self.mymap.shape[1]:
            if self.record_the_location(self.locx, self.locy+1):
                self.locy = self.locy+1
                return True
        return False
    def movLeft(self):
        if self.locx > 1:
            if self.record_the_location(self.locx-1, self.locy):
                self.locx = self.locx-1
                return True
        return False   
    def movRight(self):
        if self.locx < self.mymap.shape[2]:
            if self.record_the_location(self.locx, self.locy+1):
                self.locy = self.locy+1
                return True
        return False    
    def record_the_location(self, locx, locy):
        index = self.mymap.rows*(locx-1)+locy
        if index not in self.records:
            self.records.append(index)
            return True
            return False
        
class theMaze:
    def __init__( self, rows, columns):
        self.root = Tk()
        self.box = dict()
        self.width = math.ceil(1000/20) #root.winfo_screenwidth()
        self.height = math.ceil(1000/20) # root.winfo_screenheight()
        self.roots = Canvas(self.root, height = 6*self.height, width = 6* self.width, bg="#666666", highlightthickness=0, bd = 0)
        self.rows = rows
        self.columns = columns
        self.frame = {}
        self.mapstate = np.zeros((self.rows, self.columns))
        self.make_complicated_maze()
        self.update_the_whole_maze()
        self.updateImg()
        self.roots.pack(fill = "both", expand = True)
        self.root.title("AI Maze")   

    def updateImg(self):   
        self.root.after(1000, self.updateImg)
    def make_complicated_maze(self):
        w = self.rows
        h = self.columns
        visited = np.zeros((w,h))
        def walk(x, y):
            visited[x,y] = 1
            print(visited)
            d = [(x - 2, y), (x, y + 2), (x + 2, y), (x, y - 2)]
            shuffle(d)             
            for (xx, yy) in d:
                if xx<0 or xx>=w or yy<0 or yy>=h:
                    continue
                if visited[xx,yy]==1:
                    continue
                if xx == x:
                    visited[x,math.floor((y+yy)/2)] = 1
                elif yy == y:
                    visited[math.floor((x+xx)/2),y] = 1
                walk(xx, yy)     
            return visited
        initx = math.floor(randrange(w)/2)*2
        inity = math.floor(randrange(h)/2)*2
        walk(initx, inity)  # 1
        
        self.mapstate=visited
    def make_simple_maze(self, numberOfblocks):
        randints = []
        for x in range(numberOfblocks):
            randints.append(random.randint(1,self.rows*self.columns-2))
        for index in randints:
            print(index)
            # self.drawBox("black", index)
            self.set_state_of_box(0, index)
            self.update_the_maze(index)
    def update_the_maze(self, index):
        c = index%self.rows
        r = math.floor(index/self.rows)
        if self.mapstate[r,c] == 0:
            self.drawBox("black", r, c)
        elif self.mapstate[r,c] == 1:
            self.drawBox("white", r, c)
        else:
            self.drawBox("gray", r, c)
    def update_the_whole_maze(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.mapstate[i,j] == 0:
                    self.drawBox("black", i, j)
                elif self.mapstate[i,j] == 1:
                    self.drawBox("white", i, j)
                else:
                    self.drawBox("gray", i, j)
        self.roots.pack(fill = "both", expand = True)

    def set_state_of_box(self, *args):
        if len(args) == 2:
            self.set_state_of_theId(args[0], args[1])
        if len(args) == 3:
            self.set_state_of_theRC(args[0], args[1], args[2])
    def set_state_of_theId(self, state, index):
        c = index%self.rows
        r = math.floor(index/self.rows)
        self.set_state_of_theRC(state, r, c)       
    def set_state_of_theRC(self, state, r, c):  
        # the r and c both starts from one
        self.mapstate[r,c] = state

    def drawBox(self, *args):
        if len(args) == 2:
            self.drawBoxById(args[0], args[1])
        if len(args) == 3:
            self.drawBoxByRC(args[0], args[1], args[2])
    def drawBoxById(self, color, index):
        c = index%self.rows
        r = math.floor(index/self.rows)
        self.drawBoxByRC(color, r, c)
    def drawBoxByRC(self, color, r,c):
        # the r and c both starts from one
        index = self.rows*(r)+c
        self.frame[index] = Frame(self.roots,width=self.width,height=self.height,bg="white")
        self.frame[index].pack_propagate(0)
        self.box[index] = Label(self.frame[index], text=index, borderwidth=10, background=color, width = self.width, height = self.height , fg = "grey", font=("Courier", 19))
        self.box[index].pack(fill="both", expand=True,side='left')
        self.frame[index].place(x=(c)*self.width,y=(r)*self.height)
        self.roots.pack(fill = "both", expand = True)
        
maze = theMaze(11,11)
maze.root.mainloop()