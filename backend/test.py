from othello_env import OthelloEnv

env = OthelloEnv()
env.reset()
env.render()

env.step(20)  # (2, 3) などの有効な手を選択
env.render()

env.step(37) 
env.render()