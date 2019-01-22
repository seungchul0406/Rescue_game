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
	for i in range(config.AGENT_NUM):
		if abs(agentPos[i][0] - personPos[0]) < 50 and abs(agentPos[i][1] - personPos[1]) < 50:
			if agentPos[i][0] > personPos[0]:
				personXPos = personPos[0] - config.PERSON_SPEED
			elif agentPos[i][0] < personPos[0]:
				personXPos = personPos[0] + config.PERSON_SPEED

			if agentPos[i][1] > personPos[1]:
				personYPos = personPos[1] - config.PERSON_SPEED
			elif agentPos[i][1] < personPos[1]:
				personYPos = personPos[1] + config.PERSON_SPEED

	# move around obstacle nearby
	for i in range(config.OBSTACLE_NUM):
		if abs(obstaclePos[i][0] - personPos[0]) < config.OBSTACLE_WIDTH  - config.PERSON_SIZE and abs(obstaclePos[i][1] - personPos[1]) < config.OBSTACLE_HEIGHT - config.PERSON_SIZE:
			if obstaclePos[i][0] > personPos[0]:
				personXPos = personPos[0] - config.PERSON_SPEED
			elif obstaclePos[i][0] < personPos[0]:
				personXPos = personPos[0] + config.PERSON_SPEED

			if obstaclePos[i][1] > personPos[1]:
				personYPos = personPos[1] - config.PERSON_SPEED
			elif obstaclePos[i][1] < personPos[1]:
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
		self.agentPos = list()
		self.personPos = list()
		self.obstaclePos = list()
		for i in range(config.AGENT_NUM):
			self.agentPos.append((random.randint(0, 500), random.randint(0, 500)))
		for i in range(config.PERSON_NUM):
			self.personPos.append((random.randint(0, 500), random.randint(0, 500)))
		for i in range(config.OBSTACLE_NUM):
			self.obstaclePos.append((random.randint(0 + config.OBSTACLE_WIDTH * 0.5, 500 - config.OBSTACLE_WIDTH * 0.5), random.randint(0 + config.OBSTACLE_HEIGHT * 0.5, 500 - config.OBSTACLE_HEIGHT * 0.5)))
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
		for i in range(config.AGENT_NUM):
			drawAgent(self.agentPos[i])
		for i in range(config.PERSON_NUM):
			drawPerson(self.personPos[i])
		for i in range(config.OBSTACLE_NUM):
			drawObstacle(self.obstaclePos[i])
		drawGoal(self.goalPos)
		#updates the window
		pygame.display.flip()

	# Episode reset
	def Reset(self):
		#visualization
		self.distance_prev_agent_person = [[0]*config.PERSON_NUM]*config.AGENT_NUM
		self.distance_prev_person_goal = list()
		self.goalPos = config.GOAL_POS
		drawGoal(self.goalPos)
		
		#position reset
		self.agentPos = list()
		self.personPos = list()
		self.obstaclePos = list()
		for i in range(config.AGENT_NUM):
			self.agentPos.append((random.randint(0, 500), random.randint(0, 500)))
		for i in range(config.PERSON_NUM):
			self.personPos.append((random.randint(0, 500), random.randint(0, 500)))
		for i in range(config.OBSTACLE_NUM):
			self.obstaclePos.append((random.randint(0 + config.OBSTACLE_WIDTH * 0.5, 500 - config.OBSTACLE_WIDTH * 0.5), random.randint(0 + config.OBSTACLE_HEIGHT * 0.5, 500 - config.OBSTACLE_HEIGHT * 0.5)))

		#distance define
		for i in range(config.AGENT_NUM):
			drawAgent(self.agentPos[i])
			for j in range(config.PERSON_NUM):
				self.distance_prev_agent_person[i][j] = self.distance(self.agentPos[i],self.personPos[j])
		for i in range(config.PERSON_NUM):
			drawPerson(self.personPos[i])
			self.distance_prev_person_goal.append(self.distance(self.personPos[i],self.goalPos))
		for i in range(config.OBSTACLE_NUM):
			drawObstacle(self.obstaclePos[i])

		#updates the window
		pygame.display.flip()
		

	#  distance between two dots
	def distance(self,dot1,dot2):
		distance = ((dot1[0]-dot2[0])**2 + (dot1[1]-dot2[1])**2)**0.5
		return distance

    #  Game Update Inlcuding Display
	def PlayNextMove(self, action):
		score_0 = list()
		score_1 = list()
		score_2 = list()
		condition_agent = [0]*config.AGENT_NUM
		condition_person = [0]*config.PERSON_NUM
	
		pygame.event.pump()
		screen.fill(config.BLACK)

		#draw goal & obstacle
		for i in range(config.OBSTACLE_NUM):
			drawObstacle(self.obstaclePos[i])
		drawGoal(self.goalPos)

		#update agent
		for i in range(config.AGENT_NUM):
			self.agentPos[i] = updateAgent(action[i], self.agentPos[i])
			drawAgent(self.agentPos[i])
		
		#update person
		for i in range(config.PERSON_NUM):
			self.personPos[i] = updatePerson(self.agentPos, self.obstaclePos, self.personPos[i])
			drawPerson(self.personPos[i])
		
		#goal arrived
		for i in range(config.PERSON_NUM):
			if abs(self.goalPos[0] - self.personPos[i][0]) < config.GOAL_WIDTH * 0.5 and abs(self.goalPos[1] - self.personPos[i][1]) < config.GOAL_HEIGHT * 0.5:
				condition_person[i] = 1
				score_0.append(10.0)
		
		#obstacle collision
		for i in range(config.AGENT_NUM):
			for j in range(config.OBSTACLE_NUM):	
				if abs(self.obstaclePos[j][0] - self.agentPos[i][0]) < config.OBSTACLE_WIDTH * 0.5 - config.AGENT_SIZE and abs(self.obstaclePos[j][1] - self.agentPos[i][1]) < config.OBSTACLE_HEIGHT * 0.5 - config.AGENT_SIZE:
					condition_agent[i] = -1
					score_0.append(-5.0)

		#score based on distance
		for i in range(config.PERSON_NUM):
			if self.distance(self.personPos[i],self.goalPos) < self.distance_prev_person_goal[i]:
				score_1.append(5.0)
			elif self.distance(self.personPos[i],self.goalPos) > self.distance_prev_person_goal[i]:
				score_1.append(-0.5)
			self.distance_prev_person_goal.append(self.distance(self.personPos[i],self.goalPos))
		for i in range(config.AGENT_NUM):
			for j in range(config.PERSON_NUM):
				if self.distance(self.agentPos[i],self.personPos[j]) < self.distance_prev_agent_person[i][j]:
					score_2.append(0.05)
				elif self.distance(self.agentPos[i],self.personPos[j]) > self.distance_prev_agent_person[i][j]:
					score_2.append(-0.01)
				self.distance_prev_agent_person.append(self.distance(self.agentPos[i],self.personPos[j]))
				
		self.score = sum(score_0) + sum(score_1) + sum(score_2)

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
		return [condition_agent, condition_person, self.score, self.agentPos, self.personPos, self.obstaclePos, self.goalPos]
		
	def UpdateGameDisplay(self, Episode, Epsilon, Success, GTime):
		self.EpisodeDisplay = Episode
		self.GEpsilonDisplay = Epsilon
		self.SuccessDisplay = Success
		self.GTimeDisplay = GTime

