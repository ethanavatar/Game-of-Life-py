from . import App
from .const import *

def rule(prev_gen):
    next_gen = App.new_grid()
    for row in range(CELLMAP_HEIGHT):
        for col in range(CELLMAP_WIDTH):
            cell = prev_gen[row][col]
            alive_neighbors = sum([
                prev_gen[(row)%CELLMAP_HEIGHT][(col-1)%CELLMAP_WIDTH],
                prev_gen[(row)%CELLMAP_HEIGHT][(col+1)%CELLMAP_WIDTH],

                prev_gen[(row+1)%CELLMAP_HEIGHT][(col-1)%CELLMAP_WIDTH],
                prev_gen[(row+1)%CELLMAP_HEIGHT][(col)%CELLMAP_WIDTH],
                prev_gen[(row+1)%CELLMAP_HEIGHT][(col+1)%CELLMAP_WIDTH],

                prev_gen[(row-1)%CELLMAP_HEIGHT][(col-1)%CELLMAP_WIDTH],
                prev_gen[(row-1)%CELLMAP_HEIGHT][(col)%CELLMAP_WIDTH],
                prev_gen[(row-1)%CELLMAP_HEIGHT][(col+1)%CELLMAP_WIDTH]
            ])

            if cell == 1 and (alive_neighbors < 2):
                next_gen[row][col] = 0

            elif cell == 1 and (alive_neighbors == 2 or alive_neighbors == 3):
                next_gen[row][col] = 1

            elif cell == 1 and (alive_neighbors > 3):
                next_gen[row][col] = 0

            elif cell == 0 and (alive_neighbors == 3):
                next_gen[row][col] = 1

    return next_gen