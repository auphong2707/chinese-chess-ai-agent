from game_state import GameState
from math import sqrt, log
from abc import ABC


class Node(ABC):
    """This class represents a "node" in the game tree"""

    # [INITIALIZATION]
    def __init__(self, game_state) -> None:
        self.game_state = game_state
        self.list_of_children = list()

    # [END INITIALIZATION]

    # [METHOD]
    # Instance methods

    def generate_all_children(self) -> list:
        """This generates all descendants of the current node"""

        current_state = self.game_state
        children = []

        # Create list of possible game states
        list_of_states = current_state.generate_all_game_states()

        # Create new node and append to children list
        for state in list_of_states:
            new_node = Node(state)
            children.append(new_node)

        return children
