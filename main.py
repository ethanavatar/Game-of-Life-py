import src.GameOfLife as GoL
import src.BriansBrain as BB

from src import App
from src.const import *

def GameOfLife():
    grid = App.new_grid()
    
    # Spawn a really long vertical line with 10 dead cells on top and bottom
    for row in range(10, CELLMAP_HEIGHT-10):
        App.set_cell(grid, CELLMAP_WIDTH//2, row,  ALIVE)

    sim = App.Simulation(GoL.rule, grid)
    app = App.App(sim)
    app.run(paused=False)

def BriansBrain():
    grid = App.random_grid()
    sim = App.Simulation(BB.rule, grid)
    app = App.App(sim)
    app.run(paused=False)

if __name__ == '__main__':
    GameOfLife()
    #BriansBrain()