from Environment import board
from Agent import agent
# Generate a board b
b = board(10,30)
# Generate an agent
agent = agent(b)
# The agent do a random selections on the board
agent.SelectRandomCells()