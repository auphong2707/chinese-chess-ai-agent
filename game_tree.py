# Made by Kleecon~
from math import inf
from abc import ABC, abstractmethod
from game_state import GameState
from node import NodeMinimax, NodeMCTS, NodeExcavationMinimax
from time import time
from team import Team
from random import choice


class GameTree(ABC):
    """This class is responsible for the game tree representation"""

    MAX_NODE = inf

    def __init__(self, team: Team, value_pack: int=0) -> None:
        # This generates the initial game tree, not a forged one
        self.team = team
        self.current_node = self._create_node(
            GameState.generate_initial_game_state(value_pack), None, None
        )
        self._value_pack = value_pack
        self.count = 0

    def move_to_best_child(self) -> tuple:
        """This moves the current node to its "best child" on the game tree"""
        self.current_node = self.current_node.best_move()
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
            if new_state.board == node.game_state.board:
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


class GameTreeMinimax(GameTree):
    """This class is responsible for the game tree minimax"""

    def __init__(self, team, target_depth, value_pack: int=0):
        super().__init__(team, value_pack)
        self.target_depth = target_depth

    def _create_node(self, game_state, parent, parent_move) -> NodeMinimax:
        return NodeMinimax(game_state, parent, parent_move)

    def process(self, moves_queue) -> tuple:
        """Let the bot run"""
        # [START BOT'S TURN]

        start = time()  # Start time counter
        self.current_node.minimax(self.target_depth, self.team is Team.RED)
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        # [POST PROCESS]
        print(self.current_node.minimax_value)
        self.count = 0
        end = time()  # End time counter
        print("Time: {:.2f} s".format(end - start))
        print("{} moves: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos

        # [END BOT'S TURN]


class GameTreeMCTS(GameTree):
    """This class is responsible for performance of the MCTS game tree"""

    def __init__(self, team, time_allowed, value_pack: int=2, rollout_policy = "RANDOM"):
        super().__init__(team, value_pack)
        self.time_allowed = time_allowed
        self.rollout_policy = rollout_policy

    def traverse(self, node: NodeMCTS) -> NodeMCTS:
        """This module performs the MCTS initial traversion"""

        if len(node.list_of_children) > 0:
            return self.traverse(node.best_uct())
        else:
            return node

    def monte_carlo_tree_search(self, root):
        """This function performs the MCTS itself"""

        root.num = 0
        starting_time = time()
        while time()-starting_time < self.time_allowed:
            root.num += 1
            leaf = self.traverse(root)
            leaf.generate_all_children()
            stimulation_result = leaf.rollout(self.rollout_policy)
            leaf.backpropagate(stimulation_result)

    def process(self, moves_queue) -> tuple:
        """Let the bot run"""
        # [START BOT'S TURN]

        start = time()  # Start time counter
        self.monte_carlo_tree_search(self.current_node)
        old_pos, new_pos = self.move_to_best_child()
        moves_queue.append((old_pos, new_pos))

        # [POST PROCESS]
        print(self.count)
        self.count = 0
        end = time()  # End time counter
        print("Time: {:.2f} s".format(end - start))
        print("{} moves: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos
    
    def _create_node(self, game_state, parent, parent_move) -> NodeMCTS:
        return NodeMCTS(game_state, parent, parent_move)
    
class GameTreeDynamicMinimax(GameTreeMinimax):
    def process(self, moves_queue) -> tuple:
        """Let the bot run"""
        # [START BOT'S TURN]
        ADVANTAGE_CONSTANT = 25

        start = time()  # Start time counter
        print(self.current_node.game_state.value * self.team.value)
        if len(self.current_node.game_state.all_child_gamestates) <= 3:
            self.current_node.minimax(self.target_depth + 2, self.team is Team.RED)
        elif self.current_node.game_state.value * self.team.value >= ADVANTAGE_CONSTANT:
            self.current_node.minimax(self.target_depth + 1, self.team is Team.RED)
        else:
            self.current_node.minimax(self.target_depth, self.team is Team.RED)
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

class GameTreeDeepeningMinimax(GameTreeMinimax):
    def process(self, moves_queue) -> tuple:
        """Let the bot run"""
        # [START BOT'S TURN]
        if self._value_pack == 1:
            DEPTH_VALUE_CONSTANT = [0, 1, 2, 3, 16, 12]
        elif self._value_pack == 2:
            DEPTH_VALUE_CONSTANT = [0, 1, 1, 2, 4, 7]

        start = time()  # Start time counter
        # Find list of best moves
        best_moves = dict()
        for depth in range(1, self.target_depth + 1):
            if DEPTH_VALUE_CONSTANT[depth] == 0:
                continue
            self.current_node.minimax(depth, self.team is Team.RED)
            for child in self.current_node.list_of_children:
                if child.minimax_value == self.current_node.minimax_value:
                    key = child.parent_move
                    best_moves[key] = best_moves.get(key, 0) + DEPTH_VALUE_CONSTANT[depth]
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
        end = time()  # End time counter
        print("Time: {:.2f} s".format(end - start))
        print("{} moves: {} -> {}".format(self.team.name, old_pos, new_pos))
        return old_pos, new_pos

        # [END BOT'S TURN]
        
class GameTreeExcavationMinimax(GameTreeMinimax):
    def __init__(self, team, value_pack: int=2, rollout_policy = "RANDOM"):
        super().__init__(team, value_pack)
        self.rollout_policy = rollout_policy
        
    def _create_node(self, game_state, parent, parent_move) -> NodeExcavationMinimax:
        return NodeExcavationMinimax(game_state, parent, parent_move)

