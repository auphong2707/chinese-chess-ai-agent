from cmath import inf
from collections import defaultdict
from math import sqrt, log
from abc import ABC, abstractmethod
from random import randint
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
        list_of_states = current_state.generate_all_game_states()

        # Create new node and append to children list
        for state, move in list_of_states:
            new_node = self._create_node(state, self, move)
            children.append(new_node)

        return children

    # Abstract method
    @abstractmethod
    def best_move(self, team: Team):
        """This method will return the best node to move to from the current"""
        pass

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
        self.alpha = -inf
        self.beta = inf
        self.minimax_value = None

    # [END INITIALIZATION]

    # [METHOD]
    # Instance methods
    def generate_all_children(self) -> None:
        """This method fills up the list of children nodes"""

        self.list_of_children = self.get_all_children()
        if self._is_generated_all_children:
            return
        self._is_generated_all_children = True
    
    def reset_statistics(self) -> None:
        """This method resets the minimax statistics"""

        self.alpha = -inf
        self.beta = inf
        self.minimax_value = None

    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        return NodeMinimax(game_state, parent, parent_move)

    def best_move(self, team: Team):
        # Create a list of best value node
        best_children, best_value = list(), 0

        for child in self.list_of_children:
            evaluation_value = child.minimax_value*team.value
            # If we found a new best value, then update it and reset the list
            if evaluation_value > best_value:
                best_value = evaluation_value
                best_children.clear()

            # If the node has value equal to the best value, then add it to the list
            if evaluation_value == best_value:
                best_children.append(child)

        # Return a random child among the best
        return best_children[randint(0, len(best_children) - 1)]

    # [END METHOD]


class NodeMCTS(Node):
    """This class represents a "Monte-Carlo tree search's node" in game tree"""

    # [INITIALIZATION]
    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        # Reference to a node
        super().__init__(game_state, parent, parent_move)

        # MCTS statistics
        self._result = defaultdict(int)
        self._number_of_visits = 0
        self._result[1] = 0
        self._result[-1] = 0
        self.list_of_unvisited_child = list()

    # Properties initialization
    @property
    def q(self):
        """Return the difference between wins and losses"""
        return self._result[1] - self._result[-1]

    @property
    def n(self):
        """Return the number of visits of this node"""
        return self._number_of_visits

    @property
    def is_fully_expanded(self):
        """Return whether it has been fully expanded or not"""
        return len(self.list_of_unvisited_child) == 0

    # [END INITIALIZATION]

    # [METHOD]
    # Instance method
    def generate_all_unvisited_node(self):
        """This method generates all unvisited nodes"""
        self.list_of_unvisited_child = self.get_all_children()
        return None

    def _create_node(self, game_state: GameState, parent, parent_move: tuple):
        return NodeMCTS(game_state, parent, parent_move)

    # [END METHOD]
