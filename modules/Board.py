
BOARD_SIZE=(6,6) # y,x

import numpy as np




class Board():
    def __init__(self):
        self.state = np.zeros(BOARD_SIZE, dtype=int)

    def has_won(self):
        """
        Checks if a player has won.
        Arguments: None
        Returns:
        - the id of the player that won (int)
        - None otherwise
        """
        winner = None
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
        Checks if there are moves available in the board.
        - Arguments: None
        - Returns (bool) True/False if there are moves available or not.
        """
        top_row = self.state[0]
        return np.any(top_row == 0)


    def play(self, player_id, move):
        """
        Puts a piece in one of the columns
        Arguments:
        - player_id (int): ID of the player making the move
        - move (int): column number
        Returns:
        - False (bool) if the move is not valid
        - The new state of the board (2D numpy array)
        """
        # Validate the move
        if self._validate_move(move) == False:
            # print('Move {} not valid'.format(move))
            return False
        # Make the move
        x = move
        y = BOARD_SIZE[0]-1
        while y >= 0 and self.state[y, x] != 0:
            y -= 1
        if y >= 0:
            self.state[y, x] = player_id
            return self.state
        else:
            print('Move {} is out of range (stack overflow). This should not happen.'.format(move))
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