###################################
# Python maze generator program with randomic BFS algorithm
# using PyGame for animation
# Parsa Kr
# Python
# 2023-05-01
###################################

import pygame
import time
import random

# set up pygame window
WIDTH = 450
HEIGHT = 500
FPS = 30
# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
RED = (255 ,0 ,0)
YELLOW = (255 ,255 ,0)
GOLD = (255, 215, 0)

# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Generator (BFS)")
clock = pygame.time.Clock()

# setup maze variables
x = 0                    # x axis
y = 0                    # y axis
w = 20                   # width of cell
grid = []
visited = []
queue = []
solution = {}


# build the grid
def build_grid(x, y, w):
    for i in range(1,21):
        x = 20                                                               # set x coordinate to start position
        y = y + 20                                                           # start a new row
        for j in range(1, 21):
                # pygame.draw.line(surface to draw on, color to draw with, start position of the line,  end position of the line)
            
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y], 2)           # top of cell
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w], 2)   # right of cell
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w], 2)   # bottom of cell
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y], 2)           # left of cell
            grid.append((x,y))                                               # add cell to grid list
            x = x + 20                                                       # move cell to new position


def push_up(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y - w + 1, 19, 39), 0)            # draw a rectangle twice the width of the cell
    pygame.display.update()                                                  # to animate the wall being removed


def push_down(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 19, 39), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, BLUE, (x - w + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def single_cell(x, y):
    pygame.draw.rect(screen, GREEN, (x + 1, y + 1, 19, 19), 0)              # draw a single width cell
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 19, 19), 0)               # used to re-colour the path after single_cell
    pygame.display.update()                                                 # has visited cell


def solution_cell(x,y, color):
    pygame.draw.rect(screen, color, (x + 8, y + 8, 10, 10), 0)             # used to show the solution
    pygame.display.update()                                                # has visited cell with tiny rectangle

def solution_line(previous_x, previous_y, x, y):
    pygame.draw.line(screen, RED, [previous_x + 8, previous_y + 12], [x + 8, y + 12], 3)       # used to show the solution
    pygame.display.update()                                                                    # has visited cell with red line

def possible_move(node):
    cell = []                                                                          # define cell list
    if (node[0] + w, node[1]) not in visited and (node[0] + w, node[1]) in grid:       # right cell available?
        cell.append("right")                                                           # if yes add to cell list

    if (node[0] - w, node[1]) not in visited and (node[0] - w, node[1]) in grid:       # left cell available?
        cell.append("left")

    if (node[0] , node[1] + w) not in visited and (node[0] , node[1] + w) in grid:     # down cell available?
        cell.append("down")

    if (node[0], node[1] - w) not in visited and (node[0] , node[1] - w) in grid:      # up cell available?
        cell.append("up")
    return cell
    
def carve_out_maze(x,y):
    single_cell(x, y)                                              # starting positing of maze
    queue.append((x,y))                                            # place starting cell into stack
    visited.append((x,y))                                          # add starting cell to visited list
    while len(queue) > 0:                                          # loop until stack is empty
        time.sleep(.07)                                            # slow program now a bit
        for node in queue:
            cell = possible_move(node)

            if len(cell) > 0:                                          # check to see if cell list is empty
                random.shuffle(cell)                                   # select one of the cell randomly
                for move in cell:
                    if move == "right":                                # if this cell has been chosen
                        push_right(node[0], node[1])                                   # call push_right function
                        single_cell(node[0] + w, node[1])                              # blinking cell with green color (line 125 to 127)
                        time.sleep(.08)
                        backtracking_cell(node[0] + w, node[1])
                        solution[(node[0] + w, node[1])] = node[0], node[1]                 # solution = dictionary key = new cell, other = current cell
                        visited.append((node[0] + w, node[1]))                              # add to visited list
                        queue.append((node[0] + w, node[1]))                                # place current cell on to queue

                    elif move == "left":
                        push_left(node[0], node[1])
                        single_cell(node[0] - w, node[1])
                        time.sleep(.08)
                        backtracking_cell(node[0] - w, node[1])                        
                        solution[(node[0] - w, node[1])] = node[0], node[1]
                        visited.append((node[0] - w, node[1]))
                        queue.append((node[0] - w, node[1]))

                    elif move == "down":
                        push_down(node[0], node[1])
                        single_cell(node[0] , node[1] + w)
                        time.sleep(.08)
                        backtracking_cell(node[0] , node[1] + w)                        
                        solution[(node[0] , node[1] + w)] = node[0], node[1]
                        visited.append((node[0], node[1] + w))
                        queue.append((node[0], node[1] + w))

                    elif move == "up":
                        push_up(node[0], node[1])
                        single_cell(node[0] , node[1] - w)
                        time.sleep(.08)
                        backtracking_cell(node[0] , node[1] - w)                        
                        solution[(node[0] , node[1] - w)] = node[0], node[1]
                        visited.append((node[0], node[1] - w))
                        queue.append((node[0], node[1] - w))
                queue.pop(0)
                #break                                                           # i put this break as comment for run BFS randomly,
                                                                                 # otherwise it doesent make goode shape of maze
            else:
                queue.pop(0)
                break


def plot_route_back(x,y):
    solution_cell(x, y, YELLOW)                                          # solution list contains all the coordinates to route back to start
    while (x, y) != (20,20):                                             # loop until cell position == start position
        previous_x, previous_y = x, y
        x, y = solution[(x, y)]                                          # "key value" now becomes the new key
        solution_line(previous_x, previous_y, x, y)                                      # animate route back
        time.sleep(.1)
    solution_cell(x, y, GOLD)


x, y = 20, 20                     # starting position of grid
build_grid(40, 0, 20)             # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
carve_out_maze(x,y)               # call build the maze  function
plot_route_back(400, 400)         # call the plot solution function


# ##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False