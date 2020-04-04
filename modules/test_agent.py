from Agent import Agent
import numpy as np

# Test agent loading
agent = Agent(
    player_id=1,
    player_colour='red',
    model=None
)

board_state = np.zeros((6,6), dtype=int)

# Play
print('Play with no randomness')
move = agent.play(board_state)
print(move)

# Set randomness
print('Play with 70% randomness')
agent.set_randomness(0.7)
for i in range(10):
    move = agent.play(board_state)
    print(move)
