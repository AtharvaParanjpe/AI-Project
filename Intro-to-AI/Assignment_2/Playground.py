from Environment import *
from BasicAgent import *
from ITAgent import *
# Generate a board b
b = Board(10,20)
# Generate an agent
agent = ITAgent(b)
# The agent do a random selections on the board
print(agent.select_cells())