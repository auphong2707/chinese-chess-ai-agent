from game_state import GameState
from math import sqrt, log
from abc import ABC


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
            new_node = Node(state, self, move)
            children.append(new_node)

        return children
