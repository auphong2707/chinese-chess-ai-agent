# Made by Veil, Kleecon, TheSyx, Whatsoever
"""Module used to create GameTree class and its subclasses"""
from math import inf
from abc import ABC, abstractmethod
from time import time
from game_state import GameState
from node import NodeMinimax, NodeMCTS, NodeExcavationMinimax
from team import Team


class GameTree(ABC):
    """This class is responsible for the game tree representation"""

    # [BEGIN CONSTANTS]

    MAX_NODE = inf

    # [END CONSTANTS]

    # [BEGIN INITIALIZATION]

    def __init__(self, team: Team, value_pack: int = 0) -> None:
        # This method generates the initial game tree
        self.team = team
        self.current_node = self._create_node(
            GameState.generate_initial_game_state(value_pack), None, None
        )
        self._value_pack = value_pack
        self.count = 0

    # [END INITIALIZATION]

    # [BEGIN METHODS]
    # Instance method

    def move_to_best_child(self) -> tuple:
        """This method moves the current node to its "best child" on the game tree"""

        self.current_node = self.current_node.best_move()
        self.current_node.parent = None

        return self.current_node.parent_move

    def move_to_child_node_with_move(self, old_pos, new_pos):
        """This method moves the current node to its "destination" on the game tree"""

        # Define a comparative game state
        new_state, move = GameState.generate_game_state_with_move(
            self.current_node.game_state, old_pos, new_pos
        )

        # Traverse states in the children list to find a suitable child
        for node in self.current_node.list_of_children:
            if new_state.board == node.game_state.board:
                # Suitable child found
                self.current_node = node
                self.current_node.parent = None
                return

        # Suitable child not found
        self.current_node = self._create_node(new_state, None, move)

    def is_lost(self) -> bool:
        """This method checks if the bot had lost or not"""

        return len(self.current_node.game_state.all_child_gamestates) == 0

    # Abstract method
    @abstractmethod
    def _create_node(self, game_state, parent, parent_move) -> None:
        """This method return a new node of the tree"""
        pass

    # [END METHODS]


class GameTreeMinimax(GameTree):
    """This class is responsible for the game tree minimax"""

    # [BEGIN INITIALIZATION]

    def __init__(self, team, target_depth, value_pack: int = 0):
        super().__init__(team, value_pack)
        self.target_depth = target_depth

    # [END INITIALIZATION]

    # [BEGIN METHODS]
    # Private method

    def _create_node(self, game_state, parent, parent_move) -> NodeMinimax:
        """This method creates a Minimax node"""

        return NodeMinimax(game_state, parent, parent_move)

    # Instance method

    def process(self, moves_queue) -> tuple:
        """Let the bot run"""
        # [START BOT'S TURN]
        # Start the time counter
        start = time()
        self.current_node.minimax(self.target_depth, self.team is Team.RED)
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        # [POST PROCESS]
        print(self.current_node.minimax_value)
        self.count = 0
        end = time()  # End the time counter
        print("Time: {:.2f} s".format(end - start))
        print("{} moves: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos

        # [END BOT'S TURN]

    # [END METHODS]


class GameTreeMCTS(GameTree):
    """This class is responsible for performance of the MCTS game tree"""

    # [BEGIN INITIALIZATION]

    def __init__(
        self, team, time_allowed, value_pack: int = 2, rollout_policy="RANDOM"
    ) -> None:
        super().__init__(team, value_pack)
        self.time_allowed = time_allowed
        self.rollout_policy = rollout_policy

    # [END INITIALIZATION]

    # [BEGIN METHODS]
    # Instance method

    def traverse(self, node: NodeMCTS) -> NodeMCTS:
        """This method performs the MCTS initial traversion"""

        if len(node.list_of_children) > 0:
            return self.traverse(node.best_uct())
        else:
            return node

    def monte_carlo_tree_search(self, root) -> None:
        """This method performs the MCTS"""

        root.num = 0
        starting_time = time()
        while time() - starting_time < self.time_allowed:
            root.num += 1
            leaf = self.traverse(root)
            leaf.generate_all_children()
            stimulation_result = leaf.rollout(self.rollout_policy)
            leaf.backpropagate(stimulation_result)

    def process(self, moves_queue) -> tuple:
        """Let the bot run"""
        # [START BOT'S TURN]
        # Start the time counter
        start = time()
        self.monte_carlo_tree_search(self.current_node)
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        # [POST PROCESS]
        print(self.count)
        self.count = 0
        end = time()  # End the time counter
        print("Time: {:.2f} s".format(end - start))
        print("{} moves: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos

    def _create_node(self, game_state, parent, parent_move) -> NodeMCTS:
        """This method creates a new MCTS node"""

        return NodeMCTS(game_state, parent, parent_move)

    # [END METHODS]


class GameTreeDynamicMinimax(GameTreeMinimax):
    """This class is responsible for performance of the Dynamic Minimax game tree"""

    # [BEGIN METHODS]
    # Instance method

    def process(self, moves_queue) -> tuple:
        """Let the bot run"""
        # [START BOT'S TURN]
        ADVANTAGE_CONSTANT = 25

        start = time()  # Start the time counter
        print(self.current_node.game_state.value * self.team.value)
        # If the branching factor of the current node is <= 3, then run at target depth + 2
        if len(self.current_node.game_state.all_child_gamestates) <= 3:
            self.current_node.minimax(self.target_depth + 2, self.team is Team.RED)
        # If the advantage value of the current node is >= the advantage constant,
        # Then run at target depth + 1
        elif self.current_node.game_state.value * self.team.value >= ADVANTAGE_CONSTANT:
            self.current_node.minimax(self.target_depth + 1, self.team is Team.RED)
        # If the advantage value of the current node is smaller the advantage constant,
        # Then run at target depth
        else:
            self.current_node.minimax(self.target_depth, self.team is Team.RED)
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        # [POST PROCESS]
        print(self.count)
        self.count = 0
        end = time()  # End the time counter
        print("Time: {:.2f} s".format(end - start))
        print("{} moves: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos

        # [END BOT'S TURN]

    # [END METHOD]


class GameTreeDeepeningMinimax(GameTreeMinimax):
    """This class is responsible for performance of the Deepening Minimax game tree"""

    # [BEGIN METHODS]
    # Instance method

    def process(self, moves_queue) -> tuple:
        """Let the bot run"""

        # [START BOT'S TURN]
        # The coefficients for each value pack
        if self._value_pack == 1:
            DEPTH_VALUE_CONSTANT = [0, 1, 2, 3, 16, 12]
        elif self._value_pack == 2:
            DEPTH_VALUE_CONSTANT = [0, 1, 1, 2, 4, 7]

        start = time()  # Start the time counter
        # Find the list of best moves
        best_moves = dict()
        for depth in range(1, self.target_depth + 1):
            if DEPTH_VALUE_CONSTANT[depth] == 0:
                continue
            self.current_node.minimax(depth, self.team is Team.RED)
            for child in self.current_node.list_of_children:
                if child.minimax_value == self.current_node.minimax_value:
                    key = child.parent_move
                    best_moves[key] = (
                        best_moves.get(key, 0) + DEPTH_VALUE_CONSTANT[depth]
                    )
                    print(depth, key)

        # Find the best value
        old_pos, new_pos = None, None
        max_move_val = -inf
        for key, val in best_moves.items():
            if val > max_move_val:
                max_move_val = val
                old_pos, new_pos = key

        print("Move value:", best_moves[(old_pos, new_pos)])
        self.move_to_child_node_with_move(old_pos, new_pos)
        moves_queue.append((old_pos, new_pos))

        # [POST PROCESS]
        print(self.count)
        self.count = 0
        end = time()  # End the time counter
        print("Time: {:.2f} s".format(end - start))
        print("{} moves: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos

        # [END BOT'S TURN]

    # [END METHODS]


class GameTreeExcavationMinimax(GameTreeMinimax):
    """This class is responsible for performance of the Excavation Minimax game tree"""

    # [BEGIN INITIALIZATION]

    def __init__(self, team, value_pack: int = 2, rollout_policy="RANDOM"):
        super().__init__(team, value_pack)
        self.rollout_policy = rollout_policy

    # [END INITIALIZATION]

    # [BEGIN METHODS]

    def _create_node(self, game_state, parent, parent_move) -> NodeExcavationMinimax:
        return NodeExcavationMinimax(game_state, parent, parent_move)

    # [END METHODS]
