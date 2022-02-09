from tkinter import *
import threading
import random
import time

class Blocks:
    def __init__(self, canvas, count, x, y, height, width, color):
        self.canvas:Canvas = canvas
        self.count = count
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.color = color
        self.temp = ""
    
    def draw(self):
        self.x0 = self.x
        self.y0 = self.y - self.height
        self.x1 = self.x + self.width
        self.y1 = self.y
        self.shape = self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, width=0, fill=self.color)
    
    def select(self, color):
        self.temp = color
        self.canvas.itemconfig(self.shape, fill=self.temp)
    
    def deselect(self):
        self.canvas.itemconfig(self.shape, fill=self.color)
    
    def move(self, dx, dy=0):
        self.canvas.move(self.shape, dx, dy)


WIDTH = 600
HEIGHT = 400

BLOCK = 'green'
SELECT1 = 'yellow'
SELECT2 = 'red'

BHEIGHT = 24
BWIDTH = 20

COUNT = 10
SHUFFLE_ITER = 50
SHUFFLE_REST = 0.1
SORT_REST = 0.1

SHUFFLE_PROCESS = None
SORT_PROCESS = None

IX = (WIDTH - (2*COUNT-1)*BWIDTH)/2
IY = int(HEIGHT*0.9)


def refresh(rest=0):
    global root
    root.update_idletasks()
    if rest: time.sleep(rest)

def select(index, color):
    global blocks, array
    blocks[array[index]].select(color)

def deselect(index):
    global blocks, array
    blocks[array[index]].deselect()

def disable():
    global button_shuffle, button_sort
    button_shuffle.config(state=DISABLED, bg='pink')
    button_sort.config(state=DISABLED, bg='pink')

def enable():
    global button_shuffle, button_sort
    button_shuffle.config(state=NORMAL, bg='white')
    button_sort.config(state=NORMAL, bg='white')

def swap(x, y):
    """y>x"""
    if x>y: x, y = y, x
    blocks[array[x]].move(BWIDTH*2*(y-x))
    blocks[array[y]].move(BWIDTH*2*(x-y))
    array[x], array[y] = array[y], array[x]

def __shuffle__():
    global SHUFFLE_PROCESS
    for _ in range(SHUFFLE_ITER):
        x, y = 0, 0
        while x==y:
            x = random.randint(0, COUNT-1)
            y = random.randint(0, COUNT-1)
        select(x, SELECT1)
        refresh(SHUFFLE_REST)
        select(y, SELECT2)
        refresh(SHUFFLE_REST)
        swap(x, y)
        deselect(x)
        deselect(y)
        refresh(SHUFFLE_REST)
    print("[DONE]")
    enable()
    SHUFFLE_PROCESS = None

def __sort__():
    global SORT_PROCESS
    i = 0
    while True:
        select(i, SELECT1)
        refresh(SORT_REST)
        select(i+1, SELECT2)
        refresh(SORT_REST)
        if array[i]>array[i+1]:
            swap(i, i+1)
            refresh(SORT_REST)
            deselect(i)
            refresh(SORT_REST)
            deselect(i+1)
            refresh(SORT_REST)
            i = 0
        else:
            deselect(i)
            refresh(SORT_REST)
            deselect(i+1)
            refresh(SORT_REST)
            i += 1
        refresh(SORT_REST)
        if i+1==COUNT: break
    print("[DONE]")
    enable()
    SORT_PROCESS = None
        

def shuffle():
    global SHUFFLE_PROCESS
    disable()
    print("[SHUFFLING]")
    SHUFFLE_PROCESS = threading.Thread(target=__shuffle__)
    SHUFFLE_PROCESS.start()

def sort():
    disable()
    print("[SORTING]")
    SORT_PROCESS = threading.Thread(target=__sort__)
    SORT_PROCESS.start()

root = Tk()
root.title("sort")
root.config(bg='grey')

canvas = Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0, bg='#ffffff')
canvas.pack(padx=10, pady=10)

blocks:list[Blocks] = []
array = [x for x in range(COUNT)]

for i in range(COUNT):
    b = Blocks(canvas, i+1, IX+(BWIDTH*i*2), IY, (i+1)*BHEIGHT, BWIDTH, BLOCK)
    b.draw()
    blocks.append(b)
canvas.create_line(0, IY, WIDTH, IY, width=10)

panel = Frame(root, bg='light grey')
panel.pack(fill=BOTH, padx=10, pady=(0, 10))

button_shuffle = Button(panel, text='shuffle', bg='light grey', width=10, border=3, command=shuffle)
button_shuffle.pack(padx=5, pady=5, side=LEFT)

button_sort = Button(panel, text='sort', bg='light grey', width=10, border=3, command=sort)
button_sort.pack(padx=5, pady=5, side=LEFT)


root.mainloop()