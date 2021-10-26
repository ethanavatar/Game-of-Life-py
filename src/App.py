import pygame, random

from pygame.locals import *

from src import Game_of_Life

GRID_WIDTH = 200
GRID_HEIGHT = 200

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200

PIXEL_WIDTH = SCREEN_WIDTH / GRID_WIDTH
PIXEL_HEIGHT = SCREEN_HEIGHT / GRID_HEIGHT

SHOW_FPS = True
SHOW_GENERATION = True

FPS = None
PAUSED = True

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def new_grid():
    grid = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]
    return grid

def random_grid():
    grid = new_grid()
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            grid[row][col] = random.randint(0, 1)
    return grid

def get_neighbors(row, col):
    neighbors = [
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
    
    for pos in neighbors:
        ret.append((pos[1]%GRID_HEIGHT, pos[0]%GRID_WIDTH))
    return ret

class Simulation:
    def __init__(self, rule, grid=None):
        self.rule = rule

        if grid is None:
            self.grid = new_grid()
        else:
            self.grid = grid       

        self.generation = 0
        
    def next_generation(self):
        self.grid = self.rule(self.grid)
        self.generation += 1
    
class App:
    def __init__(self, simulation):

        successes, fails = pygame.init()

        self.simulation = simulation
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = PAUSED

        self.mouse_down = False
        self.mouse_up = False

        self.hold = False
        self.hold_value = None

        self.step_hold = False
        self.step_hold_time = 0

        self.mouse_row = None
        self.mouse_col = None

        self.FPScounter = pygame.font.Font(None, 15)
        self.GENcounter = pygame.font.Font(None, 15)
        

    def run(self, paused=PAUSED):
        self.paused = paused
        while self.running:
            
            # If there is a specified FPS cap
            if FPS:
                # Clock at the specified FPS cap
                self.clock.tick(FPS)
            # If there is no specified FPS cap
            else: # default; self.targetFPS == None
                # Clock at unbound speed
                self.clock.tick()
            
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up = True

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                self.mouse_col, self.mouse_row = int(mouse_pos[0] // PIXEL_WIDTH), int(mouse_pos[1] // PIXEL_HEIGHT)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused ^= True
                    print(f'{self.paused=}')

                if event.key == pygame.K_ESCAPE:
                    self.simulation.grid = new_grid()
                    self.simulation.generation = 0
                    print(f'clear')

                if event.key == pygame.K_r:
                    self.simulation.grid = random_grid()
                    print(f'random')

                '''
                if event.key == pygame.K_g:
                    self.simulation.grid = Game_of_Life.glider(self.simulation.grid, self.mouse_row, self.mouse_col)
                '''
                
                if event.key == pygame.K_COMMA:
                    pass
                if event.key == pygame.K_PERIOD:
                    self.paused = True
                    self.simulation.next_generation()
                    self.step_hold = True
                    self.step_hold_time = pygame.time.get_ticks()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_PERIOD:
                    self.step_hold = False

        if self.step_hold and pygame.time.get_ticks() - self.step_hold_time > 200:
            self.simulation.next_generation()

        if self.mouse_down:
            self.hold = True
            if self.simulation.grid[self.mouse_row][self.mouse_col] == 1:
                # TODO: Pure functionalize this
                self.simulation.grid[self.mouse_row][self.mouse_col] = 0

                self.hold_value = 0

            elif self.simulation.grid[self.mouse_row][self.mouse_col] == 0:
                # TODO: Pure functionalize this
                self.simulation.grid[self.mouse_row][self.mouse_col] = 1
                self.hold_value = 1

            self.mouse_down = False
        if self.hold:
            self.simulation.grid[self.mouse_row][self.mouse_col] = self.hold_value
            if self.mouse_up:
                self.hold = False
                self.mouse_up = False

    def update(self):
        if self.paused:
            return

        self.simulation.next_generation()

    def draw(self):
        self.screen.fill(BLACK)
        surface = pygame.Surface((PIXEL_WIDTH, PIXEL_HEIGHT))
        surface.fill(WHITE)
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if self.simulation.grid[row][col] == 1:
                    self.screen.blit(surface, pygame.Rect((col * PIXEL_WIDTH, row * PIXEL_HEIGHT), (PIXEL_WIDTH, PIXEL_HEIGHT)))

        if SHOW_FPS:
            fps = self.FPScounter.render(f'FPS: {round(self.clock.get_fps(), 2)}{self.simulation.generation}', True, WHITE)
            self.screen.blit(fps, (SCREEN_WIDTH - 100, 10))
        if SHOW_GENERATION:
            generation = self.GENcounter.render(f'Generation: {self.simulation.generation}', True, WHITE)
            self.screen.blit(generation, (SCREEN_WIDTH - 100, 25))
        
        pygame.display.update()