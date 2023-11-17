# Made by: Veil
from cmath import inf
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
        self._board = board
        self._current_team = current_team
        self._all_child_gamestates = None

    # Properties initialization
    # .value
    @property
    def value(self) -> float:
        """This is the Getter function of the value property,
        return the value of the game state using chess pieces value"""

        if self._value is None:
            self._value = self._get_game_state_value()

        return self._value

    # .all_child_gamestates
    @property
    def all_child_gamestates(self) -> list:
        """This is the Getter function of the list of child game states"""

        if self._all_child_gamestates is None:
            self._all_child_gamestates = self.generate_all_game_states()

        return self._all_child_gamestates
    # [END INITILIZATION]

    # [BEGIN METHOD]
    # Instance method
    def _get_game_state_value(self):
        """Return the evaluation value of the board"""

        current_value = 0

        if self.get_team_win is Team.RED:
            return inf

        if self.get_team_win is Team.BLACK:
            return -inf

        for piece in self.pieces_list_black:
            current_value = current_value - piece.piece_value

        for piece in self.pieces_list_red:
            current_value = current_value + piece.piece_value

        return current_value

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

    def generate_game_state_with_move(self, old_pos, new_pos):
        """This method creates a game state with a move
        (return None if the game state is invalid)"""
        # Create a copy of current board and transform it
        new_board = self._create_a_new_board(old_pos, new_pos)

        # Get the opponent team
        opponent = self._get_the_opponent_team()

        # Create new chess piece list and current team's general position
        new_pieces_list_red, new_pieces_list_black = list(), list()
        current_team_general_position = None

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

            # If the piece is current team general, get the position
            if new_piece.team is self._current_team and isinstance(new_piece, General):
                current_team_general_position = new_piece.position

            # Append new piece to the list
            if new_piece.team is Team.RED:
                new_pieces_list_red.append(new_piece)
            else:
                new_pieces_list_black.append(new_piece)

        # Check if the game state is valid
        # Get the new opponent pieces list
        new_opponent_pieces_list = None
        if opponent is Team.RED:
            new_opponent_pieces_list = new_pieces_list_red
        else:
            new_opponent_pieces_list = new_pieces_list_black

        # Iterate for each piece in the list and detect the invalid
        for piece in new_opponent_pieces_list:
            # If the piece is advisor or elephant, then skip
            if isinstance(piece, Advisor) or isinstance(piece, Elephant):
                continue

            # If the piece is general, check the y position
            if (
                isinstance(piece, General)
                and piece.position[1] == current_team_general_position[1]
            ):
                x_min = piece.position[0] - opponent.value
                x_max = current_team_general_position[0] - \
                    self._current_team.value
                if x_min > x_max:
                    x_min, x_max = x_max, x_min

                has_obstacle = False
                for x in range(x_min, x_max + 1):
                    if new_board[x][piece.position[1]] is not Team.NONE:
                        has_obstacle = True
                        break

                if has_obstacle is False:
                    return None
                continue

            # Else: Check if admissible moves of the piece containing the general position
            if current_team_general_position in piece.admissible_moves:
                return None

        # Return the game state which has the new information
        return GameState(
            new_pieces_list_red, new_pieces_list_black, new_board, opponent
        ), (
            old_pos, new_pos
        )

    def generate_random_game_state(self):
        """This method will generate another gamestate that can be tranformed
        by current method using each move of the piece"""

        # Return a random child game states of the current game states
        return self.all_child_gamestates[randint(0, len(self.all_child_gamestates) - 1)]

    def generate_all_game_states(self):
        """This method will return the list of all states that can be accessed
        from the current state by a single move"""

        # Create a list that keeps track of all game states that can be generated.
        game_states_available = []
        pieces_list = self._get_the_current_team_pieces_list()

        # Iterating through all moves
        for pieces in pieces_list:
            for move in pieces.admissible_moves:
                # Get the old position and new position of the chosen piece
                old_pos = pieces.position
                new_pos = move

                # Add new game state into the above list
                game_state = self.generate_game_state_with_move(old_pos, new_pos)

                if game_state is not None:
                    game_states_available.append(game_state)

        return game_states_available

    def get_team_win(self):
        """This method return the winning team"""

        # If the current game state has child game states, then return Team.NONE
        if len(self.all_child_gamestates) > 0:
            return Team.NONE

        # Return the opponent if current team has no admissible move
        return self._get_the_opponent_team()

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

if __name__ == '__main__':
    queue = [GameState.generate_initial_game_state()]
    for depth in range(1, 3):
        new_queue = list()
        for game_state in queue:
            for state, move in game_state.all_child_gamestates:
                new_queue.append(state)

        queue = new_queue
        print(depth, len(queue))