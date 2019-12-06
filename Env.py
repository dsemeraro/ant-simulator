import numpy as np
import Graphic as gp
import random
import math
from Ant import *
from Stigmergic_space import *


class Env:

    def __init__(self, n_ants=10, evaporation_rate=1, stigmergic_radius=1, observation_range=2, map_size=30):
        self.map_size = map_size
        self.grid = np.empty((self.map_size, self.map_size))
        self.stigmergic_space = Stigmergic_space(evaporation_rate, stigmergic_radius, map_size)
        
        self.food_map = 0
        
        self.anthill = (math.floor(self.map_size/2) , math.floor(self.map_size/2))
        self.n_ants = n_ants
        self.ants = []
        self.action_range = 8        
        
        self.obs_range = observation_range
        
        self.set_env()

        self.graphic = gp.Graphic(self)

    def set_env(self):
        y = np.arange(self.map_size)
        x = y[:,np.newaxis]
        x0, y0 = self.anthill
        self.grid = self.map_size - (abs(x-x0) + abs(y-y0))
        self.create_food()
        self.create_ants()      

    def reset(self):
        self.stigmergic_space.clear()
        self.create_ants()
        self.create_food()
                
        obs = np.empty((self.n_ants, 3, self.obs_range*2+1, self.obs_range*2+1))
        for i in range(self.n_ants):
            obs[i] = self.ants[i].set()

        return obs


    def render(self):
        self.graphic.draw_env()


    def create_ants(self):
        self.ants = []
        for i in range(self.n_ants):
            self.ants.append(Ant(self))


    def create_food(self):
        self.food_map = np.zeros((self.map_size,self.map_size))
        food_index = np.array([[self.anthill[0], 5]])        
        self.food_map[tuple(food_index.T)] = 3


    def step(self, actions):
        rew = np.empty(self.n_ants)
        obs = np.empty((self.n_ants, 3, self.obs_range*2+1, self.obs_range*2+1))
        dones = np.empty(self.n_ants, dtype=bool)
        for i in range(len(actions)):
            rew[i], obs[i], dones[i] = self.ants[i].move(actions[i])
        self.stigmergic_space.handle_evaporation()
        
        return (rew, obs, dones)

    def pick_food(self, x, y):
        self.food_map[x,y] -= 1

    def count_food(self):
        return np.sum(self.food_map)
