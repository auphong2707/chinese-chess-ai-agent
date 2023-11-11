from game_state import GameState
from math import sqrt, log


class Node:
    """This class represents a "node" in the game tree"""

    EXPLORATION_PARAMETER = sqrt(2)

    # [INITIALIZATION]
    def __init__(self, game_state) -> None:
        self.game_state = game_state
        self.is_fully_expanded = False

        self.list_of_children = self.generate_all_children()

        self._uct = None
        self.win_until_now = 0
        self.iters_until_now = 0
        self.parent_iters_until_now = 0
    # [END INITIALIZATION]

    # [Properties]
    @property
    def uct(self) -> float:
        """This gets the UCT index of the current node"""

        # Case 1: This node hasn't been iterated
        if self.iters_until_now == 0:
            return 0

        # Case 2: This node has been iterated before
        exploitation_component = self.win_until_now/self.iters_until_now
        exploration_component = sqrt(log(self.parent_iters_until_now)/self.iters_until_now)

        return exploitation_component + self.EXPLORATION_PARAMETER*exploration_component
    # [End properties]

    # [METHOD]
    # Instance methods
    
    def generate_all_children(self) -> list:
        """This generates all descendants of the current node"""
        
        current_state = self.game_state
        children = []

        #Create list of possible game states
        list_of_states = current_state.generate_all_game_states()

        #Create new node and append to children list
        for state in list_of_states:
            new_node = Node(state)
            children.append(new_node)

        return children