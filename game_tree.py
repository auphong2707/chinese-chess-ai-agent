# Made by Kleecon~
from cmath import inf
from abc import ABC, abstractmethod
from game_state import GameState
from piece import Piece
from node import Node
from time import time
from node import NodeMinimax, NodeMCTS
from random import choice
from team import Team


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

    def is_lost(self) -> bool:
        """This method checks if the bot had lost or not"""
        return len(self.current_node.game_state.all_child_gamestates) == 0

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

    def process(self, moves_queue) -> tuple:
        """Let the bot run"""
        # [START BOT'S TURN]

        start = time()  # Start time counter
        self.minimax(self.current_node, 0, self.team is Team.RED)
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        # [POST PROCESS]
        print(self.count)
        self.count = 0
        end = time()  # End time counter
        print("Time: {:.2f} s".format(end - start))
        print("{} moves: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos

        # [END BOT'S TURN]

class GameTreeMCTS(GameTree, NodeMCTS):
    """This class is responsible for performance of the MCTS game tree"""

    TIME_ALLOWED = 2

    def traverse(self, node: NodeMCTS):
        """This module performs the MCTS initial traversion"""

        if len(node.list_of_children) > 0:
            return self.traverse(self.best_uct(node))
        if node.n == 0:
            node.list_of_unvisited_children = node.get_all_unvisited_children()
        chosen_node = choice(node.list_of_unvisited_children)

        node.list_of_unvisited_children.remove(chosen_node)
        node.list_of_children.append(chosen_node)

        return chosen_node

    def monte_carlo_tree_search(self, root, time_allowed):
        """This function performs the MCTS itself"""

        starting_time = time()
        while time()-starting_time < time_allowed:
            leaf = self.traverse(root)
            stimulation_result = self.rollout(leaf,0)
            self.backpropagate(leaf, stimulation_result)

        return self.best_move(root)
    
    def process(self, moves_queue) -> tuple:
        """Let the bot run"""
        # [START BOT'S TURN]

        start = time()  # Start time counter
        self.monte_carlo_tree_search(self.current_node, self.TIME_ALLOWED)
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        # [POST PROCESS]
        print(self.count)
        self.count = 0
        end = time()  # End time counter
        print("Time: {:.2f} s".format(end - start))
        print("{} moves: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos

        # [END BOT'S TURN]

if __name__ == "main":
    # Test the class here Focalors
    pass
