from game_state import GameState
from math import sqrt, log


class Node:
    """This class represents a "node" in the game tree"""

    EXPLORATION_PARAMETER = sqrt(2)

    # [INITIALIZATION]
    def __init__(self, game_state) -> None:
        self.game_state = game_state
        self.is_fully_expanded = False

        self.list_of_children = list()

        self._uct = None
        self.win_until_now = 0
        self.iters_until_now = 0
        self.parent_iters_until_now = 0
    # [END INITIALIZATION]

