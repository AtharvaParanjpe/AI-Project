from Environment import *
from BasicAgent import *
from ITAgent import *
from ITAgentKnowMinesN import *
from BonusAgent import *
# Generate a board b
d = 25
mine_density = 40
times = 50
# Generate an agent
score_it = 0
score_b = 0
score_itmn = 0
score_bonus = 0

for i in range(0,times):
	b = Board(d,mine_density)
	# agent = ITAgentKnowMinesN(b)
	# score_itmn = score_itmn+agent.select_cells()
	# agent = ITAgent(b)
	# score_it = score_it+agent.select_cells()
	# agent = BasicAgent(b)
	# score_b = score_b+agent.select_cells()
	agent = BonusAgent(b)
	score_bonus = score_bonus+agent.select_cells()

# print(score_itmn/times)
# print(score_it/times)
# print(score_b/times)
print(score_bonus/times)