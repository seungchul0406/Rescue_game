import environment # My Rescue Game 
import agent # My DQN Based Agent
import config
import numpy as np 
import random 
import matplotlib.pyplot as plt
# =======================================================================
# Normalise GameState
def CaptureNormalisedState(agentXPos, agentYPos, personXPos, personYPos, obstacleXPos, obstacleYPos, goalXPos, goalYPos):
	gstate = np.zeros([config.STATECOUNT])
	gstate[0] = agentXPos/500.0	# Normalised agentXPos
	gstate[1] = agentYPos/500.0	# Normalised agentYPos
	gstate[2] = personXPos/500.0 # Normalised personXPos
	gstate[3] = personYPos/500.0 # Normalised personYPos
	gstate[4] = obstacleXPos/500.0 # Normalised obstacleXPos
	gstate[5] = obstacleYPos/500.0 # Normalised obstacleYPos
	gstate[6] = goalXPos/500.0 # Normalised goalXPos
	gstate[7] = goalYPos/500.0 # Normalised goalYPos
	
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
	
	# Initialise current Game State ~ Believe insigificant: (agentXPos, agentYPos, personXPos, personYPos)
	GameState = CaptureNormalisedState(100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0)
	
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
			[condition, ReturnScore,agentXPos, agentYPos, personXPos, personYPos, obstacleXPos, obstacleYPos, goalXPos, goalYPos]= TheGame.PlayNextMove(BestAction)
			NextState = CaptureNormalisedState(agentXPos, agentYPos, personXPos, personYPos, obstacleXPos, obstacleYPos, goalXPos, goalYPos)

			# Capture the Sample [S, A, R, S"] in Agent Experience Replay Memory 
			TheAgent.CaptureSample((GameState,BestAction,ReturnScore,NextState),Episode)
			
			#  Now Request Agent to DQN Train process  Against Experience
			TheAgent.Process()
			
			# Move State On
			GameState = NextState

			# Move GameTime Click
			GameTime = GameTime+1

			if condition == "success":
				Success = Success + 1
				break
			if condition == "fail":
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
