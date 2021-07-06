from win32api import GetAsyncKeyState
from os import system

i = 0
while(1):
    system('cls')
    if i >= 100:
        i = 0
    if i < 20:
        print('1')
    elif i < 40:
        print('10')
    elif i < 60:
        print('100')
    elif i < 80:
        print('1000')
    else:
        print('')
    if GetAsyncKeyState(ord('A')):
        print('A')
    i += 1
