"""
Initiates and plays a game. It uses the classes Agent and Board.
"""

from modules.Board import Board
import numpy as np
import os, time



class Game():
    def __init__(self, players, print_board_state=False, print_board_delay=1, clear_screen_before_printing_board=True):
        """
        Arguments:
        - players (list of Agents): agents to play the game
        """
        self.players = players
        self.print_board_state = print_board_state
        self.print_board_delay = print_board_delay
        self.clear_screen_before_printing_board = clear_screen_before_printing_board
        self.board = Board()
        self.turn = int(np.trunc(np.random.random() * len(players)))
        self.moves_history = []
        self.move_number = 0
        self.winner = None
        self.player_id_to_player_map = {
            player.player_id: player for player in self.players
        }
    

    def _next_turn(self):
        """
        Moves the turn to the next player
        Arguments: None
        Returns: None
        """
        self.turn += 1
        if self.turn >= len(self.players):
            self.turn = 0


    def start(self):
        """
        Kicks off the game.
        Arguments: None
        Returns:
        - ID of the winner or None otherwise
        """
        # Start the game loop
        while self.winner == None and self.board.can_play() == True:
            # Select player
            current_player = self.players[self.turn]
            # Make a move
            (move, move_type, move_probability) = current_player.play(self.board.state)
            attempts = 0
            while self.board._validate_move(move) == False:
                (move, move_type, move_probability) = current_player.play(self.board.state)
                attempts += 1
                if attempts >= 20:
                    print('Giving up.')
                    self.winner = None
                    self.board.print_board()
                    return None
            self.move_number += 1
            # Save the move
            self.moves_history.append(
                {
                    'player_id': current_player.player_id,
                    'board_state': np.array(self.board.state, copy=True),
                    'move': move,
                    'move_type': move_type,
                    'move_probability': move_probability,
                    'move_number': self.move_number,
                    'winner_move': False
                }
            )
            # Play
            self.board.play(current_player.player_id, move)
            self.winner = self.board.has_won()
            if self.board.has_won():
                self.moves_history[-1]['winner_move'] = True

            # Print board
            if self.print_board_state:
                if self.clear_screen_before_printing_board:
                    os.system('clear')
                self.print_board()
                print('Player: {}\nMove: {}\nMove type: {}\nProbability: {:.2f}%'.format(
                    current_player.player_id,
                    move,
                    move_type,
                    move_probability * 100
                ))
                time.sleep(self.print_board_delay)

            # Increase the turn
            self._next_turn()

        if self.winner != None:
            # print('Winner: player {}'.format(self.winner))
            self.moves_history[-1]['winner_move'] = True
            return self.winner
        else:
            # print('No more moves available')
            return self.winner


    def print_board(self):
        # Make map from player_id to colour
        colour_map = {player.player_id: player.colour for player in self.players}
        colour_map[0] = '⚫️'
        b= '\n'.join([''.join([colour_map[player_id] for player_id in row]) for row in self.board.state])
        print(b)


    def get_winner_moves(self):
        winner_moves = [move for move in self.moves_history if move['player_id'] == self.winner]
        normalised_moves = []
        winner_agent = self.player_id_to_player_map[self.winner]
        for winner_move in winner_moves:
            normalised_move = winner_move
            normalised_move['board_state'] = winner_agent._prepare_board_for_prediction(normalised_move['board_state'])
            normalised_moves.append(normalised_move)
        return normalised_moves
