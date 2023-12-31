# Made by: Veil
"""Module providing the property of game state"""
from cmath import inf
from random import shuffle
from piece import General, Piece
from team import Team


class GameState:
    """This class respresents the state of game containing
    information and transforming method"""

    # [BEGIN CONSTANTS]
    # Board size
    BOARD_SIZE_X = 10
    BOARD_SIZE_Y = 9
    # Limit for repeated moves
    MAX_PERPETUAL = 3

    # [BEGIN INITILIZATION]
    def __init__(
        self,
        board: list,
        current_team: Team,
        move_history: dict,
        value_pack: int = 0,
        number_of_red_pieces: int = 16,
        number_of_black_pieces: int = 16,
    ) -> None:
        self.board = board
        self.move_history = move_history
        self.number_of_red_pieces = number_of_red_pieces
        self.number_of_black_pieces = number_of_black_pieces

        self._value_pack = value_pack
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
    def _get_game_state_value(self) -> float:
        """Return the evaluation value of the board"""
        # Return the value of a game state when a team wins
        if self.get_team_win() is Team.RED:
            return inf

        if self.get_team_win() is Team.BLACK:
            return -inf

        current_value = 0
        # Iterate through all the positions on the board
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                # Get the notation of the position
                notation = self.board[i][j]
                # If the notation is empty, then skip
                if notation == "NN":
                    continue

                # Otherwise, create an instance of the piece and take value of that piece
                piece = Piece.create_instance(
                    (i, j),
                    notation,
                    self.board,
                    self.number_of_black_pieces + self.number_of_red_pieces,
                    self._get_number_of_team_pieces(Team[notation[0]]),
                )
                current_value += piece.piece_value(self._value_pack) * piece.team.value

        return current_value

    def _get_the_opponent_team(self) -> Team:
        """This method returns the opponent's team in the game state"""
        if self._current_team is Team.BLACK:
            return Team.RED
        else:
            return Team.BLACK

    def _get_number_of_team_pieces(self, team) -> int:
        """This method returns the number of pieces of a team"""
        if team is Team.BLACK:
            return self.number_of_black_pieces
        else:
            return self.number_of_red_pieces

    def generate_game_state_with_move(self, old_pos: tuple, new_pos: tuple):
        """This method creates a game state with a move
        (return None if the game state is invalid)"""
        # Temporary move the piece
        old_pos_notation = self.board[old_pos[0]][old_pos[1]]
        new_pos_notation = self.board[new_pos[0]][new_pos[1]]

        self.board[old_pos[0]][old_pos[1]] = "NN"
        self.board[new_pos[0]][new_pos[1]] = old_pos_notation

        # Get the opponent team
        opponent = self._get_the_opponent_team()

        # Check if the game state is valid
        def _return_to_old_state():
            self.board[old_pos[0]][old_pos[1]] = old_pos_notation
            self.board[new_pos[0]][new_pos[1]] = new_pos_notation

        # .Check for perpetual moves
        hash_code = self.hash_board(self.board)
        if self.move_history.get(hash_code, 0) + 1 == self.MAX_PERPETUAL:
            _return_to_old_state()
            return None

        # .If the check is not passed, then return None
        if General.is_general_exposed(self.board, self._current_team, opponent) is True:
            _return_to_old_state()
            return None

        # Create a copy of the moved board and return the board to the old state
        new_board = list(map(list, self.board))
        new_move_history = dict(self.move_history)
        new_move_history[hash_code] = new_move_history.get(hash_code, 0) + 1
        _return_to_old_state()

        # Calculate the number of pieces of the gamestate
        new_number_of_red_pieces = self.number_of_red_pieces
        new_number_of_black_pieces = self.number_of_black_pieces
        if self.board[new_pos[0]][new_pos[1]] != "NN":
            if self._current_team is Team.RED:
                new_number_of_black_pieces -= 1
            else:
                new_number_of_red_pieces -= 1

        return GameState(
            new_board,
            opponent,
            new_move_history,
            self._value_pack,
            new_number_of_red_pieces,
            new_number_of_black_pieces,
        ), (old_pos, new_pos)

    def generate_random_game_state(self):
        """This method generates another gamestate that can be tranformed
        by the current method using each move of the piece"""
        # Put all positions of the current team's pieces into a list and shuffle it
        team_positions = list()
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                notation = self.board[i][j]

                if Team[notation[0]] is self._current_team:
                    team_positions.append((i, j))

        shuffle(team_positions)

        # Iterate through every pieces in the list, generate the piece's move list and shuffle it
        for pos in team_positions:
            notation = self.board[pos[0]][pos[1]]
            moves_list = Piece.create_instance(
                pos,
                notation,
                self.board,
                self.number_of_black_pieces + self.number_of_red_pieces,
                self._get_number_of_team_pieces(Team[notation[0]]),
            ).admissible_moves
            shuffle(moves_list)

            for new_pos in moves_list:
                new_gamestate = self.generate_game_state_with_move(pos, new_pos)
                if new_gamestate is not None:
                    return new_gamestate

        # If the gamestate is terminal then return None
        return None

    def generate_all_game_states(self) -> list:
        """This method returns the list of all states that can be accessed
        from the current state by a single move"""

        # Create a list that keeps track of all game states that can be generated.
        game_states_available = list()

        # Iterate through all moves
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                notation = self.board[i][j]

                # If the position is empty, then skip
                if notation == "NN":
                    continue

                # If the current team's piece is on that position,
                # then create an instance and get its admissible moves list
                if Team[notation[0]] is self._current_team:
                    moves_list = Piece.create_instance(
                        (i, j),
                        notation,
                        self.board,
                        self.number_of_black_pieces + self.number_of_red_pieces,
                        self._get_number_of_team_pieces(Team[notation[0]]),
                    ).admissible_moves

                    # Iterate all moves in the moves list
                    for new_pos in moves_list:
                        # Create a new game state with that move
                        game_state = self.generate_game_state_with_move((i, j), new_pos)

                        # If the new game state is valid then add it to the list at the beginning
                        if game_state is not None:
                            game_states_available.append(game_state)

        return game_states_available

    def get_team_win(self):
        """This method returns the winning team"""

        # If the current game state has child game states, then return Team.NONE
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                notation = self.board[i][j]
                if notation == "NN":
                    continue

                if Team[notation[0]] is self._current_team:
                    moves_list = Piece.create_instance(
                        (i, j),
                        notation,
                        self.board,
                        self.number_of_black_pieces + self.number_of_red_pieces,
                        self._get_number_of_team_pieces(Team[notation[0]]),
                    ).admissible_moves

                    old_pos = (i, j)
                    for new_pos in moves_list:
                        old_pos_notation = self.board[old_pos[0]][old_pos[1]]
                        new_pos_notation = self.board[new_pos[0]][new_pos[1]]

                        self.board[old_pos[0]][old_pos[1]] = "NN"
                        self.board[new_pos[0]][new_pos[1]] = old_pos_notation

                        if (
                            General.is_general_exposed(
                                self.board,
                                self._current_team,
                                self._get_the_opponent_team(),
                            )
                            is False
                        ):
                            self.board[old_pos[0]][old_pos[1]] = old_pos_notation
                            self.board[new_pos[0]][new_pos[1]] = new_pos_notation
                            return Team.NONE

                        self.board[old_pos[0]][old_pos[1]] = old_pos_notation
                        self.board[new_pos[0]][new_pos[1]] = new_pos_notation

        # Return the opponent's team if the current team has no admissible moves
        return self._get_the_opponent_team()

    # Static method
    @staticmethod
    def hash_board(board):
        """This method returns the hash code of a board"""
        return hash(tuple(map(tuple, board)))

    # Class method
    @classmethod
    def generate_initial_game_state(cls, value_pack: int = 0):
        """This method creates the initial board"""
        initial_board = list(
            [
                ["BR", "BH", "BE", "BA", "BG", "BA", "BE", "BH", "BR"],
                ["NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN"],
                ["NN", "BC", "NN", "NN", "NN", "NN", "NN", "BC", "NN"],
                ["BP", "NN", "BP", "NN", "BP", "NN", "BP", "NN", "BP"],
                ["NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN"],
                ["NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN"],
                ["RP", "NN", "RP", "NN", "RP", "NN", "RP", "NN", "RP"],
                ["NN", "RC", "NN", "NN", "NN", "NN", "NN", "RC", "NN"],
                ["NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN", "NN"],
                ["RR", "RH", "RE", "RA", "RG", "RA", "RE", "RH", "RR"],
            ]
        )
        initial_move_history = dict()
        hash_code = GameState.hash_board(initial_board)
        initial_move_history[hash_code] = 1
        return GameState(initial_board, Team.RED, initial_move_history, value_pack)

    # [END METHOD]
