from . import App


def rule(grid):
    next_generation = App.new_grid()
    for row in range(App.GRID_HEIGHT):
        for col in range(App.GRID_WIDTH):
            alive_neighbors = 0
            for neighbor in App.get_neighbors(row, col):
                if grid[neighbor[0]][neighbor[1]] == 1:
                    alive_neighbors += 1

            if grid[row][col] == 1 and (alive_neighbors < 2):
                next_generation[row][col] = 0

            elif grid[row][col] == 1 and (alive_neighbors == 2 or alive_neighbors == 3):
                next_generation[row][col] = 1

            elif grid[row][col] == 1 and (alive_neighbors > 3):
                next_generation[row][col] = 0

            elif grid[row][col] == 0 and (alive_neighbors == 3):
                next_generation[row][col] = 1

    return next_generation