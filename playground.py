
from modules.Agent import Agent
from modules.Game import Game
from modules.PlayABunchOfGames import PlayABunchOfGames
from modules.Model import Model

# Make players
agent_1 = Agent(
    player_id=1
)
agent_1.set_randomness(0.3)
agent_2 = Agent(
    player_id=2
)
agent_2.set_randomness(0.3)
players = [agent_1, agent_2]

simulation = PlayABunchOfGames(
    players=players,
    loop=20
)

simulation.start()
top_moves = simulation.get_top_moves()

# Make a Model
model = Model()
model.train(top_moves)
