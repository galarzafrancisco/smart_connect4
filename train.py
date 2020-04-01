import json
from play import Simulation
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model


class Agent():
    def __init__(self, model):
        self.model = model
    def agent(self, board_state):
        reshaped_board = board_state.reshape((1, board_state.size))
        prediction_array = self.model.predict(reshaped_board)
        move = np.argmax(prediction_array)
        return move


class Model():
    def __init__(self, pretrained_model=None):
        self.pretrained_model = pretrained_model
        self.model = self.pretrained_model
    
    def train(self, moves, epochs=100):
        # Make x, y sets
        x = np.array([move[0] for move in moves])
        y = np.array([move[1] for move in moves])
        y_one_hot = np.zeros((y.shape[0], x[0].shape[1]))
        for i in range(y.shape[0]):
            y_one_hot[i, y[i]] = 1

        # Flatten x (transform the matrix representation of the board into a one-dimensional vector)
        x = np.array([np.reshape(i, i.size) for i in x])

        # Make train-test sets
        validation_idx = np.random.random(x.shape[0]) < 0.2
        train_idx = np.logical_not(validation_idx)
        x_train = x[train_idx]
        y_train = y_one_hot[train_idx]
        x_validation = x[validation_idx]
        y_validation = y_one_hot[validation_idx]
        
        # Train a model
        if self.model == None:
            self.model = keras.Sequential(
                layers=[
                    tf.keras.layers.Flatten(input_shape=x_train[0].shape),
                    tf.keras.layers.Dense(units=128, activation='relu'),
                    tf.keras.layers.Dense(units=60, activation='relu'),
                    tf.keras.layers.Dense(units=6, activation='softmax')
                ]
            )
            self.model.compile(
                loss='mean_squared_error',
                optimizer='adam'
            )
        self.model.fit(
            x=x_train,
            y=y_train,
            batch_size=32,
            epochs=epochs,
            validation_data=(x_validation, y_validation)
        )
        return self.model

    def save(self, path_to_save):
        self.model.save(path_to_save)