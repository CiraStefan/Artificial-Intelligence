import numpy as np
import pygame

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]

class DMap():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = -1

    def get_n(self):
        return self.__n

    def get_m(self):
        return self.__m

    def image(self, x, y):

        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        visited = pygame.Surface((20, 20))
        empty.fill(WHITE)
        brick.fill(BLACK)
        visited.fill(RED)
        imagine.fill(GRAYBLUE)

        for i in range(self.get_n()):
            for j in range(self.get_m()):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                elif self.surface[i][j] == 0:
                    imagine.blit(empty, (j * 20, i * 20))
                elif self.surface[i][j] != -1:
                    imagine.blit(visited, (j * 20, i * 20))

        drona = pygame.image.load("drona.png")
        imagine.blit(drona, (y * 20, x * 20))
        return imagine
