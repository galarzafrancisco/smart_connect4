from Game import Game
from Agent import Agent

# Make agents
agent_1 = Agent(player_id=1)
agent_1.set_randomness(0.3)
agent_2 = Agent(player_id=2)
agent_2.set_randomness(0.3)

# Make game
game = Game(
    players = [agent_1, agent_2]
)
game.start()
print('winner:', game.winner)
print('Board:')
print(game.board.state)
print('q_moves', game.move_number)
print('moves')
print(game.moves_history)
game.print_board()

print(game.player_id_to_player_map)