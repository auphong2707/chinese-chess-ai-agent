# Made by: Veil
from copy import deepcopy
from random import randint
from piece import Piece
from team import Team


class GameState:
    """This class respresents the state of game containing
    information and transforming method"""

    # [BEGIN CONSTANTS]
    # Board size
    BOARD_SIZE_X = 10
    BOARD_SIZE_Y = 9

    # [BEGIN INITILIZATION]
    def __init__(self, chess_pieces: list, board: tuple, current_team) -> None:
        # Add the chess pieces to the list
        self.chess_pieces = chess_pieces

        # Declare read-only properties
        self._value = None
        self._checked_team = Team.NONE
        self._win_status = None
        self._board = board
        self._current_team = current_team

    # Properties initialization
    # .value
    @property
    def value(self) -> float:
        """This is the Getter function of the value property,
        return the value of the game state using chess pieces value"""

        if self._value is None:
            self._value = self._get_board_value()

        return self._value

    # .checked_team
    @property
    def checked_team(self) -> Team:
        """This is the Getter function of the checked_team property,
        return the team which checkmates the opponent"""

        if self._checked_team is Team.NONE:
            self._checked_team = self._get_checked_team

        return self._checked_team

    # .win_status
    @property
    def win_status(self) -> bool:
        """This is the Getter function of the win_status property.
        If the state always recieves victory, then this will return True"""

        if self._win_status is None:
            self.win_status = self._get_win_status()

        return self._win_status

    # [END INITILIZATION]

    # [BEGIN METHOD]
    # Instance method
    def _get_board_value(self):
        # Incomplete code: Return the evaluation value of the board
        return 0

    def _get_checked_team(self):
        # Incomplete code: Return the team that checked the oponent in this state
        return Team.NONE

    def _get_win_status(self):
        # Incomplete code: Return the evaluation result that confirm this state
        # can always end the game with the victory
        return False
    
    def _get_the_opponent_team(self):
        """This method will return the opponent team in this game state"""
        if self._current_team is Team.BLACK:
            return Team.RED
        else:
            return Team.BLACK

    def generate_random_game_state(self, policy):
        """This method will generate another gamestate that can be tranformed
        by current method using each move of the piece"""

        pass

    # [END METHOD]
