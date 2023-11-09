from game_state import GameState

class Node:
    """This class represents a "node" in the game tree"""

    # <INITIALIZATION>
    def __init__(self,game_state) -> None:
        self.game_state = game_state
        self.is_fully_expanded = None
        self._uct = None
        self.list_of_unvisited_node = None
        self.list_of_visited_node = None
    # <END_INITIALIZATION>

    # <Properties>
    @property
    def uct(self) -> float:
        """This function is the Getter function of uct\
        returns the UCT index of the node"""
        if self._uct is None:
            self._uct = self._get_uct()
        
        return self._uct
    # <End properties>

    # <Begin getter/setter instance methods>
    def _get_uct(self):
        """This gets the UCT index of the current node"""
        # DEFAULT VALUE
        return 0
    # <End getter/setter instance methods>

    # <Begin instance methods>
    def generate_all_children(self) -> list:
        """This generates all descendants of the current node"""
        # Phần của Khánh
        pass

    