# Made by: Veil
from copy import deepcopy
from random import randint
from piece import Piece
from general import General
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
        """This is method will return a new board with a move has been invoked"""
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

    def generate_random_game_state(self, policy):
        """This method will generate another gamestate that can be tranformed
        by current method using each move of the piece"""

        # Get a random move and a random piece
        rand_piece_index = randint(0, len(self.chess_pieces) - 1)
        rand_move_index = randint(
            0, len(self.chess_pieces[rand_piece_index].admissible_moves)
        )

        # Get the old position and new position of the chosen piece
        old_pos = self.chess_pieces[rand_piece_index].position
        new_pos = self.chess_pieces[rand_piece_index].admissible_moves[rand_move_index]

        # Create a copy of current board and transform it
        new_board = self._create_a_new_board(old_pos, new_pos)

        # Get the opponent team
        opponent = self._get_the_opponent_team()

        # Create new chess piece list
        new_chess_pieces = []
        for piece in self.chess_pieces:
            # If the piece is on the new position of the chosen one, then remove it
            if piece.position == new_pos:
                continue

            # Create a copy of the current piece, and initialize it
            new_piece = deepcopy(piece)

            new_piece.set_board(new_board)  # Update board
            if piece.position == old_pos:  # Update position
                new_piece.position = new_pos
            if piece.team is self._current_team:  # Update admissible_moves
                new_piece.admissible_moves = new_piece.get_admissible_moves()

            new_chess_pieces.append(new_piece)

        # Return the game state which has the new information
        return GameState(new_chess_pieces, new_board, opponent)

    def _remove_checked_move(self):
        """This method will remove all the move which lead the current team be checked"""
        # Get the opponent team
        opponent = self._get_the_opponent_team()

        # Find the current team general position
        general_position = None
        for piece in self.chess_pieces:
            if piece.team is self._current_team and isinstance(piece, General):
                general_position = piece
                break

        # This method will return False if the move made the current team be checked
        def check_checkmate(board, general_position):
            for piece in self.chess_pieces:
                # If the piece is current team piece, then skip
                if piece.team is self._current_team:
                    continue

                # Made the copy of the piece, add the board
                # and get the new admissible moves of that piece
                piece_clone = deepcopy(piece)
                piece_clone.set_board(board)
                piece_clone.admissible_moves = piece_clone.get_admissible_moves()

                # Check if admissible moves of the piece containing the general position
                if general_position in piece.admissible_moves:
                    return False
            return True

        # Iterate through all the moves
        for piece in self.chess_pieces:
            # If the piece is opponent piece, then skip
            if piece.team is opponent:
                continue

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

    # [END METHOD]
