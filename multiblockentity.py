from os import system
import win32api as win
import time as tm

blocks = {'p' : '©', 's' : ' ', 'l' : '░', 'm' : '▒', 'd' : '▓', 'b' : '█'}
arrow = {'left':0x25, 'up':0x26, 'right':0x27, 'down':0x28}

gamearea = []

interval = 4

player = {(-1,-1):'╔', (0,-1):'┬', (1,-1):'╗',
          (-1,0):'├', (0,0):'┼', (1,0):'┤',
          (-1,1):'╚', (0,1):'┴', (1,1):'╝'}

xmax = int(input("Enter the width of the game area: ")) * interval + 1
ymax = int(input("Enter the width of the game area: ")) * interval + 1

"""
def maximize():
    hOut = GetStdHandle(STD_OUTPUT_HANDLE)
    NewSBSize = GetLargestConsoleWindowSize(hOut)
    DisplayArea = [0, 0, 0, 0]
    SetConsoleScreenBufferSize(hOut, NewSBSize)
    DisplayArea.Right = NewSBSize.X - 1
    DisplayArea.Bottom = NewSBSize.Y - 1
    SetConsoleWindowInfo(hOut, True, DisplayArea)
"""

def newline(y):
    line = []
    for x in range(xmax):
        if x == 0 or x == xmax-1 or y == 0 or y == ymax-1:
            line.append(blocks['b'])
        elif x % interval == 0 and y % interval == 0:
            line.append(blocks['m'])
        elif x % interval == 0 or y % interval == 0:
            line.append(blocks['l'])
        else:
            line.append(blocks['s'])
    return line

def setgame():
    for y in range(ymax):
        gamearea.append(newline(y))

def updategame():
    for y in range(ymax):
        gamearea[y] = newline(y)

i = interval//2
j = interval//2

setgame()

def setplayer(a, b):
    setgame()
    for y in range(-1,2):
        for x in range(-1,2):
            gamearea[b+y][a+x] = player[(x,y)]

while(1):
    system("cls")
    updategame()
    setplayer(i, j)
    for y in range(ymax):
        for x in range(xmax):
            print(gamearea[y][x], end="", sep="")
        print("")
    
    if win.GetAsyncKeyState(arrow['left']):
        i-=1
    if win.GetAsyncKeyState(arrow['right']):
        i+=1
    if win.GetAsyncKeyState(arrow['up']):
        j-=1
    if win.GetAsyncKeyState(arrow['down']):
        j+=1
    tm.sleep(0.1)

