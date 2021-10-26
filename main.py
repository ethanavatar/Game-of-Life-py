import src.Game_of_Life as GoL
from src import App

def main(rule, grid):
    sim = App.Simulation(rule, grid)
    app = App.App(sim)
    app.run(paused = False)

if __name__ == '__main__':
    grid = App.new_grid()
    
    # Spawn a really long vertical line with 20 dead cells on top and bottom
    for row in range(20, App.GRID_HEIGHT-20):
        grid[row][App.GRID_WIDTH // 2] = 1

    main(GoL.rule, grid)