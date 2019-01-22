import environment # My Rescue Game 
import agent # My DQN Based Agent
import config
import numpy as np 
import random 
import matplotlib.pyplot as plt
# =======================================================================
# Normalise GameState
def CaptureNormalisedState(agentPos, personPos, obstaclePos, goalPos):
	gstate = [0] * config.STATECOUNT
	for i in range(config.AGENT_NUM):
		gstate[i*2] = agentPos[i][0]/500.0
		gstate[i*2+1] = agentPos[i][1]/500.0
	for i in range(config.PERSON_NUM):
		gstate[i*2 + config.AGENT_NUM*2] = personPos[i][0]/500.0
		gstate[i*2+1 + config.AGENT_NUM*2] = personPos[i][1]/500.0
	for i in range(config.OBSTACLE_NUM):
		gstate[i*2 + config.AGENT_NUM*2 + config.PERSON_NUM*2] = obstaclePos[i][0]/500.0
		gstate[i*2+1 + config.AGENT_NUM*2 + config.PERSON_NUM*2] = obstaclePos[i][0]/500.0
	gstate[config.AGENT_NUM*2 + config.PERSON_NUM*2 + config.OBSTACLE_NUM*2] = goalPos[0]/500.0
	gstate[1 + config.AGENT_NUM*2 + config.PERSON_NUM*2 + config.OBSTACLE_NUM*2] = goalPos[1]/500.0
	
	gstate = np.array(gstate)
	
	return gstate
# =====================================================================
# Main Experiment Method 
def PlayExperiment():
	Episode = 0
	Success = 0
	GameHistory = []
	
	#Create our PongGame instance
	TheGame = environment.Rescue()
    # Initialise Game
	TheGame.InitialDisplay()
	#
	#  Create our Agent (including DQN based Brain)
	TheAgent = agent.Agent(config.STATECOUNT, config.ACTIONS)
	
	# Initialise NextAction  Assume Action is scalar:  0:stay, 1:Up, 2:Down 3:Right 4.Left
	BestAction = 0
	
	# Initialise current Game State ~ Believe insigificant: (agentPos, agentPos, personPos, personPos)
	GameState = [0] * config.STATECOUNT
	
    # =================================================================
	#Main Experiment Loop 
	for Episode in range(config.MAX_EPISODE):    
		GameTime = 0
		# Reset
		TheGame.Reset()

		for gtime in range(config.MAX_GAMETIME):
		
			# First just Update the Game Display
			TheGame.UpdateGameDisplay(Episode,TheAgent.epsilon,Success,GameTime)
		
			# Determine Next Action From the Agent
			BestAction = TheAgent.Act(GameState, Episode)

			#  Now Apply the Recommended Action into the Game 	
			[condition_agent, condition_person, ReturnScore, agentPos, personPos, obstaclePos, goalPos]= TheGame.PlayNextMove(BestAction)
			NextState = CaptureNormalisedState(agentPos, personPos, obstaclePos, goalPos)

			# Capture the Sample [S, A, R, S"] in Agent Experience Replay Memory 
			TheAgent.CaptureSample((GameState,BestAction,ReturnScore,NextState),Episode)
			
			#  Now Request Agent to DQN Train process  Against Experience
			TheAgent.Process()
			
			# Move State On
			GameState = NextState

			# Move GameTime Click
			GameTime = GameTime+1
			for i in range(config.PERSON_NUM):
				if condition_person[i] == 1:
					Success = Success + 1
					break
			for i in range(config.AGENT_NUM):
				if condition_agent[i] == -1:
					break
		
		# Move Episode Click
		Episode = Episode + 1

		if Episode % 10 == 0:
			print("Episode : ", Episode,"Success: ", Success, "EP: ", "{0:.2f}".format(TheAgent.epsilon), "Game Time: ", GameTime)
			GameHistory.append((Episode,Success,TheAgent.epsilon,GameTime))
			
	# ===============================================
	# End of Game Loop  so Plot the Score vs Game Time profile
	x_val = [x[0] for x in GameHistory]
	y_val = [x[1] for x in GameHistory]

	plt.plot(x_val,y_val)
	plt.xlabel("Episode")
	plt.ylabel("Success")
	plt.show()

	
	# =======================================================================
def main():
    #
	# Main Method Just Play our Experiment
	PlayExperiment()
	
	# =======================================================================
if __name__ == "__main__":
    main()
