import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np

class Model():
    def __init__(self, pretrained_model=None):
        if pretrained_model == None:
            # Model has not been provided. Create one.
            self.model = self._make_model()
        elif type(pretrained_model) is str:
            # A string pointing to the model on disk was provided. Load the model.
            self.model = self._load_model(pretrained_model)
        else:
            # A TensorFlow model was provided.
            self.model = pretrained_model
        self.history = {}


    def _load_model(self, model_path):
        """
        Loads a TensorFlow model.
        Arguments:
        - model_path (string): path to the model on disk
        Returns:
        - a TensorFlow model
        """
        return load_model(model_path)


    def _make_model(self):
        """
        Makes a TensorFlow model
        """
        model = keras.Sequential(
            layers=[
                tf.keras.layers.Flatten(input_shape=(6,6)),
                tf.keras.layers.Dense(units=1024, activation='relu'),
                tf.keras.layers.Dense(units=128, activation='relu'),
                tf.keras.layers.Dense(units=6, activation='softmax')
            ]
        )
        model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )
        return model


    def train(self, moves, epochs=100, batch_size=32):
        """
        Trains a TensorFlow model.
        Arguments:
        - moves (numpy array): data to use during training
        - epochs (int)
        - batch_size (int)
        Returns: None
        """
        # Make x, y sets
        x = np.array([move[0] for move in moves]) # first element is the board_state (features)
        y = np.array([move[1] for move in moves]) # second element is the move (label)
        y_one_hot = np.zeros((y.shape[0], x[0].shape[1]))
        for i in range(y.shape[0]):
            y_one_hot[i, y[i]] = 1

        # Make train-validation sets
        validation_idx = np.random.random(x.shape[0]) < 0.2
        train_idx = np.logical_not(validation_idx)
        x_train = x[train_idx]
        y_train = y_one_hot[train_idx]
        x_validation = x[validation_idx]
        y_validation = y_one_hot[validation_idx]

        # Train
        self.history = self.model.fit(
            x=x_train,
            y=y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(x_validation, y_validation),
        )
        return self.model

    
    def save(self, path_to_save):
        self.model.save(path_to_save)
    
