import json, time, os
from play import Simulation
from train import Agent, Model
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model

# Read metadata
with open('metadata.json', 'r') as f:
    metadata = json.load(f)


while True:
    current_generation = metadata['latest_generation_trained']
    # Clean screen
    # os.system('clear')
    # Load models to play
    try:
        model1 = load_model('models/model_{}.h5'.format(current_generation))
        model2 = load_model('models/model_{}.h5'.format(current_generation - 1))
        agent1 = Agent(model1, probabilistic_prediction=0.3).agent
        agent2 = Agent(model2, probabilistic_prediction=0.3).agent
    except:
        model1 = None
        model2 = None
        agent1 = None
        agent2 = None
    # Play
    print('Playing generation {} vs {}...'.format(current_generation, current_generation - 1))
    simulation = Simulation(
        loops=100,
        agents=[agent1, agent2],
        exploration=0.2
    )
    simulation.start()
    winner_moves = simulation.get_winner_moves()
    print('Game finished. We collected {} winner moves!'.format(len(winner_moves)))
    # Train
    print('Training new generation...')
    new_model = Model(pretrained_model=model1)
    new_trained_model = new_model.train(
        moves=winner_moves,
        epochs=100
    )
    new_model.save('models/model_{}.h5'.format(current_generation + 1))
    # Write metadata
    print('Training finished. Writing metadata...')
    metadata['latest_generation_trained'] = current_generation + 1
    with open('metadata.json', 'w') as f:
        f.write(json.dumps(metadata, indent=2))
    current_generation += 1


