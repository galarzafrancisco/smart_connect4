from modules.Agent import Agent
from modules.Game import Game
import numpy as np



class PlayABunchOfGames():
    
    def __init__(self, players, loop=100):
        self.players = players
        self.loop = loop
        self.all_games_moves = [] # each element is [ q_moves, [ [board1, move1], [board2, move2] ] ]
    

    def start(self):
        for iteration in range(self.loop):
            print('\tplaying game {}/{}'.format(iteration, self.loop))
            # Make a game
            self.game = Game(
                players=self.players,
                print_board_state=False
            )
            self.game.start()
            if self.game.winner:
                winner_moves = self.game.get_winner_moves()
                self.all_games_moves.append([
                    self.game.move_number,
                    [[move['board_state'], move['move']] for move in winner_moves]
                ])
    

    def get_top_moves(self, top_percentage=1.0):
        """
        Returns the moves of the games that were won in less than the average number of moves
        Arguments:
        - top_percentage (float): games that finished in less than average_moves * top_percentage moves will be returned.
        """
        q_moves_list = [iteration[0] for iteration in self.all_games_moves]
        if len(q_moves_list) == 0:
            print('This is wrong. This should not happen. But guess what? It happened!')
        q_moves_average = sum(q_moves_list) / len(q_moves_list)
        threshold = np.ceil(q_moves_average * top_percentage)
        top_moves = []
        for game_moves in self.all_games_moves:
            if game_moves[0] < threshold:
                top_moves += game_moves[1]
        print('Average number of moves:', q_moves_average)
        print('\tThreshold: {}\tQ top moves: {}', threshold, len(top_moves))
        return top_moves