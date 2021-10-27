from . import App
from .const import *

def rule(prev_gen):
    next_gen = App.new_grid()
    for i in range(CELLMAP_HEIGHT*CELLMAP_WIDTH):
        cell = prev_gen[i]
        alive_neighbors = sum([
            (prev_gen[(i-1-CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)] == ALIVE) ^ 0,
            (prev_gen[(i-CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)] == ALIVE) ^ 0,
            (prev_gen[(i+1-CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)] == ALIVE) ^ 0,
            (prev_gen[(i-1) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)] == ALIVE) ^ 0,
            (prev_gen[(i+1) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)] == ALIVE) ^ 0,
            (prev_gen[(i-1+CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)] == ALIVE) ^ 0,
            (prev_gen[(i+CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)] == ALIVE) ^ 0,
            (prev_gen[(i+1+CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)] == ALIVE) ^ 0
        ])

        if cell == ALIVE:
            next_gen[i] = DYING
        elif cell == DYING:
            next_gen[i] = DEAD
        else:
            if alive_neighbors == 2:
                next_gen[i] = ALIVE

    return next_gen