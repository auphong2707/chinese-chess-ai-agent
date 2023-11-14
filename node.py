from cmath import inf
from math import sqrt, log
from abc import ABC, abstractmethod
from game_state import GameState


class Node():
    """This class represents a "node" in the game tree"""

    # [INITIALIZATION]
    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        # Reference to parent and decendants of the node
        self.parent = parent
        self.parent_move = parent_move
        self.list_of_children = list()

        # Node statistic
        self.game_state = game_state

    # [END INITIALIZATION]

    # [METHOD]

    def best_move(self):
        """This method will return the best node to move to from the current"""
        pass


class NodeMinimax(Node):
    """This class represents a "minimax's node" in game tree"""

    # [INITIALIZATION]
    def __init__(self, game_state: GameState, parent, parent_move: tuple) -> None:
        # Reference to a node
        super().__init__(game_state, parent, parent_move)

        # Minimax statistics
        self._alpha = -inf
        self._beta = inf
        self._minimax_value = None
        self._depth = None

    # [END INITIALIZATION]

    # [METHOD]
    # Instance methods
    def generate_all_children(self) -> None:
        """This generates all descendants of the current node"""

        current_state = self.game_state
        children = []

        # Create list of possible game states
        list_of_states = current_state.generate_all_game_states()

        # Create new node and append to children list
        for state, move in list_of_states:
            new_node = Node(state, self, move)
            children.append(new_node)

        self.list_of_children = children

    def _reset_statistics(self) -> None:
        """This method resets the minimax statistics"""

        self._alpha = -inf
        self._beta = inf
        self._minimax_value = None
        self._depth = None


