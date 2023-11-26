# Made by: Veil
import time
import numpy as np
from cmath import inf
from random import randint, shuffle
from piece import General, Advisor, Elephant, Rook, Cannon, Horse, Pawn, Piece
from team import Team


class GameState:
    """This class respresents the state of game containing
    information and transforming method"""

    # [BEGIN CONSTANTS]
    # Board size
    BOARD_SIZE_X = 10
    BOARD_SIZE_Y = 9

    # Palace bound
    BOUND_PALACE_X_RED = tuple((7, 9))
    BOUND_PALACE_X_BLACK = tuple((0, 2))
    BOUND_PALACE_Y = tuple((3, 5))

    # [BEGIN INITILIZATION]
    def __init__(
        self,
        board: np.ndarray,
        current_team: Team,
    ) -> None:
        # Add the chess pieces to the list
        self.board = board

        # Declare read-only properties
        self._value = None
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

        if self.get_team_win is Team.RED:
            return inf

        if self.get_team_win is Team.BLACK:
            return -inf

        current_value = 0
        # Iterate through all position in the board
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                # Get the notation of the position
                notation = self.board[i][j]
                # If the notation is empty, then there is no piece at that position -> skip
                if notation == "":
                    continue

                # Otherwise, create a instance of the piece and take value of the piece
                piece = Piece.create_instance((i, j), notation)
                current_value += piece.piece_value * piece.team.value

        return current_value

    def _get_the_opponent_team(self):
        """This method will return the opponent team in this game state"""
        if self._current_team is Team.BLACK:
            return Team.RED
        else:
            return Team.BLACK

    def generate_game_state_with_move(self, old_pos: tuple, new_pos: tuple):
        """This method creates a game state with a move
        (return None if the game state is invalid)"""
        # Temporary move the piece
        old_pos_notation = self.board[old_pos[0]][old_pos[1]]
        new_pos_notation = self.board[new_pos[0]][new_pos[1]]

        self.board[old_pos[0]][old_pos[1]] = ""
        self.board[new_pos[0]][new_pos[1]] = old_pos_notation

        # Get the opponent team
        opponent = self._get_the_opponent_team()

        # Check if the game state is valid
        def _is_board_valid(board: np.ndarray) -> bool:
            """This method True if the board is valid, vice versa"""

            # Find the position of the current team's General
            cur_general_pos = None

            for y in range(self.BOUND_PALACE_Y[0], self.BOUND_PALACE_Y[1] + 1):
                # Find place bound of current team
                bound_x = None
                if self._current_team is Team.RED:
                    bound_x = self.BOUND_PALACE_X_RED
                elif self._current_team is Team.BLACK:
                    bound_x = self.BOUND_PALACE_X_BLACK

                # Find the general
                for x in range(bound_x[0], bound_x[1] + 1):
                    if board[x][y] == "":
                        continue
                    if board[x][y][1] == "G":
                        cur_general_pos = (x, y)

            # Check if the general is exposed
            x_str_dir, y_str_dir = [0, 0, -1, 1], [1, -1, 0, 0]

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
                    # If check position is out of the board then break
                    if Piece.is_position_on_board(check_pos) is False:
                        break

                    notation = board[check_pos[0]][check_pos[1]]
                    # If check position is empty then skip
                    if notation == "":
                        continue
                    # If check position is our team then break
                    elif Team[notation[0]] is self._current_team:
                        break
                    # If check position is oponent Rook then return False
                    elif notation[1] == "R":
                        return False

            # .Check the horse
            for index in range(8):
                check_pos = (
                    cur_general_pos[0] + x_horse_offset[index],
                    cur_general_pos[1] + y_horse_offset[index],
                )
                # If check position is out of the board then break
                if Piece.is_position_on_board(check_pos) is False:
                    break

                notation = board[check_pos[0]][check_pos[1]]
                # If check position is empty then skip
                if notation == "":
                    continue
                # If the check_position is the opponent horse
                if Team[notation[0]] is opponent and notation[1] == "H":
                    mid_pos = (
                        cur_general_pos[0] + x_orient[index // 2],
                        cur_general_pos[1] + y_orient[index // 2],
                    )
                    mid_pos_notation = board[mid_pos[0]][mid_pos[1]]
                    if mid_pos_notation == "":
                        return False

            # .Check the cannon
            for direction in range(4):
                piece_behind = 0
                for steps in range(1, 10):
                    pos = (
                        cur_general_pos[0] + steps * x_str_dir[direction],
                        cur_general_pos[1] + steps * y_str_dir[direction],
                    )
                    # If check position is out of the board then break
                    if Piece.is_position_on_board(pos) is False:
                        break
                                    
                                    
                    notation = board[pos[0]][pos[1]]
                    # If check position is empty then skip
                    if notation == "":
                        continue
                    # If there is 1 piece behind and the pos is oponent cannon, return False
                    if (
                        piece_behind == 1
                        and Team[notation[0]] is opponent
                        and notation[1] == "C"
                    ):
                        return False
                    # If the there is a piece then add 1 to piece_behind
                    if notation != "":
                        piece_behind += 1
                    # If piece_behind is greater than 1, break
                    if piece_behind > 1:
                        break

            # .Check the pawn
            # Check left, right
            for index in range(2):
                check_pos = (
                    cur_general_pos[0] + x_str_dir[index],
                    cur_general_pos[1] + y_str_dir[index],
                )
                notation = board[check_pos[0]][check_pos[1]]
                # If check position is empty then skip
                if notation == "":
                    continue
                # If the piece is the opponent piece then return False
                if Team[notation[0]] is opponent and notation[1] == "P":
                    return False
            # Check forward
            forward_notation = board[cur_general_pos[0] + opponent.value][cur_general_pos[1]]
            if (
                forward_notation != ""
                and Team[forward_notation[0]] is opponent
                and forward_notation[1] == "P"
            ):
                return False

            # .Check the general
            for steps in range(1, 10):
                pos = (cur_general_pos[0] + steps * opponent.value, cur_general_pos[1])
                # If check position is out of the board then break
                if Piece.is_position_on_board(pos) is False:
                    break

                notation = board[pos[0]][pos[1]]
                # If the there is no piece in the position, then skip
                if notation == "":
                    continue
                # If the piece is opponent's general then return False
                elif notation[1] == "G":
                    return False
                # If the piece is other piece then break
                else:
                    break

        # Conclude
        def _return_to_old_state():
            self.board[old_pos[0]][old_pos[1]] = old_pos_notation
            self.board[new_pos[0]][new_pos[1]] = new_pos_notation

        # .If the check is not passed, then return None
        if _is_board_valid(self.board) is False:
            _return_to_old_state()
            return None

        # Create a copy of moved board and return the board to the old state
        new_board = self.board.copy()
        _return_to_old_state()

        # Return the game state which has the new information
        return GameState(new_board, opponent), (old_pos, new_pos)

    def generate_random_game_state(self):
        """This method will generate another gamestate that can be tranformed
        by current method using each move of the piece"""
        # Get all position of curretn team's piece into a list and randomly shuffle it
        team_positions = list()
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                notation = self.board[i][j]

                if notation == "":
                    continue

                if Team[notation[0]] is self._current_team:
                    team_positions.append((i, j))

        shuffle(team_positions)

        # Iterate through every piece in the list, generate the piece's move list and shuffle it
        for pos in team_positions:
            moves_list = Piece.create_instance(pos, notation).get_admissible_moves(
                self.board
            )
            shuffle(moves_list)

            for new_pos in moves_list:
                new_gamestate = self.generate_game_state_with_move(pos, new_pos)
                if new_gamestate is not None:
                    return new_gamestate

        # If the gamestate is terminal then return None
        return None

    def generate_all_game_states(self):
        """This method will return the list of all states that can be accessed
        from the current state by a single move"""

        # Create a list that keeps track of all game states that can be generated.
        game_states_available = list()

        # Iterating through all moves
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                notation = self.board[i][j]

                if notation == "":
                    continue

                if Team[notation[0]] is self._current_team:
                    moves_list = Piece.create_instance(
                        (i, j), notation
                    ).get_admissible_moves(self.board)

                    for new_pos in moves_list:
                        game_state = self.generate_game_state_with_move((i, j), new_pos)

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
                black_piece = Chariot((0, columns), Team.BLACK)

            # Create black horses
            elif columns == 1 or columns == 7:
                black_piece = Horse((0, columns), Team.BLACK)

            # Create black elephants
            elif columns == 2 or columns == 6:
                black_piece = Elephant((0, columns), Team.BLACK)

            # Create black advisors
            elif columns == 3 or columns == 5:
                black_piece = Advisor((0, columns), Team.BLACK)

            # Create black general
            else:
                black_piece = General((0, columns), Team.BLACK)

            # Put the pieces created into chess_pieces list
            pieces_list_black.append(black_piece)

            # Assign team of the pieces to its position
            board[0][columns] = Team.BLACK

        # Create black cannons
        for columns in range(1, 8, 6):
            black_cannon = Cannon((2, columns), Team.BLACK)

            # Put the pieces created into chess_pieces list
            pieces_list_black.append(black_cannon)

            # Assign team of the pieces to its position
            board[2][columns] = Team.BLACK

        # Create black pawns
        for columns in range(0, GameState.BOARD_SIZE_Y, 2):
            black_pawn = Pawn((3, columns), Team.BLACK)

            # Put the pieces created into chess_pieces list
            pieces_list_black.append(black_pawn)

            # Assign team of the pieces to its position
            board[3][columns] = Team.BLACK

        # Create pieces in the last row of red team
        for columns in range(GameState.BOARD_SIZE_Y):
            # Create red chariots
            if columns == 0 or columns == 8:
                red_piece = Chariot((9, columns), Team.RED)

            # Create red horses
            elif columns == 1 or columns == 7:
                red_piece = Horse((9, columns), Team.RED)

            # Create red elephants
            elif columns == 2 or columns == 6:
                red_piece = Elephant((9, columns), Team.RED)

            # Create red advisors
            elif columns == 3 or columns == 5:
                red_piece = Advisor((9, columns), Team.RED)

            # Create red general
            else:
                red_piece = General((9, columns), Team.RED)

            # Put the pieces created into chess_pieces list
            pieces_list_red.append(red_piece)

            # Assign team of the pieces to its position
            board[9][columns] = Team.RED

        # Create red cannons
        for columns in range(1, 8, 6):
            red_cannon = Cannon((7, columns), Team.RED)

            # Put the pieces created into chess_pieces list
            pieces_list_red.append(red_cannon)

            # Assign team of the pieces to its position
            board[7][columns] = Team.RED

        # Create red pawns
        for columns in range(0, GameState.BOARD_SIZE_Y, 2):
            red_pawn = Pawn((6, columns), Team.RED)

            # Put the pieces created into chess_pieces list
            pieces_list_red.append(red_pawn)

            # Assign team of the pieces to its position
            board[6][columns] = Team.RED

        # Change type of board into tuple
        board = tuple(map(tuple, board))

        # Set all admissible moves of the red pieces
        for piece in pieces_list_red:
            piece.set_admissible_moves(board)

        # return the initial board
        return GameState(pieces_list_red, pieces_list_black, board, Team.RED)

    # [END METHOD]


if __name__ == '__main__':
    queue = [GameState.generate_initial_game_state()]
    for depth in range(1, 4):
        start = time.time()

        new_queue = list()
        for game_state_ in queue:
            for state, move_ in game_state_.all_child_gamestates:
                new_queue.append(state)

        queue = new_queue
        end = time.time()
        print(depth, len(queue), end - start)
