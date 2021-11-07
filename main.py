import pygame
from pygame.locals import *

import src.GameOfLife as GoL
import src.BriansBrain as BB

from src.const import *

def main(rule):

    successes, fails = pygame.init()

    cellmap = new_grid()

    generation_num = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    running = True
    paused = PAUSED

    mouse_down = False
    mouse_up = False

    hold = False
    hold_value = None

    forward_hold = False
    forward_hold_time = 0

    mouse_row = None
    mouse_col = None

    mod = False

    latency = 0

    FPScounter = pygame.font.Font(None, 15)
    LatencyCounter = pygame.font.Font(None, 15)
    GENcounter = pygame.font.Font(None, 15)
    while running:

        screen.fill(BLACK)
        color = BLACK
        for i in range(CELLMAP_HEIGHT*CELLMAP_WIDTH):
            row = i % CELLMAP_WIDTH
            col = i // CELLMAP_WIDTH
            if cellmap[i] == ALIVE:
                color = WHITE
                pygame.draw.rect(screen, color, pygame.Rect((col * CELL_WIDTH, row * CELL_HEIGHT), (CELL_WIDTH, CELL_HEIGHT)), FILL_CELL ^ 1)
            elif cellmap[i] == DYING:
                color = BLUE
                pygame.draw.rect(screen, color, pygame.Rect((col * CELL_WIDTH, row * CELL_HEIGHT), (CELL_WIDTH, CELL_HEIGHT)), FILL_CELL ^ 1)

        if SHOW_FPS:
            fps = FPScounter.render(f'FPS: {round(clock.get_fps(), 2)}', True, WHITE)
            screen.blit(fps, (SCREEN_WIDTH - 100, 15))

        if SHOW_LATENCY:
            latency = LatencyCounter.render(f'Latency: {latency} ms', True, WHITE)
            screen.blit(latency, (SCREEN_WIDTH - 100, 30))
            
        if SHOW_GENERATION:
            generation = GENcounter.render(f'Generation: {generation_num}', True, WHITE)
            screen.blit(generation, (SCREEN_WIDTH - 100, 45))
        
        pygame.display.update()
        
        # If there is a specified FPS cap
        if FPS:
            # Clock at the specified FPS cap
            latency = clock.tick(FPS)
        # If there is no specified FPS cap
        else: # default; targetFPS == None
            # Clock at unbound speed
            latency = clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                mouse_col, mouse_row = int(mouse_pos[0] // CELL_WIDTH), int(mouse_pos[1] // CELL_HEIGHT)
            
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    paused ^= True
                    print(f'paused = {paused}')

                elif event.key == pygame.K_ESCAPE:
                    cellmap = new_grid()
                    generation_num = 0
                    print('clear')

                elif event.key == pygame.K_r:
                    cellmap = random_grid()
                    print('random')

                elif event.key == pygame.K_PERIOD:
                    paused = True
                    cellmap = rule(cellmap)
                    forward_hold = True
                    forward_hold_time = pygame.time.get_ticks()

                elif event.key ==pygame.K_LCTRL:
                    mod = True

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_PERIOD:

                    forward_hold = False

                elif event.key == pygame.K_LCTRL:
                    mod = False

        if forward_hold and pygame.time.get_ticks() - forward_hold_time > 200:

            cellmap = rule(cellmap)

        if mouse_down:

            hold = True

            if get_cell(cellmap, mouse_col, mouse_row) != DEAD:

                set_cell(cellmap, mouse_col, mouse_row, 0)
                hold_value = 0

            elif get_cell(cellmap, mouse_col, mouse_row) == DEAD:
                if mod:
                    set_cell(cellmap, mouse_col, mouse_row, DYING)
                    hold_value = DYING
                else:
                    set_cell(cellmap, mouse_col, mouse_row, 1)
                    hold_value = 1

            mouse_down = False

        if hold:

            set_cell(cellmap, mouse_col, mouse_row, hold_value)

            if mouse_up:

                hold = False
                mouse_up = False

        paused = paused
        

        if not paused:
            cellmap = rule(cellmap)

if __name__ == '__main__':
    main(GoL.rule)