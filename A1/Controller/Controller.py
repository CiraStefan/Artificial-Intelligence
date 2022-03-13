import pickle
from random import random
import pygame

from Model.Environment import *
from Model.DMap import *
from Model.Drone import *

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


class Controller:
    def __init__(self, env, d_map, drone):
        self._env = env
        self._d_map = d_map
        self._drone = drone
        self.nr_of_visited = 1

    def markDetectedWalls(self, x, y):
        #   To DO
        # mark on this map the wals that you detect
        wals = self._env.readUDMSensors(x, y)
        i = x - 1
        if wals[UP] > 0:
            while ((i >= 0) and (i >= x - wals[UP])):
                if self._d_map.surface[i][y] == -1:
                    self._d_map.surface[i][y] = 0
                    self.nr_of_visited += 1
                i = i - 1
        if (i >= 0):
            self._d_map.surface[i][y] = 1

        i = x + 1
        if wals[DOWN] > 0:
            while ((i < self._d_map.get_n()) and (i <= x + wals[DOWN])):
                if self._d_map.surface[i][y] == -1:
                    self._d_map.surface[i][y] = 0
                    self.nr_of_visited += 1
                i = i + 1
        if (i < self._d_map.get_n()):
            self._d_map.surface[i][y] = 1

        j = y + 1
        if wals[LEFT] > 0:
            while ((j < self._d_map.get_m()) and (j <= y + wals[LEFT])):
                if self._d_map.surface[x][j] == -1:
                    self._d_map.surface[x][j] = 0
                    self.nr_of_visited += 1
                j = j + 1
        if (j < self._d_map.get_m()):
            self._d_map.surface[x][j] = 1

        j = y - 1
        if wals[RIGHT] > 0:
            while ((j >= 0) and (j >= y - wals[RIGHT])):
                if self._d_map.surface[x][j] == -1:
                    self._d_map.surface[x][j] = 0
                    self.nr_of_visited += 1
                j = j - 1
        if (j >= 0):
            self._d_map.surface[x][j] = 1
        return None

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self._drone.x > 0:
            if pressed_keys[K_UP] and self._d_map.surface[self._drone.x - 1][self._drone.y] ==0:
                self._drone.x = self._drone.x - 1
        if self._drone.x < 19:
            if pressed_keys[K_DOWN] and self._d_map.surface[self._drone.x +1][self._drone.y ]==0:
                self._drone.x = self._drone.x + 1

        if self._drone.y > 0:
            if pressed_keys[K_LEFT ]and self._d_map.surface[self._drone.x][self._drone.y -1 ]==0:
                self._drone.y = self._drone.y - 1
        if self._drone.y < 19:
            if pressed_keys[K_RIGHT] and self._d_map.surface[self._drone.x][self._drone.y + 1]==0:
                self._drone.y = self._drone.y + 1


    def moveDSF(self):
        if len(self._drone.moves_stack) == 0:
            self._drone.x = None
            self._drone.y = None
            return -1
        pair = self._drone.moves_stack.pop()
        self._drone.x = pair[0]
        self._drone.y = pair[1]
        self._d_map.surface[self._drone.x][self._drone.y] = pair[2] + 1
        if self._drone.x > 0:
            if self._d_map.surface[self._drone.x - 1][self._drone.y] == 0:
                self._drone.x = self._drone.x - 1
                self._drone.moves_stack.append([self._drone.x, self._drone.y, pair[2] + 1])
                return

        if self._drone.x < 19:
            if self._d_map.surface[self._drone.x + 1][self._drone.y] == 0:
                self._drone.x = self._drone.x + 1
                self._drone.moves_stack.append([self._drone.x, self._drone.y, pair[2] + 1])
                return

        if self._drone.y > 0:
            if self._d_map.surface[self._drone.x][self._drone.y - 1] == 0:
                self._drone.y = self._drone.y - 1
                self._drone.moves_stack.append([self._drone.x, self._drone.y, pair[2] + 1])
                return
        if self._drone.y < 19:
            if self._d_map.surface[self._drone.x][self._drone.y + 1] == 0:
                self._drone.y = self._drone.y + 1
                self._drone.moves_stack.append([self._drone.x, self._drone.y, pair[2] + 1])
                return
        # if there is no new move that we can make, we search for the previous value
        if self._drone.x > 0 and self._d_map.surface[self._drone.x - 1][self._drone.y] == pair[2]:
            self._drone.x = self._drone.x - 1
            self._drone.moves_stack.append([self._drone.x, self._drone.y, pair[2] - 1])
        if self._drone.x < 19 and self._d_map.surface[self._drone.x + 1][self._drone.y] == pair[2]:
            self._drone.x = self._drone.x + 1
            self._drone.moves_stack.append([self._drone.x, self._drone.y, pair[2] - 1])
        if self._drone.y > 0 and self._d_map.surface[self._drone.x][self._drone.y - 1] == pair[2]:
            self._drone.y = self._drone.y - 1
            self._drone.moves_stack.append([self._drone.x, self._drone.y, pair[2] - 1])
        if self._drone.y < 19 and  self._d_map.surface[self._drone.x][self._drone.y + 1] == pair[2]:
            self._drone.y = self._drone.y + 1
            self._drone.moves_stack.append([self._drone.x, self._drone.y, pair[2] - 1])

    def readUDMSensors(self, x, y):
        readings = [0, 0, 0, 0]
        # UP
        xf = x - 1
        while ((xf >= 0) and (self._env.__surface[xf][y] == 0)):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self._env.__n) and (self._env.__surface[xf][y] == 0)):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self._env.__m) and (self._env.__surface[x][yf] == 0)):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self._env.__surface[x][yf] == 0)):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1

        return readings