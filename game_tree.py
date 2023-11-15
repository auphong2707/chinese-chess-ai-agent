# Made by Kleecon~

from game_state import GameState
from piece import Piece
from node import Node
from abc import ABC, abstractmethod

class GameTree(ABC):
    """This class is responsible for the game tree representation"""

    def __init__(self, team) -> None:
        # This generates the initial game tree, not a forged one
        self.team = team
        self.current_node = Node(
            GameState.generate_initial_game_state(), None, None
        )

    def move_to_best_child(self):
        # This moves the current node to its "best child" on the game tree
        self.current_node = self.current_node.best_move()
        self.team = self.current_node.game_state.team

    def move_to_child_node_with_move(self, old_pos, new_pos):
        # This moves the current node to its "destination" on the game tree

        # Defining a comparative game state
        new_state = GameState.generate_game_state_with_move(
            self.current_node.game_state, old_pos, new_pos
        )

        # Traversing states in the children list to find a suitable child
        for node in self.current_node.list_of_children:
            if new_state[0]._board == node.game_state._board:
                # Suitable child found
                self.current_node = node
                self.current_node.parent = None
                return

        # Suitable child not found
        self.current_node = self._create_node(
            new_state, None, (old_pos, new_pos)
        )

    # Abstract method
    @abstractmethod
    def _create_node(self, game_state, parent, parent_move):
        """Create a new node here"""
        pass

if __name__ == "main":
    # Test the class here Focalors
    pass
