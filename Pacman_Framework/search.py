# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List
import random



class Node:
    def __init__(self, state, parent=None, action=None, cost=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def getState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

    def getCost(self):
        return self.cost

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def randomSearch(problem):
    result=[]
    currentState=problem.getStartState()

    while not problem.isGoalState(currentState):
        successors = problem.getSuccessors(currentState)
        if not successors:
            break
        choice = random.choice(successors)
        result.append(choice[1])  # choice[1] is the action
        currentState = choice[0]  # choice[0] is the state

    return result

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    """YOUR CODE HERE"""

    stack=util.Stack()
    stack.push((problem.getStartState(),[])) #push starting node and the list of actions to reach that node
    visited=set() #set to keep up with the visited nodes

    while not stack.isEmpty():
        current_state,actions=stack.pop()

        #if state is the goal and return list of actions that reaches the goal
        if problem.isGoalState(current_state):
            return actions

        #if state is not the goal and hasnt been visited
        if current_state not in visited:
            visited.add(current_state) #mark as visited

            #get all neighbors/successors and actions of current state and push it to stack
            for successors,action,_ in problem.getSuccessors(current_state):
                stack.push((successors,actions+[action]))

    return []

    #util.raiseNotDefined()


def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    my_queue=util.Queue()
    visited=[]
    currentNode=None

    startNode=Node(problem.getStartState(), None, None,0)
    my_queue.push(startNode)

    while not my_queue.isEmpty():
        currentNode= my_queue.pop()
        if problem.isGoalState(currentNode.getState()):
            break
        if currentNode.getState() not in [node.getState() for node in visited]:
            visited.append(currentNode)
            succ = problem.getSuccessors(currentNode.getState())
            for state, action, cost in succ:
                newNode = Node(state, currentNode, action)
                my_queue.push(newNode)

    moves=[]

    while currentNode.getParent():
        moves.append(currentNode.getAction())
        currentNode=currentNode.getParent()

    moves.reverse()
    return moves

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    priority_queue=util.PriorityQueue()
    visited=set()
    priority_queue.push((problem.getStartState(),[],0),0)  # push starting node, list of actions and cost 0 to reach that node

    while not priority_queue.isEmpty():
        current_state,actions,current_cost=priority_queue.pop()

        # if state is the goal and return list of actions that reaches the goal
        if problem.isGoalState(current_state):
            return actions

        # if state is not the goal and hasnt been visited explore it
        if current_state not in visited :
            visited.add(current_state)

            # get all neighbors/successors, actions and step costs of current state
            for successor,action,stepCost in problem.getSuccessors(current_state):
                #if successor hasnt been visited
                if successor not in visited :
                    #calculate new cost and push it to queue
                    priority_queue.push((successor, actions + [action], current_cost + stepCost), current_cost + stepCost)

    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    startNode = Node(startState, None, None, 0)
    frontier = util.PriorityQueue()
    frontier.push(startNode, heuristic(startState, problem))
    explored = {}
    explored[startState] = 0

    while not frontier.isEmpty():
        currentNode = frontier.pop()
        currentState = currentNode.getState()

        if problem.isGoalState(currentState):
            moves = []
            while currentNode.getParent():
                moves.append(currentNode.getAction())
                currentNode = currentNode.getParent()
            moves.reverse()
            return moves

        for successor, action, stepCost in problem.getSuccessors(currentState):
            newCost = currentNode.getCost() + stepCost
            if successor not in explored or newCost < explored[successor]:
                explored[successor] = newCost
                priority = newCost + heuristic(successor, problem)
                newNode = Node(successor, currentNode, action, newCost)
                frontier.push(newNode, priority)

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
