# Edited by: Veil, Kleecon, TheSyx, Whatsoever
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
    def __init__(
        self,
        position: tuple,
        team: Team,
        board: list,
        number_of_pieces: int,
        nummber_of_team_pieces: int,
    ) -> None:
        # Create properties
        self.position = position
        self.team = team

        self._admissible_moves = None
        self.board = board
        self.number_of_pieces = number_of_pieces
        self.number_of_team_pieces = nummber_of_team_pieces

    def __str__(self) -> str:
        return str(self.team) + "_" + self._piece_type

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

    @property
    def admissible_moves(self) -> list:
        """Getter of admissible_moves property,
        return a list of admissible movement of a piece"""
        if self._admissible_moves is None:
            self._admissible_moves = self.get_admissible_moves()

        return self._admissible_moves

    # [END INITILIZATION]

    # [BEGIN METHODS]
    # Instance method
    def _get_piece_team_on_position(self, position: tuple) -> Team:
        """Return the team of the piece on the position (Team.NONE, Team.RED, Team.BLACK)"""
        if self.is_position_on_board(position) is False:
            raise ValueError("The position is out of range")

        notation = self.board[position[0]][position[1]]
        if notation == "NN":
            return Team.NONE
        else:
            return Team[self.board[position[0]][position[1]][0]]

    def is_position_teammate(self, position: tuple) -> bool:
        """Return True if the piece on the position is on the same team, vice versa"""
        return self._get_piece_team_on_position(position) is self.team

    def is_position_free(self, position: tuple) -> bool:
        """Return True if there is no piece on the position, vice versa"""
        return self._get_piece_team_on_position(position) is Team.NONE

    def is_position_opponent(self, position: tuple) -> bool:
        """Return True if the piece on the position is the opponent's piece, vice versa"""
        return self._get_piece_team_on_position(position).value == -self.team.value

    def is_crossed_river(self) -> bool:
        """Return True if the piece has crossed the river"""
        return abs(self.position[0] + 9 * (self.team.value - 1) / 2) < 5

    # Abstract method
    @abstractmethod
    def piece_value(self, value_pack=0) -> float:
        """This method return the value of the piece"""
        pass

    @abstractmethod
    def get_admissible_moves(self) -> list:
        """Abstract method that return the list of admissible moves of a piece.
        This method is used to initialize the piece"""
        pass

    # Static method
    @staticmethod
    def is_position_on_board(position: tuple) -> bool:
        """Return True if the position is a valid position on the board, vice versa"""
        # Check if the x component is on the board
        result_x = position[0] >= 0 and position[0] < Piece.BOARD_SIZE_X

        # Check if the y component is on the board
        result_y = position[1] >= 0 and position[1] < Piece.BOARD_SIZE_Y

        return result_x and result_y

    @staticmethod
    def is_position_in_palace(position: tuple) -> bool:
        """Return True if the position is in the palace, vice versa"""
        # Check if the x component is in the palace
        result_x = (
            position[0] >= Piece.BOUND_PALACE_X_BLACK[0]
            and position[0] <= Piece.BOUND_PALACE_X_BLACK[1]
        ) or (
            position[0] >= Piece.BOUND_PALACE_X_RED[0]
            and position[0] <= Piece.BOUND_PALACE_X_RED[1]
        )

        # Check if the y component is on the board
        result_y = (
            position[1] >= Piece.BOUND_PALACE_Y[0]
            and position[1] <= Piece.BOUND_PALACE_Y[1]
        )

        return result_x and result_y

    @staticmethod
    def create_instance(
        position: tuple,
        notation: str,
        board: list,
        number_of_pieces: int,
        number_of_team_pieces: int,
    ):
        """This method creates an instance of a piece
        depending on the input notation and other additional arguments"""
        team = Team[notation[0]]
        piece_type = notation[1]
        match piece_type:
            case "A":
                return Advisor(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "C":
                return Cannon(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "E":
                return Elephant(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "G":
                return General(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "H":
                return Horse(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "P":
                return Pawn(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )
            case "R":
                return Rook(
                    position, team, board, number_of_pieces, number_of_team_pieces
                )

    # [END METHODS]


class Advisor(Piece):
    """Class representing the advisor piece"""

    _piece_value = 20
    _piece_type = "advisor"

    def piece_value(self, value_pack: int = 0) -> float:
        # Default value pack
        if value_pack == 0:
            return self._piece_value

        # Value pack 1
        elif value_pack == 1:
            change = 0
            # If the advisor has no admissible moves, it receives a penalty of 10 points
            if len(self.admissible_moves) == 0:
                change = -10
            return self._piece_value + change

        # Value pack 2
        elif value_pack == 2:
            change = 0
            x_orient = [1, 1, -1, -1]
            y_orient = [1, -1, -1, 1]
            for cnt in range(4):
                # Possible position setting
                pos = (
                    self.position[0] + x_orient[cnt],
                    self.position[1] + y_orient[cnt],
                )

                # If the 2 advisors are connected, they receive a bonus of 5 points
                if self.is_position_on_board(pos) and self.is_position_in_palace(pos):
                    if self.board[pos[0]][pos[1]][1] == "A":
                        change += 5

            return self._piece_value + change

        # If the value pack is not found
        else:
            raise ValueError("Value pack is not found")

    def get_admissible_moves(self) -> list:
        # Create a list of admissible moves for the advisor
        admissible_moves = []

        # Possible goal positions
        x_orient = [1, 1, -1, -1]
        y_orient = [1, -1, -1, 1]
        maximum_move_count = 4

        # Iterate through all positions
        for cnt in range(maximum_move_count):
            # New position
            pos = (self.position[0] + x_orient[cnt], self.position[1] + y_orient[cnt])

            # Chech whether the new position is legal
            if (
                self.is_position_on_board(pos)
                and not self.is_position_teammate(pos)
                and self.is_position_in_palace(pos)
            ):
                admissible_moves.append(pos)

        # Return the list of admissible moves
        return admissible_moves


class Cannon(Piece):
    """Class representing the cannon piece"""

    _piece_value = 45
    _piece_type = "cannon"

    def piece_value(self, value_pack: int = 0) -> float:
        # Default value pack
        if value_pack == 0:
            return self._piece_value

        # Value pack 1
        elif value_pack == 1:
            change = 0
            # Receive a penalty of 10 points if the cannon has no admissible moves
            if len(self.admissible_moves) == 0:
                change = -10
            return self._piece_value + change

        # Value pack 2
        elif value_pack == 2:
            change = 0
            # Receive a penalty of 10 points if the cannon has no admissible moves
            if len(self.admissible_moves) == 0:
                change += -10
            # Receive a bonus or penalty based on the game phase
            change += (self.number_of_pieces - 16) * 0.75
            # Avoid trading when losing
            change += (16 - self.number_of_team_pieces) * 0.25
            return self._piece_value + change

        # If the value pack is not found
        else:
            raise ValueError("Value pack is not found")

    def get_admissible_moves(self) -> list:
        # Create a list of admissible moves for the cannon
        admissible_moves = []

        # Define possible direction of the piece
        x_direction = [1, -1, 0, 0]
        y_direction = [0, 0, 1, -1]

        # Iterate through direction
        for direction in range(4):
            piece_behind = 0

            # Gradually increase the steps
            for steps in range(1, 10):
                # Calculate the new position
                new_position = (
                    self.position[0] + steps * x_direction[direction],
                    self.position[1] + steps * y_direction[direction],
                )

                # Check if the new position is on the board
                if self.is_position_on_board(new_position):
                    # Check if there is any piece on the new position
                    if self.is_position_free(new_position) is False:
                        piece_behind += 1

                        # If there is an enemy piece behind the piece in new position
                        if piece_behind == 2 and self.is_position_opponent(
                            new_position
                        ):
                            admissible_moves.append(new_position)
                            break

                    elif piece_behind == 0:
                        admissible_moves.append(new_position)

        return admissible_moves


class Rook(Piece):
    """Class representing the rook piece"""

    _piece_value = 90
    _piece_type = "rook"

    def __init__(
        self,
        position: tuple,
        team: Team,
        board: list,
        number_of_pieces: int,
        number_of_team_pieces: int,
    ) -> None:
        super().__init__(position, team, board, number_of_pieces, number_of_team_pieces)
        self._control_pos_count = 0

    def piece_value(self, value_pack: int = 0) -> float:
        # Default value pack
        if value_pack == 0:
            return self._piece_value

        # Value pack 1
        elif value_pack == 1:
            change = 0
            # Receive a penalty of 10 points if the rook has no admissible moves
            if len(self.admissible_moves) == 0:
                change = -10
            else:
                # Receive a bonus based on the number of positions the rook controls
                change = self._control_pos_count * 0.5
            return self._piece_value + change

        # Value pack 2
        elif value_pack == 2:
            change = 0
            # Receive a penalty of 10 points if the rook has no admissible moves
            if len(self.admissible_moves) == 0:
                change += -10
            # Receive a bonus based on the number of positions the rook controls
            else:
                change += self._control_pos_count * 0.5
            # Avoid trading when losing
            change += (16 - self.number_of_team_pieces) * 0.25
            # Receive a bonus based on the game phase and whether it has crossed the river
            change += (32 - self.number_of_pieces) * int(self.is_crossed_river())
            return self._piece_value + change

        # If the value pack is not found
        else:
            raise ValueError("Value pack is not found")

    def get_admissible_moves(self) -> list:
        # Create a list of admissible moves for the rook
        admissible_moves = []

        # Define possible direction of the piece
        x_direction = [1, -1, 0, 0]
        y_direction = [0, 0, 1, -1]

        # Iterate through direction
        for direction in range(4):
            # Gradually increase the steps
            for steps in range(1, 10):
                # Calculate the new position
                new_position = (
                    self.position[0] + steps * x_direction[direction],
                    self.position[1] + steps * y_direction[direction],
                )

                # Check if the new position is on the board
                if self.is_position_on_board(new_position):
                    # Check if there is any piece on the new position
                    if self.is_position_free(new_position) is False:
                        # Check if the piece on the new position is on the enemy team
                        if self.is_position_opponent(new_position):
                            admissible_moves.append(new_position)
                        break
                    else:
                        self._control_pos_count = self._control_pos_count + 1
                    admissible_moves.append(new_position)

        return admissible_moves


class Elephant(Piece):
    """Class representing the elephant piece"""

    _piece_value = 25
    _piece_type = "elephant"

    def _cross_river(self, position: tuple) -> bool:
        """Return True if a piece has crossed the river, vice versa"""
        if self.team is Team.RED and position[0] < 5:
            return True
        if self.team is Team.BLACK and position[0] > 4:
            return True
        return False

    def piece_value(self, value_pack: int = 0) -> float:
        # Default value pack
        if value_pack == 0:
            return self._piece_value

        # Value pack 1
        elif value_pack == 1:
            change = 0
            # Receive a penalty of 10 points if the elephant has no admissible moves
            if len(self.admissible_moves) == 0:
                change = -10
            return self._piece_value + change

        # Value pack 2
        elif value_pack == 2:
            change = 0
            # Possible goal positions
            x_direction = [2, 2, -2, -2]
            y_direction = [2, -2, 2, -2]

            # Possible block positions
            x_block = [1, 1, -1, -1]
            y_block = [1, -1, 1, -1]

            for direction in range(4):
                new_pos = (
                    self.position[0] + x_direction[direction],
                    self.position[1] + y_direction[direction],
                )
                block_pos = (
                    self.position[0] + x_block[direction],
                    self.position[1] + y_block[direction],
                )

                # Check if all the conditions below are met to add admissible moves for the elephant
                if (
                    self.is_position_on_board(new_pos)
                    and self.is_position_free(block_pos)
                    and not self._cross_river(new_pos)
                ):
                    # Receive a bonus if the 2 elephants are connected
                    if self.board[new_pos[0]][new_pos[1]][1] == "E":
                        change += 5
                        break
            return self._piece_value + change

        # If the value pack is not found
        else:
            raise ValueError("Value pack is not found")

    def get_admissible_moves(self) -> list:
        # Create a list of admissble moves for the elephant
        admissible_moves = []

        # Possible goal positions
        x_direction = [2, 2, -2, -2]
        y_direction = [2, -2, 2, -2]
        maximum_move_count = 4

        # Possible block positions
        x_block = [1, 1, -1, -1]
        y_block = [1, -1, 1, -1]

        # Iterate through direction
        for direction in range(maximum_move_count):
            new_pos = (
                self.position[0] + x_direction[direction],
                self.position[1] + y_direction[direction],
            )

            block_pos = (
                self.position[0] + x_block[direction],
                self.position[1] + y_block[direction],
            )

            # Check if all the conditions below are met to add admissible moves for the elephant
            if (
                self.is_position_on_board(new_pos)
                and self.is_position_free(block_pos)
                and not self._cross_river(new_pos)
                and not self.is_position_teammate(new_pos)
            ):
                admissible_moves.append(new_pos)

        return admissible_moves


class General(Piece):
    """Class representing the general piece"""

    _piece_value = 0
    _piece_type = "general"

    def piece_value(self, value_pack: int = 0) -> float:
        # Default value pack
        if value_pack == 0:
            return self._piece_value

        # Value pack 1
        elif value_pack == 1:
            return self._piece_value

        # Value pack 2
        elif value_pack == 2:
            opponent = Team.NONE
            if self.team is Team.RED:
                opponent = Team.BLACK
            else:
                opponent = Team.RED
            change = 0
            # Receive a penalty of 10 points if the general has no admissible moves
            if len(self.admissible_moves) == 0:
                change += -10
            # Receive a penalty of 15 points if the general is exposed
            if General.is_general_exposed(self.board, self.team, opponent) is True:
                change += -15

            return self._piece_value + change

        # If the value pack is not found
        else:
            raise ValueError("Value pack is not found")

    def get_admissible_moves(self) -> list:
        # Create a list of admissible moves for the general
        admissible_moves = []

        # Define possible direction of the piece
        x_direction = [1, -1, 0, 0]
        y_direction = [0, 0, 1, -1]

        # Iterate through direction
        for direction in range(4):
            # Calculate the new position
            new_position = (
                self.position[0] + x_direction[direction],
                self.position[1] + y_direction[direction],
            )

            # Check if the new position is in the palace
            if self.is_position_in_palace(new_position):
                # Check if there is any piece on the new position
                if self.is_position_free(new_position):
                    admissible_moves.append(new_position)

                # Check if the piece on the new position is on the enemy team
                elif self.is_position_opponent(new_position):
                    admissible_moves.append(new_position)

        return admissible_moves

    @staticmethod
    def is_general_exposed(board: list, current_team: Team, opponent: Team) -> bool:
        """This method returns True if the general is exposed"""

        # Find the position of the current team's General
        cur_general_pos = None

        for y in range(Piece.BOUND_PALACE_Y[0], Piece.BOUND_PALACE_Y[1] + 1):
            # Find the palace of current team
            bound_x = None
            if current_team is Team.RED:
                bound_x = Piece.BOUND_PALACE_X_RED
            elif current_team is Team.BLACK:
                bound_x = Piece.BOUND_PALACE_X_BLACK

            # Find the general
            for x in range(bound_x[0], bound_x[1] + 1):
                if board[x][y][1] == "G":
                    cur_general_pos = (x, y)

        # Check if the general is exposed
        # Possible directions of the cannon, the rook and the pawn
        x_str_dir, y_str_dir = [0, 0, -1, 1], [1, -1, 0, 0]

        # Possible directions of the horse
        x_horse_offset = [2, 1, -1, -2, -2, -1, 1, 2]
        y_horse_offset = [-1, -2, -2, -1, 1, 2, 2, 1]
        x_orient, y_orient = [1, -1, -1, 1], [-1, -1, 1, 1]

        # .Check the rook
        for direction in range(4):
            for steps in range(1, 10):
                # Get the position
                check_pos = (
                    cur_general_pos[0] + steps * x_str_dir[direction],
                    cur_general_pos[1] + steps * y_str_dir[direction],
                )
                # If the check position is out of the board then break
                if Piece.is_position_on_board(check_pos) is False:
                    break

                notation = board[check_pos[0]][check_pos[1]]
                # If the check position is of the same team with the general then break
                if Team[notation[0]] is not Team.NONE:
                    # If the enemy's rook is on the check position then return True
                    if Team[notation[0]] is opponent and notation[1] == "R":
                        return True
                    # Otherwise break
                    else:
                        break

        # .Check the horse
        for index in range(8):
            check_pos = (
                cur_general_pos[0] + x_horse_offset[index],
                cur_general_pos[1] + y_horse_offset[index],
            )
            # If the check position is out of the board then break
            if Piece.is_position_on_board(check_pos) is False:
                continue

            notation = board[check_pos[0]][check_pos[1]]
            # If the opponent horse is on the check position then return True
            if Team[notation[0]] is opponent and notation[1] == "H":
                mid_pos = (
                    cur_general_pos[0] + x_orient[index // 2],
                    cur_general_pos[1] + y_orient[index // 2],
                )
                mid_pos_notation = board[mid_pos[0]][mid_pos[1]]
                if mid_pos_notation == "NN":
                    return True

        # .Check the cannon
        for direction in range(4):
            piece_behind = 0
            for steps in range(1, 10):
                pos = (
                    cur_general_pos[0] + steps * x_str_dir[direction],
                    cur_general_pos[1] + steps * y_str_dir[direction],
                )
                # If the check position is out of the board then break
                if Piece.is_position_on_board(pos) is False:
                    break

                notation = board[pos[0]][pos[1]]
                # If there is 1 piece behind the check position
                # and the enemy's cannon is on the check position, then return True
                if (
                    piece_behind == 1
                    and Team[notation[0]] is opponent
                    and notation[1] == "C"
                ):
                    return True
                # Check whether there is a piece behind the check position
                if notation != "NN":
                    piece_behind += 1
                # Break if there are more than 1 piece behind the check position
                if piece_behind > 1:
                    break

        # .Check the pawn
        # Check left and right positions
        for index in range(2):
            check_pos = (
                cur_general_pos[0] + x_str_dir[index],
                cur_general_pos[1] + y_str_dir[index],
            )
            notation = board[check_pos[0]][check_pos[1]]
            # If the pawn is on the check position then return True
            if Team[notation[0]] is opponent and notation[1] == "P":
                return True
        # Check forward position
        forward_notation = board[cur_general_pos[0] + opponent.value][cur_general_pos[1]]
        if Team[forward_notation[0]] is opponent and forward_notation[1] == "P":
            return True

        # .Check the general
        for steps in range(1, 10):
            pos = (cur_general_pos[0] + steps * opponent.value, cur_general_pos[1])
            # If the check position is out of the board then break
            if Piece.is_position_on_board(pos) is False:
                break

            notation = board[pos[0]][pos[1]]
            if notation == "NN":
                continue
            # If the piece is opponent's general then return True
            if notation[1] == "G":
                return True
            # If the piece is other pieces then break
            else:
                break

        # If all check are passed, then return False
        return False


class Pawn(Piece):
    """Class representing the pawn piece"""

    _piece_value = 10
    _piece_type = "pawn"

    def piece_value(self, value_pack=0) -> float:
        # Default value pack
        if value_pack == 0:
            if self.is_crossed_river() is True:
                self._piece_value = 20
            return self._piece_value

        # Value pack 1
        elif value_pack == 1:
            change = 0
            # Receive a bonus based on the position of the pawn
            if self.team is Team.BLACK:
                if self.position == (3, 4):
                    change = 20
                elif self.position[0] == 5 or self.position[0] == 6:
                    change = 10
                elif self.position[0] == 7 or self.position[0] == 8:
                    if self.position[1] < 7 and self.position[1] > 1:
                        change = 20
                    else:
                        change = 10
            if self.team is Team.RED:
                if self.position == (6, 4):
                    change = 20
                elif self.position[0] == 3 or self.position[0] == 4:
                    change = 10
                elif self.position[0] == 1 or self.position[0] == 2:
                    if self.position[1] < 7 and self.position[1] > 1:
                        change = 20
                    else:
                        change = 10
            return self._piece_value + change

        # Value pack 2
        elif value_pack == 2:
            change = 0
            # Receive a bonus based on the position of the pawn
            if self.team is Team.BLACK:
                if self.position == (3, 4):
                    change += 20 - (32 - self.number_of_pieces) * 2
                elif self.position[0] in range(7, 9) and self.position[1] in range(2, 7):
                    change += 20
                elif self.position[0] in range(6, 9) and self.position[1] in range(1, 8):
                    change += 15
                elif self.is_crossed_river():
                    if self.position[0] == 9:
                        change += 0
                    else:
                        change += 10
            if self.team is Team.RED:
                if self.position == (6, 4):
                    change += 20 - (32 - self.number_of_pieces) * 2
                elif self.position[0] in range(1, 3) and self.position[1] in range(2, 7):
                    change += 20
                elif self.position[0] in range(1, 4) and self.position[1] in range(1, 8):
                    change += 15
                elif self.is_crossed_river():
                    if self.position[0] == 0:
                        change += 0
                    else:
                        change += 10
            # Receive a bonus based on the game phase
            change += (16 - self.number_of_team_pieces) * 2
            return self._piece_value + change

        # If the value pack is not found
        else:
            raise ValueError("Value pack is not found")

    # Searching admissible moves for the pawn
    def get_admissible_moves(self) -> list:
        # Create a list of admissible moves for the pawn
        admissible_moves = []

        # Check the new position
        new_pos = (self.position[0] - self.team.value, self.position[1])
        if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos):
            admissible_moves.append(new_pos)

        if self.is_crossed_river() is True:
            new_pos = (self.position[0], self.position[1] + 1)
            if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos):
                admissible_moves.append(new_pos)

            new_pos = (self.position[0], self.position[1] - 1)
            if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos):
                admissible_moves.append(new_pos)

        return admissible_moves


class Horse(Piece):
    """Class representing the horse piece"""

    _piece_value = 40
    _piece_type = "horse"

    def piece_value(self, value_pack: int = 0) -> float:
        # Default value pack
        if value_pack == 0:
            return self._piece_value

        # Value pack 1
        elif value_pack == 1:
            change = 0
            # Receive bonus or penalty based on the number of admissible moves it has
            if len(self.admissible_moves) == 0 or len(self.admissible_moves) == 1:
                change += -10
            elif len(self.admissible_moves) == 2:
                change += -5
            elif len(self.admissible_moves) == 5 or len(self.admissible_moves) == 6:
                change += 5
            elif len(self.admissible_moves) == 7 or len(self.admissible_moves) == 8:
                change += 10
            if self.team is Team.BLACK and self.position == (1, 4):
                change += -25
            elif self.team is Team.RED and self.position == (8, 4):
                change += -25
            return self._piece_value + change

        # Value pack 2
        elif value_pack == 2:
            change = 0
            # Receive a bonus or penalty based on the number of admissible moves it has
            if len(self.admissible_moves) == 0 or len(self.admissible_moves) == 1:
                change += -5
            elif len(self.admissible_moves) == 2:
                change += -2.5
            elif len(self.admissible_moves) == 5 or len(self.admissible_moves) == 6:
                change += 2.5
            elif len(self.admissible_moves) == 7 or len(self.admissible_moves) == 8:
                change += 5

            # Receive a bonus or penalty base on the state of the game
            change += (22 - self.number_of_pieces) * 0.75

            palace_pos = None
            if self.team is Team.RED:
                palace_pos = (1, 4)
            else:
                palace_pos = (8, 4)
            change += ((32 - self.number_of_pieces) * 0.15 *
                       (5 - (abs(palace_pos[0] - self.position[0]) + abs(palace_pos[1] - self.position[1]))))

            return self._piece_value + change

        # If the value pack is not found
        else:
            raise ValueError("Value pack is not found")

    def get_admissible_moves(self) -> list:
        # Create a list of admissible moves for the horse
        admissible_moves = []

        # Possible goal positions
        x_orient = [2, 2, 1, -1, -2, -2, -1, 1]
        y_orient = [1, -1, -2, -2, -1, 1, 2, 2]
        maximum_move_count = 8

        # Possible directions
        p_orient = [1, 0, -1, 0]
        q_orient = [0, -1, 0, 1]

        for cnt in range(maximum_move_count):
            # Middle position
            pos = (
                self.position[0] + p_orient[cnt // 2],
                self.position[1] + q_orient[cnt // 2],
            )

            # Check if the horse is not block
            if self.is_position_on_board(pos) and self.is_position_free(pos):
                # Goal position
                pos = (
                    self.position[0] + x_orient[cnt],
                    self.position[1] + y_orient[cnt],
                )

                # Check the goal position
                if self.is_position_on_board(pos) and not self.is_position_teammate(pos):
                    admissible_moves.append(pos)

        return admissible_moves
