import random 
import math
from collections import defaultdict
from GameAlgos import Game
class MCTSNode(object):

    def __init__(self, state,player,winK,parent=None):
        """
        Parameters
        ----------
        state : mctspy.games.common.TwoPlayersAbstractGameState
        parent : MonteCarloTreeSearchNode
        """
        self.state = state
        self.parent = parent
        self.player = player
        self.children = []
        self.unexplored_actions = self.untried_actions()
        self.winK=winK
        self.Q=0
        self.N=0
    def get_opponent(self,turn):
        if turn == 'X':
            return 'O'
        else:
            return 'X'
    def get_legal_actions(self,player):
        game = Game()
        turn =0
        if player == 'X':
            turn = 0
        elif player == 'O':
            turn = 1
        return game.actions(self.state,turn)

    
    def untried_actions(self):
        game = Game()
        self.unexplored_actions = self.get_legal_actions(self.get_opponent(self.player))
        return self.unexplored_actions



    def expand(self):
        next_action = self.unexplored_actions.pop()
        game = Game()
        next_state = game.result(self.state,next_action)
        if next_action[0] == 0:
            turn ='X'
        else:
            turn ='O'
        child_node = MCTSNode(next_state,turn,self.winK,parent=self)
        self.children.append(child_node)
        return child_node
        
    def move(self,action):
        game=Game()
        next_state = game.result(self.state,action)
        if action[0]==0:
            turn = 'X'
        else:
            turn = 'O'
        child_node= MCTSNode(next_state,turn,self.winK,parent=self)
        return child_node
    
    def is_terminal_node(self):
        game = Game()
        result = game.utility(self.state,self.winK)
        if result is not None:
            return 1
        else:
            return 0
            
    def rollout_policy(self,possible_moves):
        return random.choice(possible_moves)

    def rollout(self):
        game=Game()
        current_rollout_state = self
        while not current_rollout_state.is_terminal_node():
            possible_moves = current_rollout_state.get_legal_actions(self.get_opponent(current_rollout_state.player))
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        result = game.utility(current_rollout_state.state,self.winK)
        return result
    
            
    def backpropagate(self, result):
        self.N+=1
        if result == 1 and self.player == 'O':
            self.Q = self.Q+1
        elif result == -1 and self.player == 'X':
            self.Q = self.Q+1
        elif result == 1 and self.player == 'X':
            self.Q = self.Q-1
        elif result == -1 and self.player == 'O':
            self.Q = self.Q-1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.unexplored_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.Q / c.N) + c_param * math.sqrt((2 * math.log(self.N) / c.N))
            for c in self.children
        ]
        max_weight_arg = 0
        max_weight = choices_weights[0]
        for i in range(1,len(choices_weights)):
            if choices_weights[i] > max_weight:
                max_weight = choices_weights[i]
                max_weight_arg = i

        return self.children[max_weight_arg]