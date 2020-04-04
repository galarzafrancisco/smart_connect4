import json
from modules.Agent import Agent
from modules.Game import Game
from modules.PlayABunchOfGames import PlayABunchOfGames
from modules.Model import Model

# Read metadata
with open('metadata.json', 'r') as f:
    metadata = json.load(f)


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



# Loop
while True:
    current_generation = metadata['latest_generation_trained']
    randomness, probablilistic = calculate_randomness(current_generation)

    # Make players
    agent_1 = Agent( # current gen
        player_id=1,
        player_colour='white',
        model='models/model_{}.h5'.format(current_generation) if current_generation > 1 else None
    )
    agent_1.set_randomness_level(randomness)
    agent_1.set_probabilistic_level(probablilistic)
    agent_2 = Agent( # previous gen
        player_id=2,
        player_colour='red',
        model='models/model_{}.h5'.format(current_generation - 1) if current_generation > 1 else None
    )
    agent_2.set_randomness_level(randomness)
    agent_2.set_probabilistic_level(probablilistic)
    players = [agent_1, agent_2]

    # Play a bunch of times
    print('Playing a bunch of times...')
    simulation = PlayABunchOfGames(
        players=players,
        loop=500
    )
    simulation.start()
    
    # Get the best moves
    print('Getting the best moves...')
    top_percentage = 0.1
    top_moves = simulation.get_top_moves(top_percentage=top_percentage)
    while len(top_moves) < 20 and top_percentage <= 1.0:
        top_percentage += 0.1
        top_moves = simulation.get_top_moves(top_percentage=top_percentage)
    print('Top moves percentage:', top_percentage)

    if len(top_moves) > 0:
        # Make a Model
        print('Training model...')
        model = Model(
            pretrained_model='models/model_{}.h5'.format(current_generation) if current_generation > 1 else None
        )
        model.train(
            moves=top_moves,
            epochs=10
        )
        model.save('models/model_{}.h5'.format(current_generation + 1))

        # Write metadata
        print('Training finished. Writing metadata...')
        metadata['latest_generation_trained'] = current_generation + 1
        with open('metadata.json', 'w') as f:
            f.write(json.dumps(metadata, indent=2))
        current_generation += 1
    else:
        print('Skipping training because no top_moves where returned')
