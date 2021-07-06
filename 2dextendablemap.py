from os import system
from win32api import GetAsyncKeyState as keypress
from win32con import *
import time as tm
from copy import deepcopy

block = {'p' : '©', 's' : ' ', 'l' : '░', 'm' : '▒', 'd' : '▓', 'b' : '█'}
arrow = {'left':0x25, 'up':0x26, 'right':0x27, 'down':0x28}

height= 401
width = 401
sectionwidth = 121
sectionheight = 37
sectionposX = 0
sectionposY = 0

player = {'x' : 5, 'y' : height-2, 'shape' : block['p']}

gamearea = []

def reset():
    gamearea.clear()
    for y in range(height):
        newline = []
        for x in range(width):
            if y == 0 or y == height-1 or x == 0 or x == width-1:
                newline.append(block['b'])
            elif y%4 == 0 or x%4 == 0:
                newline.append(block['m'])
            elif y%2 == 0 and x%2 == 0:
                newline.append(block['l'])
            else:
                newline.append(block['s'])
        gamearea.append(newline)

def putplayer(x,y):
    displayarea[y][x] = player['shape']

def gotoxy(x,y):
    print("%c[%d;%df" % (0x1B, y, x), end='')

def fulldisplay():
    for y in range(height):
        for x in range(width):
            gotoxy(x+1,y+1)
            print(displayarea[y][x], end='')
        print('')

def sectiondisplay():
    if player['x'] < sectionwidth/2:
        sectionposX = 0
    elif player['x'] > width-sectionwidth/2:
        sectionposX = width - sectionwidth
    else:
        sectionposX = player['x'] - int(sectionwidth/2)
        
    if player['y'] < sectionheight/2:
        sectionposY = 0
    elif player['y'] > height-sectionheight/2:
        sectionposY = height - sectionheight
    else:
        sectionposY = player['y'] - int(sectionheight/2)
    
    for y in range(sectionheight):
        for x in range(sectionwidth):
            gotoxy(x+1,y+1)
            print(displayarea[sectionposY+y][sectionposX+x], end='')
        print('')

def moveplayer(direction, distance):
    displayarea[player['y']][player['x']] = gamearea[player['y']][player['x']]
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
    else:
        pass
    displayarea[player['y']][player['x']] = block['p']

def checkmovement():
    if keypress(arrow['left']):
        moveplayer('left', 1)
    if keypress(arrow['right']):
        moveplayer('right', 1)
    if keypress(arrow['up']):
        moveplayer('up', 1)
    if keypress(arrow['down']):
        moveplayer('down', 1)

def checkplacement():
    if keypress(ord('Q')):
        gamearea[player['y']][player['x']] = block['s']
        displayarea[player['y']][player['x']] = block['s']
    if keypress(ord('W')):
        gamearea[player['y']][player['x']] = block['l']
        displayarea[player['y']][player['x']] = block['l']
    if keypress(ord('E')):
        gamearea[player['y']][player['x']] = block['m']
        displayarea[player['y']][player['x']] = block['m']
    if keypress(ord('R')):
        gamearea[player['y']][player['x']] = block['d']
        displayarea[player['y']][player['x']] = block['d']
    if keypress(ord('T')):
        gamearea[player['y']][player['x']] = block['b']
        displayarea[player['y']][player['x']] = block['b']

reset()
displayarea = deepcopy(gamearea)
putplayer(player['x'],player['y'])
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
        sectiondisplay()
    tm.sleep(0.1)
input()















