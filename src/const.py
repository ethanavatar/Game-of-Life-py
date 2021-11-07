from enum import IntEnum
from random import randint

CELLMAP_WIDTH = 150
CELLMAP_HEIGHT = 150

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200

CELL_WIDTH = SCREEN_WIDTH / CELLMAP_WIDTH
CELL_HEIGHT = SCREEN_HEIGHT / CELLMAP_HEIGHT

FILL_CELL = 0

SHOW_FPS = True
SHOW_LATENCY = True
SHOW_GENERATION = True

FPS = None
PAUSED = True

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

DEAD = 0
ALIVE = 1
DYING = 2

def new_grid():
    grid = [DEAD for i in range(CELLMAP_WIDTH*CELLMAP_WIDTH)]
    return grid

def random_grid():
    grid = [randint(0, 1) for i in range(CELLMAP_WIDTH*CELLMAP_WIDTH)]
    return grid
    
def get_cell(grid, row, col):
    return grid[row*CELLMAP_WIDTH + col]

def set_cell(grid, row, col, value):
    grid[row*CELLMAP_WIDTH + col] = value