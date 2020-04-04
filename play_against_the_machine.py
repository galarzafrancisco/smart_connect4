from modules.Agent import Agent
from modules.Game import Game
import json

# Read metadata
with open('metadata.json', 'r') as f:
    metadata = json.load(f)
latest_generation_trained = metadata['latest_generation_trained']

def calculate_randomness(generation):
    if generation < 10:
        return 0.8, 0.2
    elif generation < 20:
        return 0.75, 0.25
    elif generation < 30:
        return 0.7, 0.3
    elif generation < 40:
        return 0.6, 0.4
    elif generation < 50:
        return 0.5, 0.4
    elif generation < 60:
        return 0.4, 0.4
    elif generation < 70:
        return 0.35, 0.35
    elif generation < 80:
        return 0.35, 0.3
    elif generation < 90:
        return 0.3, 0.3
    elif generation < 100:
        return 0.3, 0.25
    else:
        return 0.3, 0.2
        
randomness, probablilistic = calculate_randomness(latest_generation_trained)

# Make players
agent_1 = Agent( # current gen
    player_id=1,
    player_colour='white',
    model='models/model_{}.h5'.format(latest_generation_trained) if latest_generation_trained > 1 else None
)
agent_1.set_randomness_level(randomness)
agent_1.set_probabilistic_level(probablilistic)
agent_2 = Agent( # previous gen
    player_id=2,
    player_colour='red',
    model='models/model_{}.h5'.format(latest_generation_trained - 1) if latest_generation_trained > 1 else None
)
agent_2.set_randomness_level(randomness)
agent_2.set_probabilistic_level(probablilistic)

players = [agent_1, agent_2]

# Make game
game = Game(
    players=players,
    print_board_state=True,
    print_board_delay=1,
    clear_screen_before_printing_board=True
)
game.start()
if game.winner:
    print('Player {} won'.format(game.winner))
    print('Q moves: {}'.format(game.move_number))