import random

#Number of agent, person, and obstacle
AGENT_NUM = 3
PERSON_NUM = 5
OBSTACLE_NUM = 2

#Size parameter
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
AGENT_SIZE = 6
PERSON_SIZE = 6
OBSTACLE_MIN_WIDTH = 20
OBSTACLE_MAX_WIDTH = 80
OBSTACLE_MIN_HEIGHT = 20
OBSTACLE_MAX_HEIGHT = 80
GOAL_WIDTH = 50
GOAL_HEIGHT = 50

#RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

#Velocity of agent and person
PERSON_RAND_SPEED = 2
PERSON_SPEED = 4
AGENT_SPEED = 5

#Goalposition
GOAL_POS = (450,450)

#   DQN Algorith Paramaters 
ACTIONS = 5 # Number of Actions.  Acton istelf is a scalar:  0:stay, 1:Up, 2:Down 3:Right 4.Left
STATECOUNT = AGENT_NUM * 2 + PERSON_NUM * 2 + OBSTACLE_NUM * 2 + 2 #Size of State [agentXPos, agentYPos, personXPos, personYPos, obstacleXPos, obstacleYPos, goalXPos, goalYPos] 
MAX_EPISODE = 10000
MAX_GAMETIME = 100

#   DQN Algorith Hyper Paramaters 
ExpReplay_CAPACITY = 2000
OBSERVEPERIOD = 500		# Period actually start real Training against Experieced Replay Batches 
BATCH_SIZE = 128
GAMMA = 0.95				# Q Reward Discount Gamma
MAX_EPSILON = 1
MIN_EPSILON = 0.05
LAMBDA = 0.0005      		# Speed of Epsilon decay