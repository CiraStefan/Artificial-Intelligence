import pygame
from pygame.locals import *

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

class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moves_stack = [[x, y, 2]]
        # instead of marking visited cells with a constant value, we set for the first cell the value 2
        # after that, at each step, we increment the value in order to be able to get the previous value we visited
        self.cur_value = 2
