# Made by: Veil
from copy import deepcopy
from random import randint
from general import General
from advisor import Advisor
from elephant import Elephant
from chariot import Chariot
from cannon import Cannon
from horse import Horse
from pawn import Pawn
from team import Team


class GameState:
    """This class respresents the state of game containing
    information and transforming method"""

    # [BEGIN CONSTANTS]
    # Board size
    BOARD_SIZE_X = 10
    BOARD_SIZE_Y = 9

    # [BEGIN INITILIZATION]
    def __init__(
        self,
        pieces_list_red: list,
        pieces_list_black: list,
        board: tuple,
        current_team: Team,
    ) -> None:
        # Add the chess pieces to the list
        self.pieces_list_red = pieces_list_red
        self.pieces_list_black = pieces_list_black

        # Declare read-only properties
        self._value = None
        self._checked_team = Team.NONE
        self._win_status = None
        self._board = board
        self._current_team = current_team

        # Remove the checked move
        self._remove_checked_move()

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

    def _create_a_new_board(self, old_pos, new_pos):
        """This method returns a new board after a piece moved"""
        # Create a deepcopy of a new board
        new_board = deepcopy(self._board)

        # Transform the new board to list
        new_board = list(map(list, new_board))

        # Assign new value to the old position and new position of the moved piece
        new_board[old_pos[0]][old_pos[1]] = Team.NONE
        new_board[new_pos[0]][new_pos[1]] = self._current_team

        # Transform the new board to tuple again
        new_board = tuple(map(tuple, new_board))

        # Return the answer
        return new_board

    def _get_the_current_team_pieces_list(self):
        """This method will return the chess pieces list of the current team"""
        if self._current_team is Team.RED:
            return self.pieces_list_red
        else:
            return self.pieces_list_black

    def _get_the_opponent_pieces_list(self):
        """This method will return the chess pieces list of the opponent"""
        if self._current_team is Team.RED:
            return self.pieces_list_black
        else:
            return self.pieces_list_red

    def generate_random_game_state(self, policy):
        """This method will generate another gamestate that can be tranformed
        by current method using each move of the piece"""

        # Get the current team chess chess pieces list
        pieces_list = self._get_the_current_team_pieces_list()

        # Get a random move and a random piece
        rand_piece_index = randint(0, len(pieces_list) - 1)
        while len(pieces_list[rand_piece_index].admissible_moves) == 0:
            rand_piece_index = randint(0, len(pieces_list) - 1)

        rand_move_index = randint(0, len(pieces_list[rand_piece_index].admissible_moves) - 1)

        # Get the old position and new position of the chosen piece
        old_pos = pieces_list[rand_piece_index].position
        new_pos = pieces_list[rand_piece_index].admissible_moves[rand_move_index]

        # Create a copy of current board and transform it
        new_board = self._create_a_new_board(old_pos, new_pos)

        # Get the opponent team
        opponent = self._get_the_opponent_team()

        # Create new chess piece list
        new_pieces_list_red, new_pieces_list_black = list(), list()

        for piece in self.pieces_list_red + self.pieces_list_black:
            # If the piece is on the new position of the chosen one, then remove it
            if piece.position == new_pos:
                continue

            # Create a copy of the current piece, and initialize it
            new_piece = deepcopy(piece)

            new_piece.set_board(new_board)  # Update board
            if piece.position == old_pos:  # Update position
                new_piece.position = new_pos
            if piece.team is opponent:  # Update admissible_moves
                new_piece.set_admissible_moves()

            # Append new piece to the list
            if new_piece.team is Team.RED:
                new_pieces_list_red.append(new_piece)
            else:
                new_pieces_list_black.append(new_piece)

        # Return the game state which has the new information
        return GameState(new_pieces_list_red, new_pieces_list_black, new_board, opponent)

    def _remove_checked_move(self):
        """This method removes all moves that lead to the current team be checked"""
        # Get the opponent team
        opponent = self._get_the_opponent_team()

        # Get the piece list
        pieces_list_current_team = self._get_the_current_team_pieces_list()
        pieces_list_opponent = self._get_the_opponent_pieces_list()

        # Find the current team general position
        general_position = None
        for piece in pieces_list_current_team:
            if isinstance(piece, General):
                general_position = piece.position
                break

        # This method will return False if the move made the current team be checked
        def check_checkmate(board, general_position):
            for piece in pieces_list_opponent:
                # If the piece is advisor or elephant, then skip
                if isinstance(piece, Advisor) or isinstance(piece, Elephant):
                    continue

                # If the piece is general, check the y position
                if (
                    isinstance(piece, General)
                    and piece.position[1] == general_position[1]
                ):
                    x_min = piece.position[0] - opponent.value
                    x_max = general_position[0] - self._current_team.value
                    if x_min > x_max:
                        x_min, x_max = x_max, x_min

                    has_obstacle = False
                    for x in range(x_min, x_max + 1):
                        if board[x][general_position[1]] is not Team.NONE:
                            has_obstacle = True
                            break

                    if has_obstacle is False:
                        return False

                    continue

                # Made the copy of the piece, add the board
                # and get the new admissible moves of that piece
                piece_clone = deepcopy(piece)
                piece_clone.set_board(board)
                piece_clone.set_admissible_moves()

                # Check if admissible moves of the piece containing the general position
                if general_position in piece_clone.admissible_moves:
                    return False
            return True

        # Iterate through all the moves
        for piece in pieces_list_current_team:
            # Assign current position of the piece
            old_pos = piece.position

            # Iterate over admissible position of the piece
            new_admisible_moves = list()  # Create the new admissible moves list
            for new_pos in piece.admissible_moves:
                # Creating a new board by using the move
                new_board = self._create_a_new_board(old_pos, new_pos)

                # Check if the move made the current team be checked
                if (
                    isinstance(piece, General) and check_checkmate(new_board, new_pos)
                ) or (
                    not isinstance(piece, General)
                    and check_checkmate(new_board, general_position)
                ):
                    new_admisible_moves.append(new_pos)

            # Assign filtered adssible moves list
            piece.admissible_moves = new_admisible_moves

    # Class method
    @classmethod
    def generate_initial_game_state(cls):
        """This method creates the initial board"""

        # Create a list of chess pieces
        pieces_list_red, pieces_list_black = list(), list()

        # Create a list to keep track of the team of pieces in chess_pieces
        board = [
            [Team.NONE for columns in range(GameState.BOARD_SIZE_Y)]
            for rows in range(GameState.BOARD_SIZE_X)
        ]

        # Create pieces in the first row of black team
        for columns in range(GameState.BOARD_SIZE_Y):
            # Create black chariots
            if columns == 0 or columns == 8:
                black_piece = Chariot((0, columns), Team.BLACK, board)

            # Create black horses
            elif columns == 1 or columns == 7:
                black_piece = Horse((0, columns), Team.BLACK, board)

            # Create black elephants
            elif columns == 2 or columns == 6:
                black_piece = Elephant((0, columns), Team.BLACK, board)

            # Create black advisors
            elif columns == 3 or columns == 5:
                black_piece = Advisor((0, columns), Team.BLACK, board)

            # Create black general
            else:
                black_piece = General((0, columns), Team.BLACK, board)

            # Put the pieces created into chess_pieces list
            pieces_list_black.append(black_piece)

            # Assign team of the pieces to its position
            board[0][columns] = Team.BLACK

        # Create black cannons
        for columns in range(1, 8, 6):
            black_cannon = Cannon((2, columns), Team.BLACK, board)

            # Put the pieces created into chess_pieces list
            pieces_list_black.append(black_cannon)

            # Assign team of the pieces to its position
            board[2][columns] = Team.BLACK

        # Create black pawns
        for columns in range(0, GameState.BOARD_SIZE_Y, 2):
            black_pawn = Pawn((3, columns), Team.BLACK, board)

            # Put the pieces created into chess_pieces list
            pieces_list_black.append(black_pawn)

            # Assign team of the pieces to its position
            board[3][columns] = Team.BLACK

        # Create pieces in the last row of red team
        for columns in range(GameState.BOARD_SIZE_Y):
            # Create red chariots
            if columns == 0 or columns == 8:
                red_piece = Chariot((9, columns), Team.RED, board)

            # Create red horses
            elif columns == 1 or columns == 7:
                red_piece = Horse((9, columns), Team.RED, board)

            # Create red elephants
            elif columns == 2 or columns == 6:
                red_piece = Elephant((9, columns), Team.RED, board)

            # Create red advisors
            elif columns == 3 or columns == 5:
                red_piece = Advisor((9, columns), Team.RED, board)

            # Create red general
            else:
                red_piece = General((9, columns), Team.RED, board)

            # Put the pieces created into chess_pieces list
            pieces_list_red.append(red_piece)

            # Assign team of the pieces to its position
            board[9][columns] = Team.RED

        # Create red cannons
        for columns in range(1, 8, 6):
            red_cannon = Cannon((7, columns), Team.RED, board)

            # Put the pieces created into chess_pieces list
            pieces_list_red.append(red_cannon)

            # Assign team of the pieces to its position
            board[7][columns] = Team.RED

        # Create red pawns
        for columns in range(0, GameState.BOARD_SIZE_Y, 2):
            red_pawn = Pawn((6, columns), Team.RED, board)

            # Put the pieces created into chess_pieces list
            pieces_list_red.append(red_pawn)

            # Assign team of the pieces to its position
            board[6][columns] = Team.RED

        # Change type of board into tuple
        board = tuple(map(tuple, board))

        # Set all admissible moves of the red pieces
        for piece in pieces_list_red:
            piece.set_admissible_moves()

        # return the initial board
        return GameState(pieces_list_red, pieces_list_black, board, Team.RED)

    # [END METHOD]
