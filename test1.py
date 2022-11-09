from time import sleep
import pygame
from pygame.locals import *
import os
import sys
import random

os.putenv('SDL_FBDEV', '/dev/fb1')

pygame.init()

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

FRAMERATE = 30

BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
WHITE = (255, 255, 255)

GRAIN_SIZE = 5

BOARD_WIDTH = int(SCREEN_WIDTH / GRAIN_SIZE)
BOARD_HEIGHT = int(SCREEN_HEIGHT / GRAIN_SIZE)

lcd = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)

count = 0


def initGameBoard():
    board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    # board[0][0] = ORANGE
    return board

def updateGameBoard(board):
    for y in reversed(range(BOARD_HEIGHT)):
        for x in reversed(range(BOARD_WIDTH)):
            cell = board[y][x]
            if cell != 0:
                if y+1 < BOARD_HEIGHT:
                    if board[y+1][x] == 0:
                        board[y+1][x] = cell
                        board[y][x] = 0
                    else:
                        diags = []
                        if x+1 < BOARD_WIDTH and board[y+1][x+1] == 0 :
                            diags.append(x+1)
                        if x-1 >= 0 and board[y+1][x-1] == 0:
                            diags.append(x-1)
                        
                        if len(diags):
                            ind = 0 if len(diags) == 1 else random.randint(0, 1)
                            x2 = diags[ind]
                            board[y+1][x2] = cell
                            board[y][x] = 0
    return board

def drawGameBoard(board):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            cell = board[y][x]
            if cell != 0:
                pygame.draw.rect(lcd, cell, pygame.Rect(x * GRAIN_SIZE, y * GRAIN_SIZE, GRAIN_SIZE, GRAIN_SIZE))

game_board = initGameBoard()

while True:
    clock.tick(FRAMERATE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        left, middle, right = pygame.mouse.get_pressed()
        if left or middle or right:
            x, y = pygame.mouse.get_pos()
            game_board[int(y / GRAIN_SIZE)][int(x / GRAIN_SIZE)] = ORANGE


    lcd.fill(WHITE)

    game_board = updateGameBoard(game_board)
    drawGameBoard(game_board)

    pygame.display.flip()