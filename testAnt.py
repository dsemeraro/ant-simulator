from Env import *

env = Env(n_ants=1, observation_range=1, map_size=20)
for i in range(10):
    rew, obs, done = env.step([4])
    print("osservazioni mappa:\n", obs[0,0])
    print("osservazioni spazio stigmergico:\n", obs[0,1])
    print("osservazioni mappa cibo:\n", obs[0,2])
    print("reward: ", rew)
    env.render()
    input()
