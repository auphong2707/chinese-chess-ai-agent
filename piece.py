# Edited by: Veil, Kleecon
from team import Team
from abc import ABC, abstractmethod


class Piece(ABC):
    # [BEGIN CONSTANTS]
    # Board size
    BOARD_SIZE_X = 10
    BOARD_SIZE_Y = 9

    # Palace bound
    BOUND_PALACE_X_RED = tuple((7, 9))
    BOUND_PALACE_X_BLACK = tuple((0, 2))
    BOUND_PALACE_Y = tuple((3, 5))
    # [END CONSTANTS]

    # [BEGIN INITILIZATION]
    def __init__(self, position: tuple, team: Team, board: tuple) -> None:
        # Create properties
        self.position = position
        self.team = team
        self._board = board
        self.admissible_moves = self.get_admissible_moves()

    # Properties initialization
    # .position
    @property
    def position(self) -> tuple:
        return self._position

    @position.setter
    def position(self, new_position: tuple) -> None:
        if self.is_position_on_board(new_position) is False:
            raise ValueError("The position is out of range")

        self._position = new_position

    # .admissible moves
    @property
    def admissible_moves(self) -> list:
        return self.admissible_moves

    @admissible_moves.setter
    def set_admissible_moves(self, other: list) -> None:
        self._admissible_moves = other
    # [END INITILIZATION]

    # [BEGIN METHODS]
    # Instance method
    def get_piece_team_on_position(self, position: tuple) -> Team:
        if self.is_position_on_board(position) is False:
            raise ValueError("The position is out of range")
        
        return self._board[position[0]][position[1]]

    def is_position_free(self, position: tuple):
        return self.get_piece_team_on_position(position) is Team.NONE

    def is_position_opponent(self, position: tuple):
        return self.get_piece_team_on_position(position).value == -self.team.value

    # Abstract method
    @abstractmethod
    def get_admissible_moves(self) -> list:
        pass

    @abstractmethod
    def is_valid_move(self, position: tuple) -> bool:
        # Check if the move to the position is available by all means
        pass

    # Static method
    @staticmethod
    def is_position_on_board(position: tuple) -> bool:
        # Check if x component is on the board
        result_x = position[0] >= 0 and position[0] < Piece.BOARD_SIZE_X

        # Check if y component is on the board
        result_y = position[1] >= 0 and position[1] < Piece.BOARD_SIZE_Y

        return result_x and result_y

    @staticmethod
    def is_position_in_palace(position: tuple) -> bool:
        # Check if x component is in the palace
        result_x = (
            position[0] >= Piece.BOUND_PALACE_X_BLACK[0]
            and position[0] <= Piece.BOUND_PALACE_X_BLACK[1]
        ) or (
            position[0] >= Piece.BOUND_PALACE_X_RED[0]
            and position[0] <= Piece.BOUND_PALACE_X_RED[1]
        )

        # Check if y component is on the board
        result_y = position[1] >= Piece.BOUND_PALACE_Y[0] and position[1] <= Piece.BOUND_PALACE_Y[1]

        return result_x and result_y

    

    # [END METHODS]

