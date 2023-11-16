# Made by Kleecon~
from cmath import inf
from abc import ABC, abstractmethod
from game_state import GameState
from piece import Piece
from node import Node
from node import NodeMinimax


class GameTree(ABC):
    """This class is responsible for the game tree representation"""

    def __init__(self, team) -> None:
        # This generates the initial game tree, not a forged one
        self.team = team
        self.current_node = self._create_node(
            GameState.generate_initial_game_state(), None, None
        )

    def move_to_best_child(self) -> tuple:
        """This moves the current node to its "best child" on the game tree"""
        self.current_node = self.current_node.best_move(self.team)
        self.current_node.parent = None

        return self.current_node.parent_move

    def move_to_child_node_with_move(self, old_pos, new_pos):
        """This moves the current node to its "destination" on the game tree"""

        # Defining a comparative game state
        new_state, move = GameState.generate_game_state_with_move(
            self.current_node.game_state, old_pos, new_pos
        )

        # Traversing states in the children list to find a suitable child
        for node in self.current_node.list_of_children:
            if new_state._board == node.game_state._board:
                # Suitable child found
                self.current_node = node
                self.current_node.parent = None
                return

        # Suitable child not found
        self.current_node = self._create_node(
            new_state, None, move
        )

    # Abstract method
    @abstractmethod
    def _create_node(self, game_state, parent, parent_move) -> None:
        """This method return a new node of the tree"""
        pass


class GameTreeMinimax(GameTree, NodeMinimax):
    """This class is responsible for the game tree minimax"""

    TARGET_DEPTH = 7

    def minimax(self, node: NodeMinimax, depth: int, max_turn: bool):
        """Minimax method"""
        # If the node reaches the target depth
        if depth == self.TARGET_DEPTH:
            node.minimax_value = node.game_state.value
            return node.minimax_value

        node.list_of_children = node.generate_all_children()
        # Max turn
        if max_turn is True:
            result = -inf
            for child in node.list_of_children:
                value = self.minimax(child, depth + 1, False)
                result = max(result, value)
                node.alpha = max(node.alpha, result)
                if node.beta <= node.alpha:
                    break
            return result
        # Min turn
        else:
            result = inf
            for child in node.list_of_children:
                value = self.minimax(child, depth + 1, True)
                result = min(result, value)
                node.beta = min(node.beta, result)
                if node.beta <= node.alpha:
                    break
            return result

    def _create_node(self, game_state, parent, parent_move) -> None:
        return NodeMinimax._create_node(self, game_state, parent, parent_move)


if __name__ == "main":
    # Test the class here Focalors
    pass
