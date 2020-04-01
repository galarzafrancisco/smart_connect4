import json, time, os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from play import Player, Board, Game
from train import Model, Agent

# Read metadata
with open('metadata.json', 'r') as f:
    metadata = json.load(f)
latest_generation_trained = metadata['latest_generation_trained']

# Load model
model1 = load_model('models/model_{}.h5'.format(latest_generation_trained - 1))
model2 = load_model('models/model_{}.h5'.format(latest_generation_trained))

agent1 = Agent(model1).agent
agent2 = Agent(model2).agent
p1 = Player(
    name=1.0,
    agent=agent1,
    exploration=0,
    version=latest_generation_trained-1
)
p2 = Player(
    name=2.0,
    agent=agent2,
    exploration=0,
    version=latest_generation_trained
)
board = Board()
players = [p1, p2]
turn = int(np.trunc(np.random.random() * len(players)))
while board.has_won() == False and board.can_play() == True:
    # Select player
    this_player = players[turn]
    # Choose a number to play
    choice = this_player.play(board.state)
    while board._validate_move(choice) == False:
        choice = this_player.play(board.state)
    os.system('clear')
    print('\nPlayer {} (v{})- Choice: {}'.format(this_player.name, this_player.version, choice))
    # Play
    board.play(this_player.name, choice)
    board.print_board()
    if board.has_won():
        this_player.get_points(1)
        print('\nPlayer {} won'.format(this_player.name))

    # Increase the turn
    turn += 1
    if turn >= len(players):
        turn=0

    time.sleep(1)
    
