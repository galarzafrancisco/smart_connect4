"""
An agent is a virtual player. It makes a decision based on the state of the board.
"""

import numpy as np
from tensorflow.keras.models import load_model



class Random_Model():
    def __init__(self):
        pass
    def predict(self, board_states):
        """
        Generates a random move.
        Arguments:
        - board_states (3D numpy array): a numpy array of numpy arrays showing the board
        Returns:
        - an array of probability arrays (2D numpy array) a move (random integer in the range of 0 to x size of the board)
        """
        random_probability_array = np.random.random(board_states[0].shape[1])
        random_probability_array = random_probability_array / np.sum(random_probability_array)
        return np.array([random_probability_array])




class Agent():


    def __init__(self, player_id, player_colour=None, model=None):
        """
        Init the class.
        Arguments:
        - player_id (integer)
        - player_colour (string): colour of the player to be used when displaying the board.
           - white
           - red
           - blue
           - yellow
           - None: a colour will be automatically assigned
        - model: model used to generate the moves. This could be:
           - a tensorflow model
           - a string pointing to the model location on disk
           - None to generate random moves
        """
        self.player_id = player_id
        if model is None:
            # Model has not been provided. Make a model that generates random choices.
            self.model = Random_Model()
        elif type(model) is str:
            # A string pointing to the model on disk was provided. Load the model.
            self.model = self._load_model(model)
        else:
            # A TensorFlow model was provided.
            self.model = model
        self.randomness_level = 0.0
        self.probabilistic_level = 0.0
        if player_colour is None:
            player_colour = ['black', 'white', 'red', 'blue', 'yellow'][int(player_id)]
        self.colour = {
            'white': '⚪️',
            'black': '⚫️',
            'red': '🔴',
            'blue': '🔵',
            'yellow': '🔶'
        }.get(player_colour)


    def _load_model(self, model_path):
        """
        Loads a TensorFlow model.
        Arguments:
        - model_path (string): path to the model on disk
        Returns:
        - a TensorFlow model
        """
        return load_model(model_path)

    
    def set_probabilistic_level(self, probabilistic_level):
        """
        Sets the probability of getting a random move.
        Arguments:
        - probabilistic_level (float): the probability of getting a random move
        Returns:
        - None
        """
        self.probabilistic_level = probabilistic_level


    def set_randomness_level(self, randomness_level):
        """
        Sets the probability of getting a random move.
        Arguments:
        - randomness_level (float): the probability of getting a random move
        Returns:
        - None
        """
        self.randomness_level = randomness_level


    def _prepare_board_for_prediction(self, board_state):
        """
        The model is trained with 1.0 as the current player, 0.5 as the other player and 0.0 as an empty space.
        This function transform the board to match that definition.
        Arguments:
        - board_state (2D numpy array): a numpy array showing the board
        Returns:
        - the transformed board (2D numpy array)
        """
        index_of_this_player = board_state == self.player_id
        index_of_empty = board_state == 0
        processed_board = np.ones_like(board_state, dtype=float) * 0.5
        processed_board[index_of_empty] = 0.0
        processed_board[index_of_this_player] = 1.0
        return processed_board


    def play(self, board_state):
        """
        Generates a move based on the board state.
        Arguments:
        - board_state (2D numpy array): a numpy array showing the board
        Returns:
        - a move (integer)
        - move type (string): string representing how the move was selected. Could be 'random' or 'model'.
        """
        move_type_random_number = np.random.random()
        if move_type_random_number < self.randomness_level:
            # Random move
            move = int(np.trunc(np.random.random() * board_state.shape[1]))
            # print('Random prediction:', move)
            return (
                move,
                'random',
                1/board_state.shape[1]
            )
        else:
            # Make a prediction
            processed_board = self._prepare_board_for_prediction(board_state)
            moves_probability_array = self.model.predict(np.array([processed_board]))[0]
            
            move_type_random_number = move_type_random_number - self.randomness_level
            if move_type_random_number < self.probabilistic_level:
                # Probabilistic random move
                move = 0
                random_number = np.random.random()
                while random_number > moves_probability_array[move] and move < len(moves_probability_array)-1:
                    random_number = random_number - moves_probability_array[move]
                    move += 1
                # print('Probabilistic prediction:', move)
                return (
                    move,
                    'probabilistic_random',
                    moves_probability_array[move]
                )
            else:
                # Return the most probable move
                move = int(np.argmax(moves_probability_array))
                # print('Model prediction:', move)
                return (
                    move,
                    'model',
                    moves_probability_array[move]
                )