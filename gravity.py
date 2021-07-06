from os import system
from win32api import GetAsyncKeyState as keypress
from win32con import *
import time as tm
from copy import deepcopy

block = {'p' : '©', 's' : ' ', 'l' : '░', 'm' : '▒', 'd' : '▓', 'b' : '█'}
arrow = {'left':0x25, 'up':0x26, 'right':0x27, 'down':0x28}

height= 401
width = 33
sectionwidth = 33
sectionheight = 37
sectionposX = 0
sectionposY = 0

player = {'x' : 5, 'y' : height-2, 'shape' : block['p']}

gamearea = []

def reset():
    global gamearea, height, width, block
    gamearea.clear()
    for y in range(height):
        newline = []
        for x in range(width):
            if y == 0 or y == height-1 or x == 0 or x == width-1:
                newline.append(block['b'])
            elif y%12 == 0 and x <= width/7:
                newline.append(block['b'])
            elif (y%12 == 2 or y%12 == 10) and x >= width*2/7 and x <= width*3/7:
                newline.append(block['b'])
            elif (y%12 == 4 or y%12 == 8) and x >= width*4/7 and x <= width*5/7:
                newline.append(block['b'])
            elif y%12 == 6 and x >= width*6/7:
                newline.append(block['b'])
            # elif y%4 == 0 or x%4 == 0:
            #     newline.append(block['m'])
            # elif y%2 == 0 and x%2 == 0:
            #     newline.append(block['l'])
            else:
                newline.append(block['s'])
        gamearea.append(newline)

def putplayer(x,y):
    global displayarea, player
    displayarea[y][x] = player['shape']

def gotoxy(x,y):
    print("%c[%d;%df" % (0x1B, y, x), end='')

def fulldisplay():
    global height, width, displayarea
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

def moveplayer(direction='', distance=1):
    global displayarea, gamearea, player, height, width, block, jumping, jumped
    displayarea[player['y']][player['x']] = gamearea[player['y']][player['x']]
    
    #up, down, left and right
    if direction == 'up' and displayarea[player['y'] - distance][player['x']] != block['b']:
        if player['y'] > 0:
            player['y'] -= distance
        else: 
            player['y'] = height-1
    if direction == 'down' and displayarea[player['y'] + distance][player['x']] != block['b']:
        if player['y'] < height-1:
            player['y'] += distance
        else: 
            player['y'] = 0
    if direction == 'left' and displayarea[player['y']][player['x'] - distance] != block['b']:
        if player['x'] > 0:
            player['x'] -= distance
        else: 
            player['x'] = width-1
    if direction == 'right' and displayarea[player['y']][player['x'] + distance] != block['b']:
        if player['x'] < width-1:
            player['x'] += distance
        else: 
            player['x'] = 0
    
    #always try to fall
    if displayarea[player['y'] + 1][player['x']] != block['b'] and not jumped:
        player['y'] += 1
    
    
    if direction == 'jump' and (displayarea[player['y'] + 1][player['x']] == block['b'] or displayarea[player['y'] + 1][player['x']-1] == block['b'] or displayarea[player['y'] + 1][player['x']+1] == block['b']):
        jumping = distance
        
    if jumping:
        if displayarea[player['y'] - 1][player['x']] != block['b']:
            jumped = True
            player['y'] -= 1
            jumping -= 1
        else:
            jumping = 0
            jumped = False
    else:
        jumped = False
    displayarea[player['y']][player['x']] = block['p']

def checkmovement():
    global arrow
    if keypress(arrow['left']):
        moveplayer('left', 1)
    if keypress(arrow['right']):
        moveplayer('right', 1)
    if keypress(arrow['up']):
        moveplayer('up', 1)
    if keypress(arrow['down']):
        moveplayer('down', 1)
    if keypress(VK_SPACE):
        moveplayer('jump', 7)
    moveplayer()

def checkplacement():
    global gamearea, displayarea, player, block
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
jumping = 0
jumped = False
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
    tm.sleep(0.05)
input()













