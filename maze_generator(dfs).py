###################################
# Python maze generator program with randomic DFS algorithm
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
CHROMATIC_GREEN = (255 ,255 ,0)
GOLD = (255, 215, 0)

# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Generator (DFS)")
clock = pygame.time.Clock()

# setup maze variables
x = 0                    # x axis
y = 0                    # y axis
w = 20                   # width of cell
grid = []
visited = []
stack = []
adjacency_list = {}

# build the grid
def build_grid(x, y, w):
    for i in range(1,21):
        x = 20                                                            # set x coordinate to start position
        y = y + 20                                                        # start a new row
        for j in range(1, 21):
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y], 3)           # top of cell
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w], 3)   # right of cell
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w], 3)   # bottom of cell
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y], 3)           # left of cell
            grid.append((x,y))                                            # add cell to grid list
            x = x + 20                                                    # move cell to new position


def push_up(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y - w + 1, 19, 39), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                               # to animate the wall being removed


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
    pygame.draw.rect(screen, GREEN, (x + 1, y + 1, 19, 19), 0)          # draw a single width cell
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y + 1, 19, 19), 0)        # used to re-colour the path after single_cell
    pygame.display.update()                                          # has visited cell


def solution_cell(x,y, color, weight, height):
    pygame.draw.rect(screen, color, (x + 8, y + 8, weight, height), 0)             # used to show the solution
    pygame.display.update()                                                # has visited cell with tiny rectangle

def solution_line(previous_x, previous_y, x, y):
    pygame.draw.line(screen, RED, [previous_x + 8, previous_y + 12], [x + 8, y + 12], 3)        # used to show the solution
    pygame.display.update()                                                                     # has visited cell with red line

def BFS_covering(node, color):
    pygame.draw.rect(screen, color, (node[0] + 1, node[1] + 1, 19, 19), 0)             # used to show the solution
    pygame.display.update()
    
def carve_out_maze(x,y):
    single_cell(x, y)                                              # starting positing of maze
    stack.append((x,y))                                            # place starting cell into stack
    visited.append((x,y))                                          # add starting cell to visited list
    while len(stack) > 0:                                          # loop until stack is empty
        time.sleep(.07)                                            # slow program now a bit
        cell = []                                                  # define cell list
        if (x + w, y) not in visited and (x + w, y) in grid:       # right cell available?
            cell.append("right")                                   # if yes add to cell list

        if (x - w, y) not in visited and (x - w, y) in grid:       # left cell available?
            cell.append("left")

        if (x , y + w) not in visited and (x , y + w) in grid:     # down cell available?
            cell.append("down")

        if (x, y - w) not in visited and (x , y - w) in grid:      # up cell available?
            cell.append("up")

        if len(cell) > 0:                                          # check to see if cell list is empty
            cell_chosen = (random.choice(cell))                    # select one of the cell randomly

            if cell_chosen == "right":                             # if this cell has been chosen
                push_right(x, y)                                   # call push_right function
                if (x, y) not in adjacency_list:
                    adjacency_list[(x, y)] = list()
                adjacency_list[(x, y)].append((x + w, y))
                #solution[(x + w, y)] = x, y                        # solution = dictionary key = new cell, other = current cell
                x = x + w                                          # make this cell the current cell
                visited.append((x, y))                              # add to visited list
                stack.append((x, y))                                # place current cell on to stack

            elif cell_chosen == "left":
                push_left(x, y)
                if (x, y) not in adjacency_list:
                    adjacency_list[(x, y)] = list()
                adjacency_list[(x, y)].append((x - w, y))                
                #solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(x, y)
                if (x, y) not in adjacency_list:
                    adjacency_list[(x, y)] = list()
                adjacency_list[(x, y)].append((x, y + w))                
                #solution[(x , y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(x, y)
                if (x, y) not in adjacency_list:
                    adjacency_list[(x, y)] = list()
                adjacency_list[(x, y)].append((x, y - w))                
                #solution[(x , y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack
            single_cell(x, y)                                     # use single_cell function to show backtracking image
            time.sleep(.1)                                        # slow program down a bit
            backtracking_cell(x, y)                               # change colour to green to identify backtracking path


def plot_route_back(x,y):
    solution = bfs_solver((20, 20))
    solution_cell(x, y, CHROMATIC_GREEN, 10, 10)                                          # solution list contains all the coordinates to route back to start
    while (x, y) != (20, 20):                                       # loop until cell position == start position
        previous_x, previous_y = x, y
        x, y = solution[(x, y)]                                    # "key value" now becomes the new key
        solution_line(previous_x, previous_y, x, y)                                      # animate route back
        time.sleep(.1)
    solution_cell(x, y, GOLD, 10, 10)
    
'''def bfs_solver(start_node):
    level = {start_node : 0}
    parent = {start_node : None}
    frontier = [start_node]
    l = 1
    single_cell(start_node[0], start_node[1])
    time.sleep(.08)
    BFS_covering(start_node, YELLOW)
    while frontier:
        next_node = []
        for i in frontier:
            for j in adjacency_list[i]:
                if j not in level:
                    single_cell(j[0], j[1])
                    time.sleep(.08)
                    BFS_covering(j, YELLOW)                    
                    level[j] = l
                    parent[j] = i
                    next_node.append(j)
        frontier = next_node
        l +=1
    return parent'''

def bfs_solver(start_node):
    visited_node = []
    queue = []
    parent = {}
    queue.append(start_node)
    visited_node.append(start_node)
    single_cell(start_node[0], start_node[1])
    time.sleep(.08)
    backtracking_cell(start_node[0], start_node[1])
    solution_cell(start_node[0], start_node[1], GREEN, 3, 3)
    while len(queue) > 0:
        frontier = []
        if queue[0] in adjacency_list:
            frontier = adjacency_list[queue[0]]
        else:
            queue.pop(0)
            continue
        for node in frontier:
            if node not in visited_node:
                queue.append(node)
                visited_node.append(node)
                parent[node] = queue[0]
                single_cell(node[0], node[1])
                time.sleep(.08)
                backtracking_cell(node[0], node[1])
                solution_cell(node[0], node[1], GREEN, 3, 3)
        queue.pop(0)
    return parent


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