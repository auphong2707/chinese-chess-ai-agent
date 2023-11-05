# Edited by: Veil, Kleecon
from abc import ABC, abstractmethod
from team import Team


class Piece(ABC):
    '''This class is an abtract class which is inherited by every pieces in the game'''
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
        '''Getter of the position property, return the position of the piece'''
        return self._position

    @position.setter
    def position(self, new_position: tuple) -> None:
        if self.is_position_on_board(new_position) is False:
            raise ValueError("The position is out of range")

        self._position = new_position

    # .admissible moves
    @property
    def admissible_moves(self) -> list:
        '''Getter of the admissible_moves property, return the list of admissible move of a piece'''
        return self.admissible_moves

    @admissible_moves.setter
    def set_admissible_moves(self, other: list) -> None:
        self._admissible_moves = other

    # [END INITILIZATION]

    # [BEGIN METHODS]
    # Instance method
    def _get_piece_team_on_position(self, position: tuple) -> Team:
        '''Return the team of the piece on the position (Team.NONE, Team.RED, Team.BLACK)'''
        if self.is_position_on_board(position) is False:
            raise ValueError("The position is out of range")

        return self._board[position[0]][position[1]]

    def is_position_free(self, position: tuple):
        '''Return True if there is no piece on the position, vice versa'''
        return self.get_piece_team_on_position(position) is Team.NONE

    def is_position_opponent(self, position: tuple):
        '''Return True if the piece on the position is opponent piece, vice versa'''
        return self.get_piece_team_on_position(position).value == -self.team.value

    # Abstract method
    @abstractmethod
    def get_admissible_moves(self) -> list:
        '''Abstract method that return the list of admissible moves of a piece.
        This method is used to initialize the piece'''
        pass

    # Static method
    @staticmethod
    def is_position_on_board(position: tuple) -> bool:
        '''Return True if the position is a valid position of the board, vice versa'''
        # Check if x component is on the board
        result_x = position[0] >= 0 and position[0] < Piece.BOARD_SIZE_X

        # Check if y component is on the board
        result_y = position[1] >= 0 and position[1] < Piece.BOARD_SIZE_Y

        return result_x and result_y

    @staticmethod
    def is_position_in_palace(position: tuple) -> bool:
        '''Return True if the position is in the palace, vice versa'''
        # Check if x component is in the palace
        result_x = (
            position[0] >= Piece.BOUND_PALACE_X_BLACK[0]
            and position[0] <= Piece.BOUND_PALACE_X_BLACK[1]
        ) or (
            position[0] >= Piece.BOUND_PALACE_X_RED[0]
            and position[0] <= Piece.BOUND_PALACE_X_RED[1]
        )

        # Check if y component is on the board
        result_y = (
            position[1] >= Piece.BOUND_PALACE_Y[0]
            and position[1] <= Piece.BOUND_PALACE_Y[1]
        )

        return result_x and result_y

    # [END METHODS]
