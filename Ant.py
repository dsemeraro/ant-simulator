import numpy as np
#action list:
#0: right
#1: up-right
#2: up
#3: up-left
#4: left
#5: down-left
#6: down
#7: down-right

class Ant:
    def __init__(self, env):
        #x: row, y: column
        self.x, self.y = env.anthill
        self.food = False
        self.env = env      
        
    def set(self):
        obs = self.set_observation()
        return obs

    def move(self, action):
        
        rew = 0
        done = False
        if self.food:
            self.env.stigmergic_space.release_pheromone(self.x, self.y)

        direction = self.set_direction(action)

        if self.isIllegal(direction):
            rew = -10
        else:
            self.x += direction[0]
            self.y += direction[1]

            if self.env.food_map[self.x, self.y] != 0 and not self.food:
                self.food = True
                self.env.pick_food(self.x, self.y)
                rew = 10
            if (self.x, self.y) == self.env.anthill and self.food:           
                rew = 20
                done = True

        obs = self.set_observation()
        return (rew, obs, done) 

    def set_direction(self, action):
        direction = [0,0]
        if action == 7 or action == 0 or action == 1: #right
            direction[1] += 1
        if action == 1 or action == 2 or action == 3: #up
            direction[0] += -1
        if action == 4 or action == 3 or action == 5: #left
            direction[1] += -1
        if action == 5 or action == 6 or action == 7: #down
           direction[0] += 1
        return direction

    def isIllegal(self, direction):
        x = self.x + direction[0]
        y = self.y + direction[1]
        if x > self.env.map_size-1 or x < 0:
            return True
        if y > self.env.map_size-1 or y < 0:
            return True
        return False

#obs[0]: matrice quadrata di dimensione observation_range per l'ambiente che la formica vede
#obs[1]: matrice quadrata di dimensione observation_range per il feromone
#obs[2]: matrice quadrata di dimensione observation_range per il cibo
    def set_observation(self):
        obs_width = self.env.obs_range*2+1
        obs = np.full((3, obs_width, obs_width), -1)

        map_i_l, map_i_r, map_i_u, map_i_d = self.set_map_index()
        obs_i_l, obs_i_r, obs_i_u, obs_i_d = self.set_obs_index(obs_width)
        
        obs[0, obs_i_l:obs_i_r, obs_i_u:obs_i_d] = self.env.grid[map_i_l:map_i_r, map_i_u:map_i_d]
        obs[1, obs_i_l:obs_i_r, obs_i_u:obs_i_d] = self.env.stigmergic_space.map_pheromone[map_i_l:map_i_r, map_i_u:map_i_d]
        obs[2, obs_i_l:obs_i_r, obs_i_u:obs_i_d] = self.env.food_map[map_i_l:map_i_r, map_i_u:map_i_d]
        return obs

    def set_map_index(self):
        x_left = self.x - self.env.obs_range if self.x - self.env.obs_range >= 0 else 0
        x_right = self.x + self.env.obs_range + 1
        y_up = self.y - self.env.obs_range if self.y - self.env.obs_range >= 0 else 0
        y_down = self.y + self.env.obs_range + 1

        return x_left, x_right, y_up, y_down

    def set_obs_index(self, obs_width):
        l = 0 if (self.x - self.env.obs_range >= 0) else (self.env.obs_range - self.x)
        r = obs_width if (self.x + self.env.obs_range < self.env.map_size) else (obs_width - self.x + self.env.map_size - self.env.obs_range - 1)
        u = 0 if (self.y - self.env.obs_range >= 0) else (self.env.obs_range - self.y)
        d = obs_width if (self.y + self.env.obs_range < self.env.map_size) else (obs_width - self.y + self.env.map_size - self.env.obs_range - 1)

        return l, r, u, d
