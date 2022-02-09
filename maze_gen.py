from tkinter import *
from tkinter import filedialog
import random
import time
import threading
from PIL import ImageGrab


class Cell:
    visited = False
    bd = 1

    def __init__(self, canvas, row, col, size, color1, color2):
        self.canvas:Canvas = canvas
        self.r = row
        self.c = col
        self.s = size
        self.c1 = color1
        self.c2 = color2

    def draw(self):
        x0 = self.c*self.s
        y0 = self.r*self.s
        x1 = (self.c+1)*self.s
        y1 = (self.r+1)*self.s
        self.shape = self.canvas.create_rectangle(x0, y0, x1, y1, width=0, fill=self.c2)
        self.n = self.canvas.create_line(x0, y0, x1, y0, width=self.bd, fill=self.c1)
        self.s = self.canvas.create_line(x0, y1, x1, y1, width=self.bd, fill=self.c1)
        self.e = self.canvas.create_line(x1, y0, x1, y1, width=self.bd, fill=self.c1)
        self.w = self.canvas.create_line(x0, y0, x0, y1, width=self.bd, fill=self.c1)

    def erase_wall(self, wall):
        if wall is N: self.canvas.itemconfig(self.n, state=HIDDEN)
        elif wall is S: self.canvas.itemconfig(self.s, state=HIDDEN)
        elif wall is E: self.canvas.itemconfig(self.e, state=HIDDEN)
        elif wall is W: self.canvas.itemconfig(self.w, state=HIDDEN)
        else: print(f"[INVALID WALL OPTION:{wall}]")
    
    def changecolor(self, color):
        self.c2 = color
        self.canvas.itemconfig(self.shape, fill=self.c2)

class Tracker:
    r = 0
    c = 0
    def __init__(self, canvas, rows, cols, size, color):
        self.canvas:Canvas = canvas
        self.rows = rows
        self.cols = cols
        self.size = size
        self.col = color
    
    def draw(self):
        self.shape = self.canvas.create_rectangle(self.c+Cell.bd//2, self.r+Cell.bd//2, (self.c+1)*self.size-Cell.bd//2, (self.r+1)*self.size-Cell.bd//2, width=0, fill=self.col)
    
    def hide(self):
        self.canvas.itemconfig(self.shape, state=HIDDEN)
    
    def show(self):
        self.canvas.itemconfig(self.shape, state=NORMAL)
    
    def move(self, dx=None, dy=None):
        dx = 0 if dx is None else (self.size*dx)
        dy = 0 if dy is None else (self.size*dy)
        self.canvas.move(self.shape, dx, dy)
        self.r += dy
        self.c += dx
        return self.r, self.c


ROWS = 20
COLS = 30
SIZE = 20

REST = 0.05

COLOR0 = 'grey'
COLOR1 = 'black'
COLOR2 = 'dark grey'
COLOR3 = 'white'

PROCESS = None
TERMINATE_PROCESS = False

grid:list[list[Cell]] = []
stack:list[tuple[int, int]] = []

root = Tk()
root.title("Maze Gen")
root.config(bg='pink')
root.geometry("+20+20")

body = Frame(root, bg=COLOR1)
body.pack(padx=10, pady=10)

canvas = Canvas(body, width=COLS*SIZE, height=ROWS*SIZE, bg='white', highlightthickness=0)
canvas.pack(padx=3, pady=3)


def draw(r, c):
    global grid, canvas
    for i in range(r):
        dg = []
        for j in range(c):
            z = Cell(canvas, i, j, SIZE, COLOR1, COLOR2)
            z.draw()
            dg.append(z)
        grid.append(dg)

def refresh():
    global root
    root.update_idletasks()
    time.sleep(REST)

def getneighbours(r, c):
    n = []
    if (r-1) in range(ROWS):
        if not grid[r-1][c].visited: n.append((-1, 0, N))
    if (r+1) in range(ROWS):
        if not grid[r+1][c].visited: n.append((+1, 0, S))
    if (c-1) in range(COLS):
        if not grid[r][c-1].visited: n.append((0, -1, W))
    if (c+1) in range(COLS):
        if not grid[r][c+1].visited: n.append((0, +1, E))
    return n

def erasewall(r, c, wall):
    global canvas, grid
    if wall==N:
        grid[r][c].erase_wall(N)
        if (r-1) in range(ROWS): grid[r-1][c].erase_wall(S)
    elif wall==S:
        grid[r][c].erase_wall(S)
        if (r+1) in range(ROWS): grid[r+1][c].erase_wall(N)
    elif wall==E:
        grid[r][c].erase_wall(E)
        if (c+1) in range(COLS): grid[r][c+1].erase_wall(W)
    elif wall==W:
        grid[r][c].erase_wall(W)
        if (c-1) in range(COLS): grid[r][c-1].erase_wall(E)
    else: print(f"[INVALID WALL OPTION:{wall}]")

def __start__():
    global grid, stack, ROWS, COLS, TERMINATE_PROCESS, PROCESS, TRACKER
    r, c = 0, 0
    TRACKER.show()
    while True:
        grid[r][c].visited = True
        grid[r][c].changecolor(COLOR3)
        neighbour = getneighbours(r, c)

        if TERMINATE_PROCESS: break
        if not neighbour:
            if r==0 and c==0:
                print("[FINISHED]")
                break
            else:
                r0, c0 = stack.pop()
                TRACKER.move(-c0, -r0)
                r -= r0
                c -= c0
                refresh()
                continue

        dr, dc, dn = random.choice(neighbour)
        erasewall(r, c, dn)
        stack.append((dr, dc))
        r += dr
        c += dc
        TRACKER.move(dc, dr)
        refresh()
    TRACKER.hide()
    kill()

def start():
    global PROCESS, start_button
    start_button.config(text='stop', command=kill)
    PROCESS = threading.Thread(target=__start__)
    PROCESS.start()

def kill():
    global TERMINATE_PROCESS, start_button
    TERMINATE_PROCESS = True
    start_button.destroy()

def end():
    global PROCESS, TERMINATE_PROCESS
    try:
        if PROCESS.is_alive():
            print("Press stop button before exit")
            return None
    except: pass
    try:kill()
    except: pass
    TERMINATE_PROCESS = True
    if PROCESS is not None: PROCESS.join()
    try: print("threading alive?:",PROCESS.is_alive())
    except: pass
    root.destroy()

def save():
    global canvas, body
    x0 = body.winfo_rootx()
    y0 = body.winfo_rooty()
    x1 = x0 + body.winfo_width()
    y1 = y0 + body.winfo_height()
    print(x0, y0, x1, y1)
    filepath = filedialog.asksaveasfilename(filetypes=(('png files', '*.png'), ('jpeg files', '*.jpg'), ('jpg files', '*.jpg')))
    if filepath:
        try:
            ImageGrab.grab().crop((x0,y0,x1,y1)).save(filepath)
            print(f"[SAVED] {filepath}")
        except ValueError:
            print("[MISSING EXTENSION]")
        except Exception as e:
            print(f"[ERROR] {e}")


draw(ROWS, COLS)

TRACKER = Tracker(canvas, ROWS, COLS, SIZE, COLOR0)
TRACKER.draw()
TRACKER.hide()

panel = Frame(root, bg='grey')
panel.pack(padx=10, pady=10, fill=BOTH)

start_button = Button(panel, text="Start", width=6, border=3, command=start)
start_button.pack(padx=5, pady=5, side=LEFT)

save_button = Button(panel, text='Save', width=6, border=3, command=save)
save_button.pack(padx=5, pady=5, side=LEFT)

root.protocol("WM_DELETE_WINDOW", end)
root.mainloop()
