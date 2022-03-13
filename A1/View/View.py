import time

from Controller.Controller import *

class View:
    def __init__(self, controller):
        self.controller = controller
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")
        self.screen = pygame.display.set_mode((800, 400))
        self.screen.fill(WHITE)
        self.screen.blit(self.controller._env.image(), (0, 0))

    def run(self):
        self.controller._d_map.surface[self.controller._drone.x][self.controller._drone.y] = -2
        self.controller.markDetectedWalls(self.controller._drone.x, self.controller._drone.y)
        pygame.display.flip()
        # define a variable to control the main loop
        running = True

        # main loop
        while running:
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
            time.sleep(0.1)
            self.controller.moveDSF()
            if self.controller._drone.x is None or self.controller._drone.y is None \
                    or self.controller.nr_of_visited == self.controller._env.nr_of_cells:
                running = False
                continue
            self.controller.markDetectedWalls(self.controller._drone.x, self.controller._drone.y)
            self.screen.blit(self.controller._d_map.image(self.controller._drone.x, self.controller._drone.y), (400, 0))
            pygame.display.flip()

        pygame.quit()

