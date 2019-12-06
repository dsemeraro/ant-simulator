#rimuove messaggio di benvenuto di pygame
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import numpy as np
import sys

ENL_RATIO = 10
RED = (255,0,0)
GREEN = (0, 200, 0)
ORANGE = (235, 120, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)
OPAQUE = 255

class Graphic:
    
    def __init__(self, env):
        pygame.init()
        self.env = env
        self.screen = pygame.display.set_mode(
            (self.env.map_size * ENL_RATIO, self.env.map_size * ENL_RATIO)
        )
        self.screen.fill(WHITE)        
    
    def draw_env(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill(WHITE)
        
        #draws pheromone     
        index = np.asarray(np.where(self.env.stigmergic_space.map_pheromone > 0)).T
        for x,y in index:
            self.draw_object(
                y, x, BLUE,
                self.env.stigmergic_space.map_pheromone[x,y]
            )

        #draws anthill
        x,y = self.env.anthill
        self.draw_object(y, x, ORANGE, OPAQUE)

        #draws food        
        index = np.asarray(np.where(self.env.food_map != 0)).T
        for x,y in index:
            self.draw_object(y, x, RED, OPAQUE)
        
        #draws ants        
        for ant in self.env.ants:
            if ant.food:
                self.draw_object(ant.y, ant.x, GREEN, OPAQUE)
            else:
                self.draw_object(ant.y, ant.x, BLACK, OPAQUE)
        
        pygame.display.update()

    def draw_object(self, x, y, color, alpha):
        rect = pygame.Surface((ENL_RATIO, ENL_RATIO))
        rect.set_alpha(alpha*3)
        rect.fill(color)
        self.screen.blit(rect, (x * ENL_RATIO, y * ENL_RATIO))        

