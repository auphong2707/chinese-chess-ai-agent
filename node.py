import time
from math import inf, sqrt, log
from abc import ABC, abstractmethod
from random import randint, choice, shuffle
from game_state import GameState
from team import Team


class Node(ABC):
    """This class represents a "node" in the game tree"""

    # [INITIALIZATION]
    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        # Reference to parent and decendants of the node
        self.parent = parent
        self.parent_move = parent_move
        self.list_of_children = list()

        # Node statistic
        self.game_state = game_state
        self._is_generated_all_children = False

    # [END INITIALIZATION]

    # [METHOD]
    # Instance methods
    def get_all_children(self) -> list:
        """This generates all descendants of the current node"""

        current_state = self.game_state
        children = []

        # Create list of possible game states
        list_of_states = current_state.all_child_gamestates

        # Create new node and append to children list
        for state, move in list_of_states:
            new_node = self._create_node(state, self, move)
            children.append(new_node)

        return children

    def generate_all_children(self) -> None:
        """This method fills up the list of children nodes"""
        if self._is_generated_all_children:
            return
        self.list_of_children = self.get_all_children()
        self._is_generated_all_children = True

    # Abstract method

    @abstractmethod
    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        """This method will return a new node"""
        pass

    # [END METHOD]


class NodeMinimax(Node):
    """This class represents a "minimax's node" in game tree"""

    # [INITIALIZATION]
    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        # Reference to a node
        super().__init__(game_state, parent, parent_move)

        # Minimax statistics
        self.minimax_value = None

    # [END INITIALIZATION]

    # [METHOD]
    # Instance methods
    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        return NodeMinimax(game_state, parent, parent_move)

    def best_move(self, team: Team):
        """This module returns the so-considered "best child" 
        of the current node"""

        # Create a list of best value node
        best_children = list()

        for child in self.list_of_children:
            # If the node has value equal to the current node's value, then add it to the list
            if child.minimax_value == self.minimax_value:
                best_children.append(child)

        # Return a random child among the best
        shuffle(best_children)
        return best_children.pop()

    # [END METHOD]


class NodeMCTS(Node):
    """This class represents a "Monte-Carlo tree search's node" in game tree"""

    EXPLORATION_CONSTANT = sqrt(2)
    EXPONENTIAL_INDEX = 1
    MAX_NODE_COUNT = 90

    # [INITIALIZATION]
    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        # Reference to a node
        super().__init__(game_state, parent, parent_move)

        # MCTS statistics
        self._number_of_visits = 0
        self._rating = 0

    # Properties initialization
    @property
    def q(self):
        """Return the node's personal rating"""
        return self.game_state._current_team.value * self._rating

    @property
    def n(self):
        """Return the number of visits of this node"""
        return self._number_of_visits

    # [END INITIALIZATION]

    # [METHOD]
    # Instance method

    def best_uct(self):
        """This function calculates the child with best UCT index of node"""

        # Preset init
        current_best_uct_value = -inf
        current_result_child = []

        for child in self.list_of_children:
            if child.n != 0:
                # The current child has been visited
                uct = child.q/child.n\
                    + self.EXPLORATION_CONSTANT * \
                    (log(self.n)/child.n)**self.EXPONENTIAL_INDEX
            else:
                # The curent child has not been visited
                uct = inf

            # Comparison random choosing
            if uct > current_best_uct_value:
                current_best_uct_value = uct
                current_result_child = [child]
            elif uct == current_best_uct_value:
                current_result_child.append(child)

        shuffle(current_result_child)
        return current_result_child.pop()

    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        return NodeMCTS(game_state, parent, parent_move)

    def update_stat(self, result):
        """This module updates a node's stats"""

        self._rating += result
        self._number_of_visits += 1

    def terminate_value(self, is_end: bool) -> float:
        """This module returns the value if a node is at it's termination"""

        # Outplay case
        if is_end:
            winning_team = self.game_state._get_the_opponent_team()
            if winning_team is Team.RED:
                return 1
            if winning_team is Team.BLACK:
                return -1
        else:
            return self.game_state.value / 500

    def rollout_policy(self):
        """This module returns the chosen simulation init node
        based on the given rollout policy"""

        # Random policy
        new_game_state = self.game_state.generate_random_game_state()
        if new_game_state is None:
            return None
        else:
            return self._create_node(new_game_state[0], self, new_game_state[1])

    def rollout(self):
        """This module performs the rollout simulation"""

        node_count = 0
        current_node = self
        while node_count < self.MAX_NODE_COUNT:
            new_node = current_node.rollout_policy()
            # If the current node is terminal, return; otherwise, assign current to a random child node
            if new_node is None:
                return current_node.terminate_value(True)
            current_node = new_node
            
            node_count += 1

        return current_node.terminate_value(False)

    def backpropagate(self, result):
        """This module performs the MCTS backpropagation"""

        current_node = self
        while current_node.parent is not None:
            # I am going to meet my ultimate ancestor!
            current_node.update_stat(result)
            current_node = current_node.parent

        current_node.update_stat(result)

    def best_move(self, team):
        """This module returns the so-considered "best child" 
        of the current node"""

        max_number_of_visits = 0
        current_best_child = []

        # Traversing my sons
        for child in self.list_of_children:
            if child.n > max_number_of_visits:
                max_number_of_visits = child.n
                current_best_child.clear()
            if child.n == max_number_of_visits:
                current_best_child.append(child)

        shuffle(current_best_child)
        return current_best_child.pop()
    # [END METHOD]

if __name__ == "__main__":
    import psutil
    queue = [NodeMinimax._create_node(
            None, GameState.generate_initial_game_state(), None, None
        )]
    for depth in range(1, 5):
        start = time.time()

        new_queue = list()
        while len(queue) > 0:
            cur = queue.pop()
            cur.generate_all_children()
            for child_node in cur.list_of_children:
                new_queue.append(child_node)

        queue = new_queue
        end = time.time()
        print(depth, len(queue), end - start)
    
    pid = psutil.Process()
    memory_info = pid.memory_info()
    print(f"Memory Usage: {memory_info.rss/(1024**2)} megabytes")