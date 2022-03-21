

# import the pygame module, so you can use it
import pickle,pygame
import time
from datetime import datetime
from random import random, randint
import numpy as np


from taks1.Controller import Controller
from taks1.entities import *

BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)





def dummysearch():
    #example of some path in test1.map from [5,7] to [7,11]
    return [[5,7],[5,8],[5,9],[5,10],[5,11],[6,11],[7,11]]
    
def displayWithPath(image, path):
    mark = pygame.Surface((20,20))
    mark.fill(GREEN)
    for move in path:
        image.blit(mark, (move[1] *20, move[0] * 20))
        
    return image


def displayWithPath1(image, path):
    mark = pygame.Surface((20, 20))
    mark.fill(RED)
    for move in path:
        image.blit(mark, (move[1] * 20, move[0] * 20))

    return image

                  
# define a main function
def main():
    
    # we create the map
    m = Map() 
    #m.randomMap()
    #m.saveMap("test2.map")
    m.loadMap("test1.map")
    
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")
        
    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)
    
    #create drona
    d = Drone(x, y)
    
    #create Controller
    c = Controller(m, d)
    
    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400,400))
    screen.fill(WHITE)
    
    
    # define a variable to control the main loop
    running = True
    path = []
    path1 = []
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            
            if event.type == KEYDOWN:
                startX = d.getX()
                startY = d.getY()
                t0 = datetime.now()
                path = c.searchAStar(m, d, startX, startY, 19, 19)
                t1 = datetime.now()
                path1 = c.searchGreedy(m, d, startX, startY, 19, 19)
                t2 = datetime.now()
                if path is not None:
                    # screen.blit(displayWithPath(m.image(), path),(0,0))
                    astar_time = t1 - t0
                    print('time taken for A* is: ' + astar_time.__str__())
                    # screen.blit(displayWithPath1(m.image(), path1),(0,0))
                    greedy_time = t2 - t1
                    print('time taken for greedy is: ' + greedy_time.__str__())
                    running = False
                #d.move(m) #this call will be erased
        
        
        screen.blit(d.mapWithDrone(m.image()),(0,0))
        pygame.display.flip()
       
    #path = dummysearch()

    screen.blit(displayWithPath(m.image(), path),(0,0))

    pygame.display.flip()
    time.wait(2000)
    # time.sleep(5)
    pygame.quit()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()