

# import the pygame module, so you can use it
import pickle,pygame,sys
import time

from pygame.locals import *
from random import random, randint
import numpy as np
from View.View import *
        

        
        



# define a main function
def main():
    #we create the environment
    e = Environment()
    e.randomMap()
    #print(str(e))
    
    # we create the map
    m = DMap()
    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)
    
    #cream drona
    d = Drone(x, y)

    controller = Controller(e, m, d)
    view = View(controller)
    view.run()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()