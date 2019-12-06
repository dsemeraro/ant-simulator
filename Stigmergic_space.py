import numpy as np

class Stigmergic_space:
    def __init__(self, evaporation_rate, stigmergic_radius, map_size):
        self.map_pheromone = np.zeros((map_size, map_size))
        self.evaporation_rate = evaporation_rate
        self.stigmergic_radius = stigmergic_radius
        self.counter = 0

    def handle_evaporation(self):
        if self.counter == self.evaporation_rate:
            self.map_pheromone[self.map_pheromone > 0] -= 1
            self.counter = 0
        self.counter += 1
    
    def release_pheromone(self, x, y):
        self.map_pheromone[x,y] += 10
        if(self.stigmergic_radius > 0):
            self.map_pheromone[x-self.stigmergic_radius: x+self.stigmergic_radius+1,
                               y-self.stigmergic_radius: y+self.stigmergic_radius+1] += 5
    
    def clear(self):
        self.map_pheromone.fill(0)
