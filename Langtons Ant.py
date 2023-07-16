"""
Langton's Ant
"""
import numpy as np
import sys
import pygame


class LangtonsAnt:
    def __init__(self, grid_dimensions: (int, int)):
        self.grid_dimensions = grid_dimensions
        self.grid = np.zeros(grid_dimensions)
        # start with ant in center pointing north
        self.position = (int(grid_dimensions[0]/2), int(grid_dimensions[1]/2))
        self.orientation = (0, -1)    # (0, -1):=north, (1, 0):=west, (0, 1):= south, (-1, 0):=east
        return

    def flip_cell(self, pos: (int, int)):
        self.grid[pos[0], pos[1]] = (self.grid[pos[0], pos[1]] + 1) % 2

    def update(self):
        # white cell
        if self.grid[self.position[0], self.position[1]] == 0:
            # turn right:
            if self.orientation == (0, -1): # north -> west
                self.orientation = (1, 0)
            elif self.orientation == (1, 0): # west -> south
                self.orientation = (0, 1)
            elif self.orientation == (0, 1): # south -> east
                self.orientation = (-1, 0)
            elif self.orientation == (-1, 0): # east -> north
                self.orientation = (0, -1)
            # flip cell
            self.flip_cell((self.position[0], self.position[1]))
            # go forward
            self.position = ((self.position[0] + self.orientation[0]) % self.grid_dimensions[0],
                             (self.position[1] + self.orientation[1]) % self.grid_dimensions[1])
        # black cell
        elif self.grid[self.position[0], self.position[1]] == 1:
            # turn right:
            if self.orientation == (0, -1): # north -> east
                self.orientation = (-1, 0)
            elif self.orientation == (-1, 0): # east -> south
                self.orientation = (0, 1)
            elif self.orientation == (0, 1): # south -> west
                self.orientation = (1, 0)
            elif self.orientation == (1, 0): # east -> north
                self.orientation = (0, -1)
            # flip cell
            self.flip_cell((self.position[0], self.position[1]))
            # go forward
            self.position = ((self.position[0] + self.orientation[0]) % self.grid_dimensions[0],
                             (self.position[1] + self.orientation[1]) % self.grid_dimensions[1])
        return

    def get_grid(self):
        return self.grid



if __name__ == '__main__':
    # figure out proportions:
    block_num = 90
    block_size = 7
    screen_size = block_num * (block_size)

    ant = LangtonsAnt((block_num, block_num))

    # pygame setup
    pygame.init()
    pygame.display.set_caption("Langton's Ant")
    screen = pygame.display.set_mode((screen_size, screen_size))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:
        # poll for events
        # pygame.QHIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        for y in range(block_num):
            for x in range(block_num):
                rect = pygame.Rect(x*(block_size), y*(block_size), block_size, block_size)
                pygame.draw.rect(screen, "indigo", rect)


        # RENDER YOUR GAME HERE
        ant.update()
        ant_grid = ant.get_grid()

        for (i, row) in enumerate(ant_grid):
            for (j, value) in enumerate(row):
                if value == 1:
                    pygame.draw.rect(surface=screen, color="yellowgreen", rect=((i*(block_size), j*(block_size)),
                                                                                (block_size, block_size)))

        # flip() the display to put your work on screen
        pygame.display.flip()

        dt = clock.tick(500)/ 1000  # limit FPS to 60

    pygame.quit()
