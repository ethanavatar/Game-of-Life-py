import pygame, random

from pygame.locals import *

from .const import *

def new_grid():
    grid = [DEAD for i in range(CELLMAP_WIDTH*CELLMAP_WIDTH)]
    return grid

def random_grid():
    grid = [random.randint(0, 1) for i in range(CELLMAP_WIDTH*CELLMAP_WIDTH)]
    return grid
def get_cell(grid, row, col):
    return grid[row*CELLMAP_WIDTH + col]

def set_cell(grid, row, col, value):
    grid[row*CELLMAP_WIDTH + col] = value

class Simulation:
    def __init__(self, rule, initial_state=None):
        self.rule = rule

        if initial_state is None:
            self.current_gen = new_grid()
        else:
            self.current_gen = initial_state     

        self.generation = 0
        
    def next_generation(self):
        self.last_gen = self.current_gen
        self.current_gen = self.rule(self.current_gen)
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

        self.forward_hold = False
        self.forward_hold_time = 0

        self.backward_hold = False
        self.backward_hold_time = 0

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up = True

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                self.mouse_col, self.mouse_row = int(mouse_pos[0] // CELL_WIDTH), int(mouse_pos[1] // CELL_HEIGHT)
            
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    self.paused ^= True
                    print(f'paused = {self.paused}')

                elif event.key == pygame.K_ESCAPE:
                    self.simulation.current_gen = new_grid()
                    self.simulation.generation = 0
                    print('clear')

                elif event.key == pygame.K_r:
                    self.simulation.current_gen = random_grid()
                    print('random')

                elif event.key == pygame.K_PERIOD:
                    self.paused = True
                    self.simulation.next_generation()
                    self.forward_hold = True
                    self.forward_hold_time = pygame.time.get_ticks()

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_PERIOD:

                    self.forward_hold = False

        if self.forward_hold and pygame.time.get_ticks() - self.forward_hold_time > 200:

            self.simulation.next_generation()

        if self.mouse_down:

            self.hold = True

            if get_cell(self.simulation.current_gen, self.mouse_col, self.mouse_row) == ALIVE:

                set_cell(self.simulation.current_gen, self.mouse_col, self.mouse_row, 0)
                self.hold_value = 0

            elif get_cell(self.simulation.current_gen, self.mouse_col, self.mouse_row) == DEAD:

                set_cell(self.simulation.current_gen, self.mouse_col, self.mouse_row, 1)
                self.hold_value = 1

            self.mouse_down = False

        if self.hold:

            set_cell(self.simulation.current_gen, self.mouse_col, self.mouse_row, self.hold_value)

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
        for i in range(CELLMAP_HEIGHT*CELLMAP_WIDTH):
            row = i % CELLMAP_WIDTH
            col = i // CELLMAP_WIDTH
            if self.simulation.current_gen[i] == ALIVE:
                color = WHITE
                pygame.draw.rect(self.screen, color, pygame.Rect((col * CELL_WIDTH, row * CELL_HEIGHT), (CELL_WIDTH, CELL_HEIGHT)), FILL_CELL ^ 1)
            elif self.simulation.current_gen[i] == DYING:
                color = BLUE
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