class MonteCarloTreeSearch(object):

    def __init__(self, node):
        self.root = node

    def best_action(self, simulations_number):
        for _ in range(0, simulations_number):  
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        if self.root.is_terminal_node():
            return self.root
        else:
            print('Getting Final')
            return self.root.best_child(c_param=0.0)

    def _tree_policy(self):
        current_node = self.root
        
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node