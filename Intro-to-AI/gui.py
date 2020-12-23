from tkinter import *
import math
import random
randints = []
for x in range(20):
    randints.append(random.randint(1,99))

print(randints)
root = Tk()
box = dict()
width = math.ceil(1000/20) #root.winfo_screenwidth()
height = math.ceil(1000/20) # root.winfo_screenheight()
roots = Canvas(root, height = 6*height, width = 6* width, bg="#666666", highlightthickness=0, bd = 0)
frame = {}

for r in range(1, 11):     
    for c in range(1, 11):
        
        frame[10*(r-1)+c] = Frame(roots,width=width,height=height,bg="white")
        frame[10*(r-1)+c].pack_propagate(0)
        # if()
        box[10*(r-1)+c] = Label(frame[10*(r-1)+c], text=10*(r-1)+c, borderwidth=10, background="white", width = width, height = height , fg = "grey", font=("Courier", 19))

        box[10*(r-1)+c].pack(fill="both", expand=True,side='left')
        frame[10*(r-1)+c].place(x=(c-1)*width,y=(r-1)*height)
     
roots.pack(fill = "both", expand = True)

root.title("AI Maze")
root.mainloop() 