import pygame 
import random 
import config
# ===============================================================

#initialize screen
screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

# ===============================================================
#Visualization
def drawAgent(agentPos):
	pygame.draw.circle(screen, config.RED, agentPos, config.AGENT_SIZE)
    
def drawPerson(personPos):
	pygame.draw.circle(screen, config.BLUE, personPos, config.PERSON_SIZE)

def drawObstacle(obstaclePos):
	obstacle = pygame.Rect(obstaclePos[0], obstaclePos[1], config.OBSTACLE_WIDTH, config.OBSTACLE_HEIGHT)
	pygame.draw.rect(screen, config.YELLOW, obstacle)

def drawGoal(goalPos):
	goal = pygame.Rect(goalPos[0], goalPos[1], config.GOAL_WIDTH, config.GOAL_HEIGHT)
	pygame.draw.rect(screen, config.GREEN, goal)
# =========================================================================
#Update the agent position
def updateAgent(action, agentPos):
	# Assume Action is scalar:  0:stay, 1:Up, 2:Down 3:Left 4:Right
	agentXPos = agentPos[0]
	agentYPos = agentPos[1]
	
	#if move up
	if (action == 1):
		agentYPos = agentPos[1] + config.AGENT_SPEED	
	#if move down
	if (action == 2):
		agentYPos = agentPos[1] - config.AGENT_SPEED
	#if move right
	if (action == 3):
		agentXPos = agentPos[0] + config.AGENT_SPEED
	#if move left
	if (action == 4):
		agentXPos = agentPos[0] - config.AGENT_SPEED

	#don't let it move off the screen
	if (agentPos[0] < 0 + config.AGENT_SIZE):
		agentXPos = 0 + config.AGENT_SIZE
	if (agentPos[1] < 0 + config.AGENT_SIZE):
		agentYPos = 0 + config.AGENT_SIZE
	if (agentPos[0] > config.WINDOW_WIDTH - config.AGENT_SIZE):
		agentXPos = config.WINDOW_WIDTH - config.AGENT_SIZE
	if (agentPos[1] > config.WINDOW_HEIGHT - config.AGENT_SIZE):
		agentYPos = config.WINDOW_HEIGHT - config.AGENT_SIZE

	agentPos = (agentXPos, agentYPos)
	return agentPos
# =========================================================================
#Update the person position, using the agent posistions
def updatePerson(agentPos, obstaclePos, personPos):
	personXPos = personPos[0]
	personYPos = personPos[1]
	
	# move around agent nearby
	if abs(agentPos[0] - personPos[0]) < 50 and abs(agentPos[1] - personPos[1]) < 50:

		if agentPos[0] > personPos[0]:
			personXPos = personPos[0] - config.PERSON_SPEED
		elif agentPos[0] < personPos[0]:
			personXPos = personPos[0] + config.PERSON_SPEED

		if agentPos[1] > personPos[1]:
			personYPos = personPos[1] - config.PERSON_SPEED
		elif agentPos[1] < personPos[1]:
			personYPos = personPos[1] + config.PERSON_SPEED

	# move around obstacle nearby
	if abs(obstaclePos[0] - personPos[0]) < config.OBSTACLE_WIDTH  * 0.5 - config.PERSON_SIZE and abs(obstaclePos[1] - personPos[1]) < config.GOAL_HEIGHT * 0.5 - config.PERSON_SIZE:

		if obstaclePos[0] > personPos[0]:
			personXPos = personPos[0] - config.PERSON_SPEED
		elif obstaclePos[0] < personPos[0]:
			personXPos = personPos[0] + config.PERSON_SPEED

		if obstaclePos[1] > personPos[1]:
			personYPos = personPos[1] - config.PERSON_SPEED
		elif obstaclePos[1] < personPos[1]:
			personYPos = personPos[1] + config.PERSON_SPEED

	# move around whenever there isn't the agent nearby
	# else:
	# 	choice = random.randint(1, 5)
	# 	if choice == 1:
	# 		personXPos = personPos[0] + int(random.randint(1, config.PERSON_SPEED) * 1.0)
	# 	elif choice == 2:
	# 		personYPos = personPos[1] + int(random.randint(1, config.PERSON_SPEED) * 1.0)
	# 	elif choice == 3:
	# 		personXPos = personPos[0] - int(random.randint(1, config.PERSON_SPEED) * 1.0)
	# 	elif choice == 4:
	# 		personYPos = personPos[1] - int(random.randint(1, config.PERSON_SPEED) * 1.0)
	# 	elif choice == 5:
	# 		pass
	
	#don't let it move off the screen
	if (personPos[0] < 0 + config.PERSON_SIZE*4):
		personXPos = 0 + config.PERSON_SIZE*4
	if (personPos[1] < 0 + config.PERSON_SIZE*4):
		personYPos = 0 + config.PERSON_SIZE*4
	if (personPos[0] > config.WINDOW_WIDTH - config.PERSON_SIZE*4):
		personXPos = config.WINDOW_WIDTH - config.PERSON_SIZE*4
	if (personPos[1] > config.WINDOW_HEIGHT - config.PERSON_SIZE*4):
		personYPos = config.WINDOW_HEIGHT - config.PERSON_SIZE*4

	personPos = (personXPos, personYPos)
	return personPos
# =========================================================================
#Game class
class Rescue:
	def __init__(self):
		# Initialise pygame
		pygame.init()
		pygame.display.set_caption('Rescue DQN Experiment')

		self.agentPos = config.AGENT_INIT_POS
		self.personPos = config.PERSON_INIT_POS
		self.obstaclePos = config.OBSTACLE_POS
		self.goalPos = config.GOAL_POS

		self.clock = pygame.time.Clock()
		self.GTimeDisplay = 0
		self.success = 0
		self.score = 0
		self.GEpsilonDisplay = 1.0

		self.font = pygame.font.SysFont("calibri",20)
		
    # Initialise Game
	def InitialDisplay(self):
		#for each frame, calls the event queue, like if the main window needs to be repainted
		pygame.event.pump()
		#make the background config.black
		screen.fill(config.BLACK)
		#visualization
		drawAgent(self.agentPos)
		drawPerson(self.personPos)
		drawObstacle(self.obstaclePos)
		drawGoal(self.goalPos)
		#updates the window
		pygame.display.flip()

	# Episode reset
	def Reset(self):
		#visualization
		self.agentPos = config.AGENT_INIT_POS
		self.personPos = config.PERSON_INIT_POS
		self.obstaclePos = config.OBSTACLE_POS
		self.goalPos = config.GOAL_POS
		drawAgent(self.agentPos)
		drawPerson(self.personPos)
		drawObstacle(self.obstaclePos)
		drawGoal(self.goalPos)
		self.distance_prev_person_goal = self.distance(self.personPos,self.goalPos)
		self.distance_prev_agent_person = self.distance(self.agentPos,self.personPos)
		#updates the window
		pygame.display.flip()
		

	#  distance between two dots
	def distance(self,dot1,dot2):
		distance = ((dot1[0]-dot2[0])**2 + (dot1[1]-dot2[1])**2)**0.5
		return distance

    #  Game Update Inlcuding Display
	def PlayNextMove(self, action):
		score_1 = 0
		score_2 = 0
	
		pygame.event.pump()
		screen.fill(config.BLACK)

		#draw goal & obstacle
		drawObstacle(self.obstaclePos)
		self.obstacleXPos = self.obstaclePos[0]
		self.obstacleYPos = self.obstaclePos[1]
		drawGoal(self.goalPos)
		self.goalXPos = self.goalPos[0]
		self.goalYPos = self.goalPos[1]

		#update agent
		self.agentPos = updateAgent(action, self.agentPos)
		drawAgent(self.agentPos)
		self.agentXPos = self.agentPos[0]
		self.agentYPos = self.agentPos[1]
		
		#update person
		self.personPos = updatePerson(self.agentPos, self.obstaclePos, self.personPos)
		drawPerson(self.personPos)
		self.personXPos = self.personPos[0]
		self.personYPos = self.personPos[1]

		#goal arrived
		if abs(self.goalPos[0] - self.personPos[0]) < config.GOAL_WIDTH * 0.5 and abs(self.goalPos[1] - self.personPos[1]) < config.GOAL_HEIGHT * 0.5:
			condition = "success"
			self.score = 50.
		#obstacle collision
		elif abs(self.obstaclePos[0] - self.agentPos[0]) < config.OBSTACLE_WIDTH * 0.5 - config.AGENT_SIZE and abs(self.obstaclePos[1] - self.agentPos[1]) < config.OBSTACLE_HEIGHT * 0.5 - config.AGENT_SIZE:
			condition = "fail"
			self.score = - 5.

		#score based on distance
		else :
			condition = "none"
			if self.distance(self.personPos,self.goalPos) < self.distance_prev_person_goal:
				score_1 = 5.
			elif self.distance(self.personPos,self.goalPos) > self.distance_prev_person_goal:
				score_1 = - 0.5
			if self.distance(self.agentPos,self.personPos) < self.distance_prev_agent_person:
				score_2 = 0.05
			elif self.distance(self.agentPos,self.personPos) > self.distance_prev_agent_person:
				score_2 = - 0.01
			
			self.score = score_1 + score_2
			
			self.distance_prev_person_goal = self.distance(self.personPos,self.goalPos)
			self.distance_prev_agent_person = self.distance(self.agentPos,self.personPos)

		#  Display Parameters
		ScoreDisplay = self.font.render("Score: "+ str("{0:.2f}".format(self.score)), True,(255,255,255))
		screen.blit(ScoreDisplay,(400.,20.))
		EpisodeDisplay = self.font.render("Episode: "+ str(self.EpisodeDisplay), True,(255,255,255))
		screen.blit(EpisodeDisplay,(400.,40.))
		EpsilonDisplay = self.font.render("Epsilon: "+ str("{0:.2f}".format(self.GEpsilonDisplay)), True,(255,255,255))
		screen.blit(EpsilonDisplay,(400.,60.))
		SuccessDisplay = self.font.render("Success: "+ str(self.SuccessDisplay), True,(255,255,255))
		screen.blit(SuccessDisplay,(400.,80.))
		TimeDisplay = self.font.render("Time: "+ str(self.GTimeDisplay), True,(255,255,255))
		screen.blit(TimeDisplay,(400.,100.))

		#update the Game Display
		pygame.display.flip()

		#return the score and position of the agent and person 
		return [condition, self.score,self.agentXPos, self.agentYPos, self.personXPos, self.personYPos, self.obstacleXPos, self.obstacleYPos, self.goalXPos, self.goalYPos]
		
	def UpdateGameDisplay(self, Episode, Epsilon, Success, GTime):
		self.EpisodeDisplay = Episode
		self.GEpsilonDisplay = Epsilon
		self.SuccessDisplay = Success
		self.GTimeDisplay = GTime

