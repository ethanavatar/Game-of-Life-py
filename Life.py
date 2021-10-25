import pygame, random

GRID_WIDTH = 160
GRID_HEIGHT = 90

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

FPS = 24
PAUSED = False

def new_grid():
    grid = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]
    return grid

def checker(i=None):
    grid = new_grid() if i == None else i
    activator = 1
    for row in range(GRID_HEIGHT):
        activator ^= 1
        for col in range(GRID_WIDTH):
            grid[row][col] = activator
            activator ^= 1
    return grid

def get_neighbors(grid, row, col):
    tries = [
        (col-1, row),
        (col+1, row),
        (col, row-1),
        (col, row+1),
        (col-1, row-1),
        (col+1, row+1),
        (col-1, row+1),
        (col+1, row-1)
    ]
    ret = []
    
    for pos in tries:
        try:
            grid[pos[1]][pos[0]]
        except IndexError:
            continue
        else:
            ret.append(pos)
    return ret

def update_cell(grid, row, col, value=None):
    if value == None:
        grid[row][col] ^= 1
    else:
        grid[row][col] = value
    #print(get_neighbors(grid, row, col))

def simulate(grid):
    next_generation = new_grid()
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            alive_neighbors = 0
            for neighbor in get_neighbors(grid, row, col):
                if grid[neighbor[1]][neighbor[0]] == 1:
                    alive_neighbors += 1

            if grid[row][col] == 1 and (alive_neighbors < 2):
                update_cell(next_generation, row, col, 0)

            elif grid[row][col] == 1 and (alive_neighbors == 2 or alive_neighbors == 3):
                update_cell(next_generation, row, col, 1)

            elif grid[row][col] == 1 and (alive_neighbors > 3):
                update_cell(next_generation, row, col, 0)

            elif grid[row][col] == 0 and (alive_neighbors == 3):
                update_cell(next_generation, row, col, 1)

    return next_generation
                
def main(grid):

    successes, fails = pygame.init()

    screen = pygame.display.set_mode(size = (SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    PIXEL_WIDTH = SCREEN_WIDTH / GRID_WIDTH
    PIXEL_HEIGHT = SCREEN_HEIGHT / GRID_HEIGHT

    #print((PIXEL_WIDTH, PIXEL_HEIGHT))
            
    mouse_down = False
    mouse_up = False

    hold = False
    hold_value = None

    mouse_pos = None
    grid_col = None
    grid_row = None
    
    paused = PAUSED
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                grid_col, grid_row = int(mouse_pos[0] // PIXEL_WIDTH), int(mouse_pos[1] // PIXEL_HEIGHT)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused ^= True
                    print(f'{paused=}')

                if event.key == pygame.K_ESCAPE:
                    grid = new_grid()

                if event.key == pygame.K_r:
                    grid = new_grid()
                    for row in range(GRID_HEIGHT):
                        for col in range(GRID_WIDTH):
                            grid[row][col] = random.randint(0, 1)

        if not paused:
            grid = simulate(grid)

        if mouse_down:
            hold = True

            #print(((grid_col, grid_row), mouse_pos))

            if grid[grid_row][grid_col] == 1:
                update_cell(grid, grid_row, grid_col, 0)
                hold_value = 0

            elif grid[grid_row][grid_col] == 0:
                update_cell(grid, grid_row, grid_col, 1)
                hold_value = 1

            mouse_down = False
        if hold:
            update_cell(grid, grid_row, grid_col, hold_value)
            if mouse_up:
                hold = False
                mouse_up = False
            

        screen.fill(BLACK)

        surface = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
        surface.fill(WHITE)

        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if grid[row][col] == 1:
                    screen.blit(surface, pygame.Rect((col * PIXEL_WIDTH, row * PIXEL_HEIGHT), (PIXEL_WIDTH, PIXEL_HEIGHT)))

        pygame.display.update()

if __name__ == '__main__':

    grid = new_grid()
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if random.randint(1, 10) % 2:
                grid[row][col] = 1

    main(grid)