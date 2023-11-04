# Made by: Veil
from piece import Piece
from team import Team


class GameState:
    # [BEGIN CONSTANTS]
    # Board size
    BOARD_SIZE_X = 10
    BOARD_SIZE_Y = 9
    # [END CONSTANTS]

    # [BEGIN INITILIZATION]
    def __init__(self, chess_pieces: list) -> None:
        # Add the chess pieces to the list
        self.chess_pieces = chess_pieces

        # Declare read-only properties
        self._value = None
        self._checked_team = Team.NONE
        self._win_status = None

    # Properties initialization
    # .value
    @property
    def value(self) -> float:
        if self._value is None:
            self._value = self._get_board_value()

        return self._value
    
    # .checked_team
    @property
    def checked_team(self) -> Team:
        if self._checked_team is Team.NONE:
            self._checked_team = self._get_checked_team

        return self._checked_team

    # .win_status
    @property
    def win_status(self) -> bool:
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

    # Class method
    @classmethod
    def generate_board_state(cls, policy):
        pass
    
    # [END METHOD]