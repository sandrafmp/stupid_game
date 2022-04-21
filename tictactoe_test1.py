import pygame as pg
import sys
import time
import pygame
from pygame.locals import *

### CREATE GRID ###

black = (0, 0, 0)
white = (255, 255, 255)

#red = (255, 0, 0)
red = (0, 0, 255) #blå
WIDTH = 20
HEIGHT = 20
MARGIN = 5
grid = []
for row in range(20):
    grid.append([])
    for column in range(20):
        grid[row].append(0)
grid[1][5] = 0
pygame.init()
window_size = [505, 505]

scr = pygame.display.set_mode(window_size)
pygame.display.set_caption("Grid")
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            grid[row][column] = 1
            print("Click ", pos, "Grid coordinates: ", row, column)
    scr.fill(black)
    for row in range(20):
        for column in range(20):
            color = white
            if grid[row][column] == 1:
                color = red
            pygame.draw.rect(scr,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    clock.tick(50)
    pygame.display.flip()
pygame.quit()