# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """
    
    def manhattanDistance(self, x1, y1, x2, y2):
        return abs(x1-x2)+abs(y1-y2)
    
    def makePossibleGhostStates(self, tuple):
        return {
            (tuple[0]-1,tuple[1]): True, 
            (tuple[0]+1, tuple[1]): True, 
            (tuple[0], tuple[1]-1): True, 
            (tuple[0], tuple[1]+1): True,
            tuple: True
        }

    def closestFoodFinder(self, tuple, FoodGrid):
        x=tuple[0]
        y=tuple[1]

        #print(FoodGrid)

        if FoodGrid[x][y] == True: #something brokjen with this function
            #print("ANGIEANGIE")
            return 105
        
        #print("Height: ",FoodGrid.height)
        #print("Width: ", FoodGrid.width)

        rowCounter=0
        colCounter=0

        minDist=5000

        while rowCounter < FoodGrid.width: 
            colCounter=0
            while colCounter < FoodGrid.height:
                #print(rowCounter, colCounter, FoodGrid[rowCounter][colCounter])
                if FoodGrid[rowCounter][colCounter] == True:
                    #print("Distance: ", self.manhattanDistance(x, y, rowCounter, colCounter))
                    minDist=min(minDist, self.manhattanDistance(x, y, rowCounter, colCounter))
                if minDist==1:
                    return 99
                colCounter+=1

            rowCounter+=1

        #print(minDist)
        
        return(100-minDist)


        

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        #print("\n")

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        scoreToReturn = 0

        """
        if action == 'Stop':
            return 0
        """
        #print(type(newFood))

        #can check to see if the new position would eat a Food:

        #print(newPos, type(newPos), "\n")\

        #print(action)

        #print(newFood, "\n")

        
        
        for ghost in newGhostStates: 
            #print(ghost.getPosition())
            
            if newPos in self.makePossibleGhostStates(tuple=ghost.getPosition()):
                #print(newPos, ghost.getPosition())
                scoreToReturn -= 200

        
       


        #return scoreToReturn
        #return scoreToReturn
        score=self.closestFoodFinder(newPos, currentGameState.getFood())
        #print(action, scoreToReturn+score)

        return scoreToReturn + score
    

        
        if currentGameState.getFood()[newPos[0]][newPos[1]] == True:
            #this State Gets a Food!!
            #print("This state would eat food!")
            scoreToReturn += 5
        
        return scoreToReturn

        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    
    def pacmanMaxFunc(self, gameState, totalDepthToGoTo, currDepth, numAgents):



        print("AT THE TOP OF PACMAN MAX FUNC AT CURRENT DEPTH OF ", currDepth)

        if gameState.isWin() or gameState.isLose(): 
            print("WIN/LOSS STATE")
            return self.evaluationFunction(gameState)

        if currDepth == 1: #Jack ignore this its basically just shit code because i originiall wrote the code to only return the Score for minimax, and not the action associated with that score so had to add some shite code
            maxScore=float('-inf')
            actionToReturn='None'

            scores=[]

            for action in gameState.getLegalActions(agentIndex=0): # for move in legal moves for pacman
                thisScore=self.ghostMinFunc(gameState=gameState.generateSuccessor(0, action), totalDepthToGoTo=totalDepthToGoTo, currDepth=currDepth, numAgents=numAgents, currAgentNum=1)
                scores.append(thisScore)
                if maxScore < thisScore: 
                    print("maxScore < thisScore in PacmanMaxFunc Depth=1", "MaxScore: ", maxScore, "thiScore", thisScore)
                    maxScore=thisScore
                    actionToReturn=action
            print(scores)
            return (maxScore, actionToReturn)
        


        maxScore=float('-inf')
        scores=[]
        for action in gameState.getLegalActions(agentIndex=0): # for move in legal moves for pacman
            thisScore=self.ghostMinFunc(gameState=gameState.generateSuccessor(0, action), totalDepthToGoTo=totalDepthToGoTo, currDepth=currDepth, numAgents=numAgents, currAgentNum=1)
            maxScore=max(maxScore, thisScore)#self.ghostMinFunc(gameState=gameState.generateSuccessor(0, action), totalDepthToGoTo=totalDepthToGoTo, currDepth=currDepth, numAgents=numAgents, currAgentNum=1))
            scores.append(thisScore)
        print("SCORES: ", scores)
        return maxScore
    
    def ghostMinFunc(self, gameState, totalDepthToGoTo, currDepth, numAgents, currAgentNum):

        if gameState.isWin() or gameState.isLose(): 
            print("WIN/LOSS STATE")
            return self.evaluationFunction(gameState)

        print("Looking at ghost: ", currAgentNum, "At Depth: ", currDepth)

        if currAgentNum == numAgents - 1: #if we are on the last ghost
            print("ON THE LAST GHOST")

            minScore = float('inf')
            scores=[]
            if len(gameState.getLegalActions(currAgentNum)) == 0: 
                print("NO ACTIONS FOR LAST GHOST ARE AVAILABLE, RETURNING -INF")
                return float('inf')
            for action in gameState.getLegalActions(agentIndex=currAgentNum):
                
                if currDepth == self.depth: 
                    
                    scoreAtThisState=self.evaluationFunction(gameState.generateSuccessor(currAgentNum, action))
                    print("REACHED A Kinda-Leaf, a place where the recursion will end with SCORE: ", scoreAtThisState)
                    minScore = min(minScore, scoreAtThisState)

                    scores.append(scoreAtThisState)
                
                else: 
                    minScore=min(minScore, self.pacmanMaxFunc(gameState=gameState.generateSuccessor(currAgentNum, action), totalDepthToGoTo=totalDepthToGoTo, currDepth=currDepth+1, numAgents=numAgents))
            print("ABout to return this minScore: ", minScore, "From these Scores", scores, "at agent", currAgentNum, "at depth", currDepth)
            return minScore
        
        else: 
            print("PROBS ABOUT TO RETURN INFINITY FOR NO FUCKING REASON")
            minScore = float('inf')

            print(gameState.getLegalActions(currAgentNum))
            if len(gameState.getLegalActions(currAgentNum)) == 0: 
                return float('-inf')
            for action in gameState.getLegalActions(agentIndex=currAgentNum):
                print("GOING THROUGH FOR LOOP AT ACTION",  action)
                minScore=min(minScore, self.ghostMinFunc(gameState=gameState.generateSuccessor(currAgentNum, action), totalDepthToGoTo=totalDepthToGoTo, currDepth=currDepth, numAgents=numAgents, currAgentNum=currAgentNum+1))
            return minScore
        
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action                              THIS ONE!!!!!! IMPORTANT

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():                                                                         THIS ONE IMPORTANT DID NOT USE IT DO I NEED TO???????
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        #def pacmanMaxFunc(self, gameState, totalDepthToGoTo, currDepth, numAgents):

        print("PICKINJG ACTION", self.depth, "\n", "\n")
        tuple= self.pacmanMaxFunc(gameState=gameState, totalDepthToGoTo=self.depth, currDepth=1, numAgents=gameState.getNumAgents())
        print(tuple)
        
        return tuple[1]


        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def pacmanMaxFunc(self, gameState, currDepth, numAgents, alpha, beta):

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)


        if currDepth == 1: #if at the first depth need to return the action to take, not just the score

            maxScore=float('-inf')
            actionToReturn = None

            for action in gameState.getLegalActions(agentIndex=0):

                thisScore=self.ghostMinFunc(gameState.generateSuccessor(agentIndex=0, action=action), currDepth, numAgents, currAgentNum=1, alpha=alpha, beta=beta) #finish line
                #def ghostMinFunc(self, gameState, currDepth, numAgents, currAgentNum, alpha, beta):
                if thisScore > beta:
                    return thisScore
                #dont think I need to do the above 2 lines, but the below line is def neccesary
                alpha = max(alpha, thisScore)

                if maxScore < thisScore: 
                    maxScore = thisScore
                    actionToReturn = action
                
            return (maxScore, actionToReturn)
        
        maxScore = float('-inf')

        for action in gameState.getLegalActions(agentIndex=0):
            maxScore=max(maxScore, self.ghostMinFunc(gameState.generateSuccessor(0, action), currDepth, numAgents, 1, alpha, beta))#finish this line!!

            if maxScore > beta:#do not prune on equality
                return maxScore
            
            alpha = max(alpha, maxScore)
        
        return maxScore

    
    def ghostMinFunc(self, gameState, currDepth, numAgents, currAgentNum, alpha, beta):

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        if currAgentNum == numAgents-1: #we are on the last ghost, need to call pacman after this one OR return the score if at the right depth

            minScore=float('inf')

            for action in gameState.getLegalActions(agentIndex=currAgentNum):

                if currDepth == self.depth:
                    
                    minScore=min(minScore, self.evaluationFunction(gameState.generateSuccessor(currAgentNum, action)))

                    if minScore < alpha: 
                        return minScore

                    beta=min(beta, minScore)
                
                else:
                    #def pacmanMaxFunc(self, gameState, currDepth, numAgents, alpha, beta):
                    minScore=min(minScore, self.pacmanMaxFunc(gameState=gameState.generateSuccessor(currAgentNum, action), currDepth=currDepth+1, numAgents=numAgents, alpha=alpha, beta=beta))

                    if minScore < alpha: 
                        return minScore
                    beta=min(beta, minScore)

            return minScore
        
        else: #not on the last ghost, need to pass to next ghost instead of pacman

            minScore = float('inf')

            for action in gameState.getLegalActions(agentIndex=currAgentNum):

                minScore = min(minScore, self.ghostMinFunc(gameState.generateSuccessor(currAgentNum, action), currDepth, numAgents, currAgentNum+1, alpha, beta))
                if minScore < alpha:
                    return minScore
                
                beta = min(beta, minScore)
            
            return minScore



        


    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return (self.pacmanMaxFunc(gameState, currDepth=1, numAgents=gameState.getNumAgents(), alpha=float('-inf'), beta=float('inf')))[1]

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def pacmanMaxFunc(self, gameState, currDepth, numAgents):

        if gameState.isWin() or gameState.isLose():
            #print("MAX END STATE - PROBS SHOULDNT HAPPEN?")
            return self.evaluationFunction(gameState)


        if currDepth == 1: #if at the first depth need to return the action to take, not just the score

            maxScore=float('-inf')
            actionToReturn = None

            for action in gameState.getLegalActions(agentIndex=0):

                thisScore=self.ghostMinFunc(gameState.generateSuccessor(agentIndex=0, action=action), currDepth, numAgents, currAgentNum=1) 

                if maxScore < thisScore: 
                    maxScore = thisScore
                    actionToReturn = action
                
            return (maxScore, actionToReturn)
        
        
        
        maxScore=float('-inf')
        scores=[]

        for action in gameState.getLegalActions(agentIndex=0):
            thisScore=self.ghostMinFunc(gameState.generateSuccessor(0, action), currDepth, numAgents, 1)
            scores.append(thisScore)
            maxScore=max(maxScore,thisScore)
        #print("returning: ", maxScore, "from: ", scores)
        
        return maxScore

    
    def ghostMinFunc(self, gameState, currDepth, numAgents, currAgentNum):

        if gameState.isWin() or gameState.isLose():
            #("EXPECT WIN/LOSS STATE")
            return self.evaluationFunction(gameState)
        
        if currAgentNum == numAgents-1: #we are on the last ghost, need to call pacman after this one OR return the score if at the right depth

            sumScore=0
            scores=[]

            for action in gameState.getLegalActions(agentIndex=currAgentNum):

                if currDepth == self.depth:
                    thisScore=self.evaluationFunction(gameState.generateSuccessor(currAgentNum, action))
                    scores.append(thisScore)
                    sumScore+=thisScore

                    
                
                else:
                    #def pacmanMaxFunc(self, gameState, currDepth, numAgents, alpha, beta):
                    thisScore=self.pacmanMaxFunc(gameState=gameState.generateSuccessor(currAgentNum, action), currDepth=currDepth+1, numAgents=numAgents)
                    scores.append(thisScore)
                    sumScore+=thisScore
                    
            #print("returning: ", sumScore / len(gameState.getLegalActions(agentIndex=currAgentNum)), "from these scores: ", scores)
            return (sumScore / len(gameState.getLegalActions(agentIndex=currAgentNum)))
        
        else: #not on the last ghost, need to pass to next ghost instead of pacman

            sumScore=0
            scores=[]
            for action in gameState.getLegalActions(agentIndex=currAgentNum):

                sumScore+=self.ghostMinFunc(gameState.generateSuccessor(currAgentNum, action), currDepth, numAgents, currAgentNum+1)
                
            
            return (sumScore / len(gameState.getLegalActions(currAgentNum)))

    

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #def pacmanMaxFunc(self, gameState, currDepth, numAgents):

        #print("using epectimax, with depth: ", self.depth)

        return self.pacmanMaxFunc(gameState, 1, gameState.getNumAgents())[1]

        util.raiseNotDefined()

def manhattanDistance(x1, y1, x2, y2):
        return abs(x1-x2)+abs(y1-y2)
    
        

def closestFoodFinder(tuple, FoodGrid):
    x=tuple[0]
    y=tuple[1]

    #print(FoodGrid)

    if FoodGrid[x][y] == True: #something brokjen with this function
        #print("ANGIEANGIE")
        return 55
    
    #print("Height: ",FoodGrid.height)
    #print("Width: ", FoodGrid.width)

    rowCounter=0
    colCounter=0

    minDist=5000

    while rowCounter < FoodGrid.width: 
        colCounter=0
        while colCounter < FoodGrid.height:
            #print(rowCounter, colCounter, FoodGrid[rowCounter][colCounter])
            if FoodGrid[rowCounter][colCounter] == True:
                #print("Distance: ", self.manhattanDistance(x, y, rowCounter, colCounter))
                minDist=min(minDist, manhattanDistance(x, y, rowCounter, colCounter))
            if minDist==1:
                return 49
            colCounter+=1

        rowCounter+=1

    #print(minDist)
    
    return(50-minDist)


def betterEvaluationFunction(currentGameState):
    import random
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    currPos=currentGameState.getPacmanPosition()
    currFood=currentGameState.getFood()
    #print(currPos)
    closestFood=closestFoodFinder(currPos, currFood)
    #print(closestFood)

    ghostDist=0
    ghost=currentGameState.getGhostStates()[0].getPosition()
    #print(currPos, ghost)
    ghostDist=manhattanDistance(currPos[0], currPos[1], ghost[0], ghost[1])

    #print(ghostDist)

    if currentGameState.isLose():
        #print("HERE")
        return currentGameState.getScore()

    if currentGameState.isWin():
        return currentGameState.getScore()+random.random()*20
    
    return currentGameState.getScore() + closestFood+random.random()*10 + ghostDist
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
