import pygame, random

from pygame.locals import *

from .const import *

def new_grid():
    grid = [[DEAD for i in range(CELLMAP_WIDTH)] for j in range(CELLMAP_HEIGHT)]
    return grid

def random_grid():
    grid = new_grid()
    for row in range(CELLMAP_HEIGHT):
        for col in range(CELLMAP_WIDTH):
            grid[row][col] = random.randint(0, 1)
    return grid

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

        self.latency = 0

        self.FPScounter = pygame.font.Font(None, 15)
        self.LatencyCounter = pygame.font.Font(None, 15)
        self.GENcounter = pygame.font.Font(None, 15)
        

    def run(self, paused=PAUSED):
        self.paused = paused
        while self.running:
            
            # If there is a specified FPS cap
            if FPS:
                # Clock at the specified FPS cap
                self.latency = self.clock.tick(FPS)
            # If there is no specified FPS cap
            else: # default; self.targetFPS == None
                # Clock at unbound speed
                self.latency = self.clock.tick()
            
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
                self.mouse_col, self.mouse_row = int(mouse_pos[0] // CELL_WIDTH), int(mouse_pos[1] // CELL_HEIGHT)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused ^= True
                    print(f'paused={self.paused}')

                if event.key == pygame.K_ESCAPE:
                    self.simulation.grid = new_grid()
                    self.simulation.generation = 0
                    print('clear')

                if event.key == pygame.K_r:
                    self.simulation.grid = random_grid()
                    print('random')

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
        color = BLACK
        for row in range(CELLMAP_HEIGHT):
            for col in range(CELLMAP_WIDTH):
                if self.simulation.grid[row][col] == 1:
                    color = WHITE
                    pygame.draw.rect(self.screen, color, pygame.Rect((col * CELL_WIDTH, row * CELL_HEIGHT), (CELL_WIDTH, CELL_HEIGHT)), FILL_CELL ^ 1)

        if SHOW_FPS:
            fps = self.FPScounter.render(f'FPS: {round(self.clock.get_fps(), 2)}', True, WHITE)
            self.screen.blit(fps, (SCREEN_WIDTH - 100, 15))

        if SHOW_LATENCY:
            latency = self.LatencyCounter.render(f'Latency: {self.latency} ms', True, WHITE)
            self.screen.blit(latency, (SCREEN_WIDTH - 100, 30))
            
        if SHOW_GENERATION:
            generation = self.GENcounter.render(f'Generation: {self.simulation.generation}', True, WHITE)
            self.screen.blit(generation, (SCREEN_WIDTH - 100, 45))
        
        pygame.display.update()