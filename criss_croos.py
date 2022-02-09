import sys
from tkinter import *
import numpy.random as npr

def draw(width=40, height=40, cell=10, bias=0.5):
    root= Tk()

    canvas = Canvas(root, bg='black', height=height*cell, width=width*cell, highlightthickness=0)
    canvas.pack()

    for i in range(height):
        for j in range(width):
            r = (npr.randint(0, 100))/100
            if r>=bias:
                canvas.create_line(j*cell, i*cell, cell*(j+1), cell*(i+1), width=1, fill='white')
            else:
                canvas.create_line((j+1)*cell, i*cell, j*cell, (i+1)*cell, width=1, fill='white')
    
    
    root.mainloop()

if __name__ == '__main__':
    print(sys.argv)
    draw(50, 40, 20, 0.5)