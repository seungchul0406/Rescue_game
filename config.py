FPS = 10000	#  Experiment Performance Seems rather sensitive to Computer performance

#Size parameter
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
AGENT_SIZE = 10
PERSON_SIZE = 10
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 20
GOAL_WIDTH = 150
GOAL_HEIGHT = 150

#RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

#Velocity of agent and person
PERSON_SPEED = 2
AGENT_SPEED = 3

#Initialie positions
AGENT_INIT_POS = (15,15)
PERSON_INIT_POS = (55,55)

#Goal and obstacle position
OBSTACLE_POS = (150,350)
GOAL_POS = (425,425)

#   DQN Algorith Paramaters 
ACTIONS = 5 # Number of Actions.  Acton istelf is a scalar:  0:stay, 1:Up, 2:Down 3:Right 4.Left
STATECOUNT = 4 # Size of State [agentXPos, agentYPos, personXPos, personYPos] 
MAX_EPISODE = 100000
MAX_GAMETIME = 1500

#   DQN Algorith Hyper Paramaters 
ExpReplay_CAPACITY = 2000
OBSERVEPERIOD = 10000000		# Period actually start real Training against Experieced Replay Batches 
BATCH_SIZE = 128
GAMMA = 0.95				# Q Reward Discount Gamma
MAX_EPSILON = 1
MIN_EPSILON = 0.05
LAMBDA = 0.0005      		# Speed of Epsilon decay