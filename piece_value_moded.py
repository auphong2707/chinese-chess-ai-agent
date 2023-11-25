# Edited by: Veil, Kleecon
"""Module providing the property of abstract class and team members"""
from abc import ABC, abstractmethod
from team import Team


class Piece(ABC):
    """This class is an abtract class which is inherited by every pieces in the game"""

    # [BEGIN CONSTANTS]

    _piece_value = None
    _piece_type = None

    # Board size
    BOARD_SIZE_X = 10
    BOARD_SIZE_Y = 9

    # Palace bound
    BOUND_PALACE_X_RED = tuple((7, 9))
    BOUND_PALACE_X_BLACK = tuple((0, 2))
    BOUND_PALACE_Y = tuple((3, 5))
    # [END CONSTANTS]

    # [BEGIN INITILIZATION]
    def __init__(self, position: tuple, team: Team) -> None:
        # Create properties
        self.position = position
        self.team = team

        self.admissible_moves = None

    def __str__(self) -> str:
        return str(self.team) + '_' + self._piece_type

    # Properties initialization
    # .position
    @property
    def position(self) -> tuple:
        """Getter of the position property, return the position of the piece"""
        return self._position

    @position.setter
    def position(self, new_position: tuple) -> None:
        """Setter of the position property, recieve a position as a tuple"""
        if self.is_position_on_board(new_position) is False:
            raise ValueError("The position is out of range")

        self._position = new_position

    # .piece value
    @property
    def piece_value(self):
        """This method return the value of the piece"""
        return self._piece_value

    @property
    def has_crossed_river(self):
        """Return True if the piece is crossed the river"""
        return abs(self.position[0] + 9 * (self.team.value - 1) / 2) < 5
        
    # [END INITILIZATION]

    # [BEGIN METHODS]
    # Instance method
    def _get_piece_team_on_position(self, position: tuple, board: tuple) -> Team:
        """Return the team of the piece on the position (Team.NONE, Team.RED, Team.BLACK)"""
        if self.is_position_on_board(position) is False:
            raise ValueError("The position is out of range")

        return board[position[0]][position[1]]

    def is_position_teammate(self, position: tuple, board: tuple):
        """Return True if the piece on the position is teammate piece, vice versa"""
        return self._get_piece_team_on_position(position, board) is self.team

    def is_position_free(self, position: tuple, board: tuple):
        """Return True if there is no piece on the position, vice versa"""
        return self._get_piece_team_on_position(position, board) is Team.NONE

    def is_position_opponent(self, position: tuple, board: tuple):
        """Return True if the piece on the position is opponent piece, vice versa"""
        return self._get_piece_team_on_position(position, board).value == -self.team.value

    def set_admissible_moves(self, board: tuple):
        """This method will set a new list of admissible moves of the piece"""
        self.admissible_moves = self.get_admissible_moves(board)

    # Abstract method
    @abstractmethod
    def get_admissible_moves(self, board: tuple) -> list:
        """Abstract method that return the list of admissible moves of a piece.
        This method is used to initialize the piece"""
        pass

    @abstractmethod
    def create_copy(self):
        """This return a copy of current piece with a new attached board"""
        pass

    # Static method
    @staticmethod
    def is_position_on_board(position: tuple) -> bool:
        """Return True if the position is a valid position of the board, vice versa"""
        # Check if x component is on the board
        result_x = position[0] >= 0 and position[0] < Piece.BOARD_SIZE_X

        # Check if y component is on the board
        result_y = position[1] >= 0 and position[1] < Piece.BOARD_SIZE_Y

        return result_x and result_y

    @staticmethod
    def is_position_in_palace(position: tuple) -> bool:
        """Return True if the position is in the palace, vice versa"""
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


class Advisor(Piece):
    """Class representing an advisor"""

    _piece_value = 20
    _piece_type = 'advisor'

    @property
    def piece_value(self):
        if len(self.admissible_moves) == 0:
            self._piece_value = 10
        return self._piece_value
      
    def get_admissible_moves(self, board: tuple):
        # Movement
        admissible_moves = []

        # Possible goal positions
        x_orient = [1, 1, -1, -1]
        y_orient = [1, -1, -1, 1]
        maximum_move_count = 4

        # Iteration through all positions
        for cnt in range(maximum_move_count):
            # Possible position setting
            pos = (self.position[0] + x_orient[cnt],
                   self.position[1] + y_orient[cnt])

            # Checkment
            if (
                self.is_position_on_board(pos)
                and not self.is_position_teammate(pos, board)
                and self.is_position_in_palace(pos)
            ):
                admissible_moves.append(pos)

        # Return
        return admissible_moves

    def create_copy(self):
        return Advisor(self.position, self.team)


class Cannon(Piece):
    """Class representing a cannon"""

    _piece_value = 45
    _piece_type = 'cannon'
    
    @property
    def piece_value(self):
        if len(self.admissible_moves) == 0:
            self._piece_value = 35
        return self._piece_value
    
    def get_admissible_moves(self, board: tuple) -> list:
        x_direction = [1, -1, 0, 0]
        y_direction = [0, 0, 1, -1]
        admissible_moves = []

        for direction in range(4):
            piece_behind = 0

            for steps in range(1, 10):
                new_position = (self.position[0] + steps*x_direction[direction],
                                self.position[1] + steps*y_direction[direction])

                # Check if the new position is on the board
                if self.is_position_on_board(new_position):

                    # Check if there is any piece on the new position
                    if self.is_position_free(new_position, board) is False:
                        piece_behind += 1

                        # If there is an enemy piece behind the piece in new position
                        if piece_behind == 2 and self.is_position_opponent(new_position, board):

                            admissible_moves.append(new_position)
                            break

                    elif piece_behind == 0:
                        admissible_moves.append(new_position)

        return admissible_moves

    def create_copy(self):
        return Cannon(self.position, self.team)


class Chariot(Piece):
    """Class representing a chariot"""

    _piece_value = 90
    _piece_type = 'chariot'

    @property
    def piece_value(self):
        if len(self.admissible_moves) == 0:
            self._piece_value = 80
        return self._piece_value
    
    def get_admissible_moves(self, board: tuple) -> list:
        x_direction = [1, -1, 0, 0]
        y_direction = [0, 0, 1, -1]

        admissible_moves = []

        for direction in range(4):
            for steps in range(1, 10):
                new_position = (
                    self.position[0] + steps * x_direction[direction],
                    self.position[1] + steps * y_direction[direction],
                )

                # Check if the new position is on the board
                if self.is_position_on_board(new_position):
                    # Check if there is any piece on the new position
                    if self.is_position_free(new_position, board) is False:
                        # Check if the piece on the new position is on the enemy team
                        if self.is_position_opponent(new_position, board):
                            admissible_moves.append(new_position)
                        break

                    admissible_moves.append(new_position)

        return admissible_moves

    def create_copy(self):
        return Chariot(self.position, self.team)


class Elephant(Piece):
    """Class representing an elephant"""

    _piece_value = 25
    _piece_type = 'elephant'

    @property
    def piece_value(self):
        if len(self.admissible_moves) == 0:
            self._piece_value = 15
        return self._piece_value
    
    def _cross_river(self, position: tuple):
        """Return True if the piece cross river, vice versa"""
        if self.team is Team.RED and position[0] < 6:
            return True
        if self.team is Team.BLACK and position[0] > 5:
            return True
        return False

    def get_admissible_moves(self, board: tuple):
        admissible_moves = []

        # Possible goal positions
        x_direction = [2, 2, -2, -2]
        y_direction = [2, -2, 2, -2]
        maximum_move_count = 4

        # Possible block positions
        x_block = [1, 1, -1, -1]
        y_block = [1, -1, 1, -1]

        for direction in range(maximum_move_count):
            new_pos = (
                self.position[0] + x_direction[direction],
                self.position[1] + y_direction[direction],
            )

            block_pos = (
                self.position[0] + x_block[direction],
                self.position[1] + y_block[direction],
            )

            # Check if all the conditions below met to add admissible moves for elephant piece
            if (
                self.is_position_on_board(new_pos)
                and self.is_position_free(block_pos, board)
                and not self._cross_river(new_pos)
                and not self.is_position_teammate(new_pos, board)
            ):
                admissible_moves.append(new_pos)

        return admissible_moves

    def create_copy(self):
        return Elephant(self.position, self.team)


class General(Piece):
    """Class representing a general"""

    _piece_value = 0
    _piece_type = 'general'

    def get_admissible_moves(self, board: tuple) -> list:
        x_direction = [1, -1, 0, 0]
        y_direction = [0, 0, 1, -1]

        admissible_moves = []

        for direction in range(4):
            new_position = (
                self.position[0] + x_direction[direction],
                self.position[1] + y_direction[direction],
            )

            # Check if the new position is in the palace
            if self.is_position_in_palace(new_position):
                # Check if there is any piece on the new position
                if self.is_position_free(new_position, board):
                    admissible_moves.append(new_position)

                # Check if the piece on the new position is on the enemy team
                elif self.is_position_opponent(new_position, board):
                    admissible_moves.append(new_position)

        return admissible_moves

    def create_copy(self):
        return General(self.position, self.team)


class Pawn(Piece):
    """Class representing a pawn"""

    _piece_value = 10
    _piece_type = 'pawn'

    @property
    def piece_value(self):
        if self.team is Team.RED:
            if self.position == (3, 4):
                self._piece_value = 30
            elif self.position[0] == 5 or self.position[0] == 6:
                self._piece_value = 20
            elif self.position[0] == 7 or self.position[0] == 8:
                if self.position[1] < 7 and self.position[1] > 1:
                    self._piece_value = 30
                else:
                    self._piece_value = 20
        if self.team is Team.BLACK:
            if self.position == (6, 4):
                self._piece_value = 30
            elif self.position[0] == 3 or self.position[0] == 4:
                self._piece_value = 20
            elif self.position[0] == 1 or self.position[0] == 2:
                if self.position[1] < 7 and self.position[1] > 1:
                    self._piece_value = 30
                else:
                    self._piece_value = 20
        return self._piece_value

    # Searching admissible moves for the pawn
    def get_admissible_moves(self, board: tuple) -> list:
        possible_moves = []

        # Movement
        new_pos = (self.position[0] - self.team.value, self.position[1])
        if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos, board):
            possible_moves.append(new_pos)

        if self.has_crossed_river is True:
            new_pos = (self.position[0], self.position[1] + 1)
            if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos, board):
                possible_moves.append(new_pos)

            new_pos = (self.position[0], self.position[1] - 1)
            if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos, board):
                possible_moves.append(new_pos)

        # Capture (it's the same with movement, dang it)

        return possible_moves

    def create_copy(self):
        return Pawn(self.position, self.team)


class Horse(Piece):
    """Class representing a horse"""

    _piece_value = 40
    _piece_type = 'horse'

    @property
    def piece_value(self):
        if len(self.admissible_moves) == 0 or len(self.admissible_moves) == 1:
            self._piece_value = 30
        if len(self.admissible_moves) == 2:
            self._piece_value = 35
        if len(self.admissible_moves) == 5 or len(self.admissible_moves) == 6:
            self._piece_value = 45
        if len(self.admissible_moves) == 7 or len(self.admissible_moves) == 8:
            self._piece_value = 50
        return self._piece_value
    
    def get_admissible_moves(self, board: tuple) -> list:

        # Movement
        admissible_moves = []

        # Possible goal positions
        x_orient = [2, 2, 1, -1, -2, -2, -1, 1]
        y_orient = [1, -1, -2, -2, -1, 1, 2, 2]
        maximum_move_count = 8

        # Possible middle move positions
        p_orient = [1, 0, -1, 0]
        q_orient = [0, -1, 0, 1]

        for cnt in range(maximum_move_count):

            # Middle position
            pos = (self.position[0] + p_orient[cnt//2],
                   self.position[1] + q_orient[cnt//2])

            # Check the middle position
            if self.is_position_on_board(pos)\
                    and self.is_position_free(pos, board):

                # Goal position
                pos = (self.position[0] + x_orient[cnt],
                       self.position[1] + y_orient[cnt])

                # Check the goal position
                if self.is_position_on_board(pos)\
                        and not self.is_position_teammate(pos, board):
                    admissible_moves.append(pos)

        # Return
        return admissible_moves

    def create_copy(self):
        return Horse(self.position, self.team)
