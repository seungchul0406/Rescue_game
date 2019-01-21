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
def updateAgent(action, agentPos, dft):
	# Assume Action is scalar:  0:stay, 1:Up, 2:Down 3:Left 4:Right
	dft =7
	agentXPos = agentPos[0]
	agentYPos = agentPos[1]
	
	#if move up
	if (action == 1):
		agentYPos = agentPos[1] + config.AGENT_SPEED*dft	
	#if move down
	if (action == 2):
		agentYPos = agentPos[1] - config.AGENT_SPEED*dft
	#if move right
	if (action == 3):
		agentXPos = agentPos[0] + config.AGENT_SPEED*dft
	#if move left
	if (action == 4):
		agentXPos = agentPos[0] - config.AGENT_SPEED*dft

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
def updatePerson(agentPos, obstaclePos, personPos, dft):
	dft =7
	personXPos = personPos[0]
	personYPos = personPos[1]
	
	# move around agent nearby
	if abs(agentPos[0] - personPos[0]) < 50 and abs(agentPos[1] - personPos[1]) < 50:

		if agentPos[0] > personPos[0]:
			personXPos = personPos[0] - config.PERSON_SPEED*dft
		elif agentPos[0] < personPos[0]:
			personXPos = personPos[0] + config.PERSON_SPEED*dft

		if agentPos[1] > personPos[1]:
			personYPos = personPos[1] - config.PERSON_SPEED*dft
		elif agentPos[1] < personPos[1]:
			personYPos = personPos[1] + config.PERSON_SPEED*dft

	# move around obstacle nearby
	if abs(obstaclePos[0] - personPos[0]) < config.OBSTACLE_WIDTH * 0.5 and abs(obstaclePos[1] - personPos[1]) < config.GOAL_HEIGHT * 0.5:

		if obstaclePos[0] > personPos[0]:
			personXPos = personPos[0] - config.PERSON_SPEED*dft
		elif obstaclePos[0] < personPos[0]:
			personXPos = personPos[0] + config.PERSON_SPEED*dft

		if obstaclePos[1] > personPos[1]:
			personYPos = personPos[1] - config.PERSON_SPEED*dft
		elif obstaclePos[1] < personPos[1]:
			personYPos = personPos[1] + config.PERSON_SPEED*dft

	# move around whenever there isn't the agent nearby
	else:
		choice = random.randint(1, 5)
		if choice == 1:
			personXPos = personPos[0] + int(random.randint(1, 5) * 1.0)
		elif choice == 2:
			personYPos = personPos[1] + int(random.randint(1, 5) * 1.0)
		elif choice == 3:
			personXPos = personPos[0] - int(random.randint(1, 5) * 1.0)
		elif choice == 4:
			personYPos = personPos[1] - int(random.randint(1, 5) * 1.0)
		elif choice == 5:
			pass
	
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
# =========================================================================812NZSJ037550
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
		#updates the window
		pygame.display.flip()
		self.distance_prev = self.distance()
		self.distance_2_prev = self.distance_2()

	#  distance between goal and person
	def distance(self):
		distance = ((self.goalPos[0]-self.personPos[0])**2 + (self.goalPos[1]-self.personPos[1])**2)**0.5
		# print("distance : ",distance)
		return distance

	#  distance between person and agent
	def distance_2(self):
		distance_2 = ((self.personPos[0]-self.agentPos[0])**2 + (self.personPos[1]-self.agentPos[1])**2)**0.5
		# print("distance : ",distance)
		return distance_2
	
	#  Reset condition check
	def Condition(self):
		score_1 = 0
		score_2 = 0
		#goal arrived
		if abs(self.goalPos[0] - self.personPos[0]) < config.GOAL_WIDTH and abs(self.goalPos[1] - self.personPos[1]) < config.GOAL_HEIGHT:
			condition = "success"
			self.score = 50.
		#obstacle collision
		elif abs(self.obstaclePos[0] - self.agentPos[0]) < config.OBSTACLE_WIDTH and abs(self.obstaclePos[1] - self.agentPos[1]) < config.OBSTACLE_HEIGHT:
			condition = "fail"
			self.score = - 5.

		#score based on distance
		else :
			condition = "none"
			if self.distance() < self.distance_prev:
				score_1 = 0.1
			elif self.distance() > self.distance_prev:
				score_1 = - 0.1
			if self.distance_2() < self.distance_2_prev:
				score_2 = 0.01
			elif self.distance_2() > self.distance_2_prev:
				score_2 = - 0.01
			# score_3 = - self.GTimeDisplay * 0.0001
			self.score = score_1 + score_2
			# print(score_1,score_2)
			
			self.distance_prev = self.distance()
			self.distance_2_prev = self.distance_2()
		
		return condition, self.score


    #  Game Update Inlcuding Display
	def PlayNextMove(self, action):
		# Calculate DeltaFrameTime
		DeltaFrameTime = self.clock.tick(config.FPS)
	
		pygame.event.pump()
		screen.fill(config.BLACK)

		#draw goal & obstacle
		drawObstacle(self.obstaclePos)
		drawGoal(self.goalPos)

		#update agent
		self.agentPos = updateAgent(action, self.agentPos, DeltaFrameTime)
		drawAgent(self.agentPos)
		self.agentXPos = self.agentPos[0]
		self.agentYPos = self.agentPos[1]
		
		#update person
		self.personPos = updatePerson(self.agentPos, self.obstaclePos, self.personPos, DeltaFrameTime)
		drawPerson(self.personPos)
		self.personXPos = self.personPos[0]
		self.personYPos = self.personPos[1]

		#  Display Parameters
		ScoreDisplay = self.font.render("Score: "+ str("{0:.2f}".format(self.score)), True,(255,255,255))
		screen.blit(ScoreDisplay,(400.,20.))
		EpisodeDisplay = self.font.render("Episode: "+ str(self.EpisodeDisplay), True,(255,255,255))
		screen.blit(EpisodeDisplay,(400.,40.))
		EpsilonDisplay = self.font.render("Ep: "+ str("{0:.2f}".format(self.GEpsilonDisplay)), True,(255,255,255))
		screen.blit(EpsilonDisplay,(400.,60.))
		SuccessDisplay = self.font.render("Success: "+ str(self.SuccessDisplay), True,(255,255,255))
		screen.blit(SuccessDisplay,(400.,80.))
		TimeDisplay = self.font.render("Time: "+ str(self.GTimeDisplay), True,(255,255,255))
		screen.blit(TimeDisplay,(400.,100.))

		#update the Game Display
		pygame.display.flip()

		#return the score and position of the agent and person 
		return [self.score,self.agentXPos, self.agentYPos, self.personXPos, self.personYPos]
		
	def UpdateGameDisplay(self, Episode, Epsilon, Success, GTime):
		self.EpisodeDisplay = Episode
		self.GEpsilonDisplay = Epsilon
		self.SuccessDisplay = Success
		self.GTimeDisplay = GTime

