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
    os.system('clear')
    # Load models to play
    model1 = load_model('models/model_{}.h5'.format(current_generation))
    model2 = load_model('models/model_{}.h5'.format(current_generation - 1))
    agent1 = Agent(model1).agent
    agent2 = Agent(model2).agent
    # Play
    print('Playing generation {} vs {}...'.format(current_generation, current_generation - 1))
    simulation = Simulation(
        loops=5000,
        agents=[agent1, agent2],
        exploration=0.3
    )
    simulation.start()
    winner_moves = simulation.get_winner_moves()
    print('Game finished. We collected {} winner moves!'.format(len(winner_moves)))
    # Train
    print('Training new generation...')
    new_model = Model()
    new_trained_model = new_model.train(winner_moves)
    new_model.save('models/model_{}.h5'.format(current_generation + 1))
    # Write metadata
    print('Training finished. Writing metadata...')
    metadata['latest_generation_trained'] = current_generation + 1
    with open('metadata.json', 'w') as f:
        f.write(json.dumps(metadata, indent=2))
    current_generation += 1


