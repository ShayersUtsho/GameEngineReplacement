from os import system
from win32api import GetAsyncKeyState as keypress
from win32con import *
import time as tm
from copy import deepcopy

block = {'p' : '©', 's' : ' ', 'l' : '░', 'm' : '▒', 'd' : '▓', 'b' : '█'}
arrow = {'left':0x25, 'up':0x26, 'right':0x27, 'down':0x28}

height= 9
width = 9
depth = 9

player = {'x' : int(width/2), 'y' : int(height/2), 'z' : int(depth/2), 'shape' : block['p']}

gamearea = []

def reset():
    gamearea.clear()
    for z in range(depth):
        newlayer = []
        for y in range(height):
            newline = []
            for x in range(width):
                if y == 0 or y == height-1 or x == 0 or x == width-1 or z == 0 or z == depth-1:
                    newline.append(block['b'])
                elif (z%4 == 0 and y%4 == 0) or (z%4 == 0 and x%4 == 0) or (x%4 == 0 and y%4 == 0):
                    newline.append(block['m'])
                elif z%2 == 0 and y%2 == 0 and x%2 == 0:
                    newline.append(block['l'])
                else:
                    newline.append(block['s'])
            newlayer.append(newline)
        gamearea.append(newlayer)

def putplayer(x,y,z):
    displayarea[z][y][x] = player['shape']

def gotoxy(x,y):
    print("%c[%d;%df" % (0x1B, y, x), end='')

def threedisplay():
    for y in range(height):
        for x in range(width):
            gotoxy(x+1,y+1)
            print(displayarea[player['z']][y][x], end='')
        print('')
    for z in range(depth):
        for y in range(height):
            gotoxy(width+y+2,z+1)
            print(displayarea[z][height-y-1][player['x']], end='')
        print('')
    for z in range(depth):
        for x in range(height):
            gotoxy(2*width+x+3,z+1)
            print(displayarea[z][player['y']][x], end='')
        print('')
        
def fulldisplay():
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                gotoxy((z%depth)*(width+1)+x+1, int(z/depth)*(height+1)+y+1)
                print(displayarea[z][y][x], end='')
            print('')

def moveplayer(direction, distance):
    displayarea[player['z']][player['y']][player['x']] = gamearea[player['z']][player['y']][player['x']]
    if direction == 'up':
        if player['y'] > 0:
            player['y'] -= distance
        else: 
            player['y'] = height-1
    elif direction == 'down':
        if player['y'] < height-1:
            player['y'] += distance
        else: 
            player['y'] = 0
    elif direction == 'left':
        if player['x'] > 0:
            player['x'] -= distance
        else: 
            player['x'] = width-1
    elif direction == 'right':
        if player['x'] < width-1:
            player['x'] += distance
        else: 
            player['x'] = 0
    elif direction == 'shallow':
        if player['z'] > 0:
            player['z'] -= distance
        else: 
            player['z'] = width-1
    elif direction == 'deep':
        if player['z'] < width-1:
            player['z'] += distance
        else: 
            player['z'] = 0
    else:
        pass
    displayarea[player['z']][player['y']][player['x']] = block['p']

def checkmovement():
    if keypress(arrow['left']):
        moveplayer('left', 1)
    if keypress(arrow['right']):
        moveplayer('right', 1)
    if keypress(arrow['up']):
        moveplayer('up', 1)
    if keypress(arrow['down']):
        moveplayer('down', 1)
    if keypress(VK_SPACE):
        moveplayer('shallow', 1)
    if keypress(VK_SHIFT):
        moveplayer('deep', 1)

def checkplacement():
    if keypress(ord('Q')):
        gamearea[player['z']][player['y']][player['x']] = block['s']
        displayarea[player['z']][player['y']][player['x']] = block['s']
    if keypress(ord('W')):
        gamearea[player['z']][player['y']][player['x']] = block['l']
        displayarea[player['z']][player['y']][player['x']] = block['l']
    if keypress(ord('E')):
        gamearea[player['z']][player['y']][player['x']] = block['m']
        displayarea[player['z']][player['y']][player['x']] = block['m']
    if keypress(ord('R')):
        gamearea[player['z']][player['y']][player['x']] = block['d']
        displayarea[player['z']][player['y']][player['x']] = block['d']
    if keypress(ord('T')):
        gamearea[player['z']][player['y']][player['x']] = block['b']
        displayarea[player['z']][player['y']][player['x']] = block['b']

reset()
displayarea = deepcopy(gamearea)
putplayer(player['x'],player['y'],player['z'])
full = False
while 1:
    system('cls')
    checkmovement()
    checkplacement()
    if keypress(ord('F')):
        full = not full
    if full:
        fulldisplay()
    else:
        threedisplay()
    tm.sleep(0.1)
input()
