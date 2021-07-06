from os import system

block = {'p' : '©', 's' : ' ', 'l' : '░', 'm' : '▒', 'd' : '▓', 'b' : '█'}

height = 31
width = 31

def coord(x, y):
    return y*width + x

def change(val, string, i):
    temp = list(string)
    temp[i] = val
    string = ''.join(temp)

def gotoxy(x,y):
    print("%c[%d;%df" % (0x1B, y, x), end='')

def display2d():
    global board
    for y in range(height):
        for x in range(width):
            print(block[board[y][x]], end='')
        print('')

def findplayer():
    global board
    for y in range(height):
        for x in range(width):
            if block[board[y][x]] == 'p':
                change('s', board, coord(x, y))
                return [x, y]
                break

def make2d(board1):
    boardx = []
    for y in range(height):
        newline = []
        for x in range(width):
            character = board1[coord(x,y)]
            newline.append(character)
        boardx.append(newline)
    return boardx

for i in range(15):
    system('cls')
    if i >= 7:
        height = 15
    file = open('level-'+str((i+1)//10)+str((i+1)%10)+'.txt')
    board = make2d(list(file.read()))
    player_coord = findplayer()
    display2d()
    file.close()
    input()















