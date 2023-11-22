# Made by Kleecon~
from cmath import inf
from abc import ABC, abstractmethod
from game_state import GameState
from piece import Piece
from node import Node
from node import NodeMinimax


class GameTree(ABC):
    """This class is responsible for the game tree representation"""

    MAX_NODE = inf

    def __init__(self, team) -> None:
        # This generates the initial game tree, not a forged one
        self.team = team
        self.current_node = self._create_node(
            GameState.generate_initial_game_state(), None, None
        )
        self.count = 0

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

    def __init__(self, team, target_depth):
        super().__init__(team)
        self.target_depth = target_depth

    def minimax(self, node: NodeMinimax, depth: int, max_turn: bool, alpha: float = -inf, beta: float = inf):
        """Minimax method"""
        self.count += 1
        node.reset_statistics()
        # If the node reaches the target depth or the count reaches max number
        if depth == self.target_depth or self.count >= self.MAX_NODE:
            node.minimax_value = node.game_state.value
            return node.minimax_value

        node.generate_all_children()
        # Max turn
        if max_turn is True:
            node.minimax_value = -inf
            for child in node.list_of_children:
                value = self.minimax(child, depth + 1, False, alpha, beta)
                node.minimax_value = max(node.minimax_value, value)
                alpha = max(alpha, node.minimax_value)
                if beta <= alpha:
                    break
            return node.minimax_value
        # Min turn
        else:
            node.minimax_value = inf
            for child in node.list_of_children:
                value = self.minimax(child, depth + 1, True, alpha, beta)
                node.minimax_value = min(node.minimax_value, value)
                beta = min(beta, node.minimax_value)
                if beta <= alpha:
                    break
            return node.minimax_value

    def _create_node(self, game_state, parent, parent_move) -> NodeMinimax:
        return NodeMinimax(game_state, parent, parent_move)

if __name__ == "main":
    # Test the class here Focalors
    pass
