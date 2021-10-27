from . import App
from .const import *

def rule(prev_gen):
    next_gen = App.new_grid()
    for i in range(CELLMAP_HEIGHT*CELLMAP_WIDTH):
        cell = prev_gen[i]
        alive_neighbors = sum([
            prev_gen[(i-1-CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)],
            prev_gen[(i-CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)],
            prev_gen[(i+1-CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)],
            prev_gen[(i-1) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)],
            prev_gen[(i+1) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)],
            prev_gen[(i-1+CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)],
            prev_gen[(i+CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)],
            prev_gen[(i+1+CELLMAP_WIDTH) % (CELLMAP_WIDTH*CELLMAP_HEIGHT)]
        ])

        if cell == ALIVE:
            if alive_neighbors < 2 or alive_neighbors > 3:
                next_gen[i] = DEAD
            else:
                next_gen[i] = ALIVE
        else:
            if alive_neighbors == 3:
                next_gen[i] = ALIVE

    return next_gen