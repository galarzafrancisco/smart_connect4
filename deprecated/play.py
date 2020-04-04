import numpy as np
import time

BOARD_SIZE=(6,6) # y,x
SLEEP=0



class Board():
    def __init__(self):
        self.state = np.zeros(BOARD_SIZE)

    def has_won(self):
        """
        Returns the player that won, or False otherwise
        """
        winner = False
        # Look for horizontal lines
        for y in range(BOARD_SIZE[0]):
            for x in range(BOARD_SIZE[1]-3):
                line = self.state[y, x:x+4]
                unique_players_in_line = np.unique(line)
                if unique_players_in_line.size == 1:
                    if unique_players_in_line[0] != 0:
                        return unique_players_in_line[0]

        # Look for vertical lines
        for x in range(BOARD_SIZE[1]):
            for y in range(BOARD_SIZE[0]-3):
                line = self.state[y:y+4, x]
                unique_players_in_line = np.unique(line)
                if unique_players_in_line.size == 1:
                    if unique_players_in_line[0] != 0:
                        return unique_players_in_line[0]

        # Look for diagonal lines (y=x+b)
        for x in range(BOARD_SIZE[1]-3):
            for y in range(BOARD_SIZE[0]-3):
                line = np.array([self.state[y+i, x+i] for i in range(4)])
                unique_players_in_line = np.unique(line)
                if unique_players_in_line.size == 1:
                    if unique_players_in_line[0] != 0:
                        return unique_players_in_line[0]

        # Look for diagonal lines (y=-x+b)
        for x in range(3,BOARD_SIZE[1],1):
            for y in range(BOARD_SIZE[0]-3):
                line = np.array([self.state[y+i, x-i] for i in range(4)])
                unique_players_in_line = np.unique(line)
                if unique_players_in_line.size == 1:
                    if unique_players_in_line[0] != 0:
                        return unique_players_in_line[0]

        return winner
    
    def can_play(self):
        """
        Returns True if there are moves available
        """
        top_row = self.state[0]
        return np.any(top_row == 0)

    def play(self, player, move):
        """
        Puts a piece in one of the columns
        """
        if not self._validate_move(move):
            print('Move {} not valid'.format(move))
            return False
        x = move
        y = BOARD_SIZE[0]-1
        while y >= 0 and self.state[y, x] != 0:
            y -= 1
        if y >= 0:
            self.state[y, x] = player
            return self.state
        else:
            print('Move {} is out of range (stack overflow)'.format(move))
            return False
    
    def print_board(self):
        colours = {
            '0': "⚫️",
            '1': "⚪️",
            '2': "🔴"
        }
        b = '\n'.join([''.join([colours[str(int(v))] for v in row]) for row in self.state])
        print(b)

    def _validate_move(self, move):
        """
        Checks if the move is valid and returns True if it is
        """
        return self.state[0,move] == 0



class Player():
    """
    name: a number to identify the player.
    agent: a function that returns a number to play. Takes as an argument the state of the board.
    exploration: the probability of making a random move
    """
    def __init__(self, name, agent=None, exploration=1.0, version=None):
        self.name=name
        if agent == None:
            # If no agent is provided, generate a random choice
            self.agent=lambda board_state: int(np.trunc(np.random.random() * board_state.shape[1]))
        else:
            self.agent=agent
        self.exploration=exploration
        self.score=0
        self.version=version
    
    def play(self, board_state):
        if np.random.random() < self.exploration:
            return int(np.trunc(np.random.random() * board_state.shape[1]))
        else:
            my_index = board_state == self.name
            opponent_index = np.logical_and(board_state != self.name, board_state != 0)
            normalized_board = np.array(board_state, copy=True)
            normalized_board[my_index] = 1.0
            normalized_board[opponent_index] = 1.0
            return self.agent(normalized_board)
    
    def get_points(self, points):
        self.score += points



class Game():
    def __init__(self, players):
        self.players = players
        self.board = Board()
        self.turn = int(np.trunc(np.random.random() * len(players)))
        self.iterations = []
        self.winner_iterations = []
        self.winner = None
        self.q_moves = 0
    
    def start(self):
        while self.board.has_won() == False and self.board.can_play() == True:
            # Select player
            this_player = self.players[self.turn]
            # Choose a number to play
            choice = this_player.play(self.board.state)
            while self.board._validate_move(choice) == False:
                choice = this_player.play(self.board.state)
            # Store the current state of the board and the move made
            self.iterations.append((this_player.name, np.array(self.board.state, copy=True), choice)) # (player, board state, move)
            # Play
            self.board.play(this_player.name, choice)
            self.q_moves += 1
            if self.board.has_won():
                this_player.get_points(1)

            # Increase the turn
            self.turn += 1
            if self.turn >= len(self.players):
                self.turn=0

        # self.board.print_board()
        self.winner = self.board.has_won()
        if self.winner != False:
            # print('Winner: player {}'.format(self.winner))
            return(self.winner)
        else:
            # print('No more moves available')
            pass

    def get_winner_moves(self):
        for iteration in self.iterations:
            if iteration[0] == self.winner: # player
                winner_index = iteration[1] == self.winner # board state
                loser_index = np.logical_and(iteration[1] != self.winner, iteration[1] != 0)
                iteration[1][winner_index] = 1.0
                iteration[1][loser_index] = 0.5
                self.winner_iterations.append(iteration)
        return {
            'q_moves': self.q_moves,
            'moves': self.winner_iterations
        }



class Simulation():
    def __init__(self, loops=1000, agents=[None, None], exploration=1.0):
        self.loops = loops
        self.agents = agents
        self.players_names = [1, 2]
        self.exploration = exploration
        self.players = [
            Player(
                player_name,
                agent,
                self.exploration
            ) for player_name, agent in zip(self.players_names, self.agents)
        ]
        self.winner_moves = []
        
    def start(self):
        for i in range(self.loops):
            print('\tPlaying game {} of {}'.format(i, self.loops))
            try:
                game = Game(self.players)
                game.start()
                for winner_move in game.get_winner_moves():
                    self.winner_moves.append([winner_move[1], winner_move[2]])
            except Exception as e:
                print('Error in game {}'.format(i))
                print(e)
    
    def get_winner_moves(self, best=True):
        if best:
            np.array([int(m['q_moves']) for m in self.winner_moves])
        return self.winner_moves

    def save_winner_moves_as_csv(self, file_path):
        pass


if __name__ == "__main__":
    simulation = Simulation(loops=5000)
    simulation.start()
    print(simulation.get_winner_moves())