# Made by: Veil
import time
from cmath import inf
from random import randint, shuffle
from piece import General, Advisor, Elephant, Rook, Cannon, Horse, Pawn, Piece
from team import Team
from copy import deepcopy


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
        board: list,
        current_team: Team,
        value_pack: int = 0
    ) -> None:
        # Add the chess pieces to the list
        self.board = board

        # Declare properties
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
    def _get_game_state_value(self):
        """Return the evaluation value of the board"""

        if self.get_team_win() is Team.RED:
            return inf

        if self.get_team_win()  is Team.BLACK:
            return -inf

        current_value = 0
        # Iterate through all position in the board
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                # Get the notation of the position
                notation = self.board[i][j]
                # If the notation is empty, then there is no piece at that position -> skip
                if notation == "NN":
                    continue

                # Otherwise, create a instance of the piece and take value of the piece
                piece = Piece.create_instance((i, j), notation, self.board)
                current_value += piece.piece_value(self._value_pack) * piece.team.value

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

        self.board[old_pos[0]][old_pos[1]] = "NN"
        self.board[new_pos[0]][new_pos[1]] = old_pos_notation

        # Get the opponent team
        opponent = self._get_the_opponent_team()

        # Check if the game state is valid
        def _return_to_old_state():
            self.board[old_pos[0]][old_pos[1]] = old_pos_notation
            self.board[new_pos[0]][new_pos[1]] = new_pos_notation

        # .If the check is not passed, then return None
        if General.is_general_exposed(self.board, self._current_team, opponent) is False:
            _return_to_old_state()
            return None

        # Create a copy of moved board and return the board to the old state
        new_board = list(map(list, self.board))
        _return_to_old_state()
        # Return the game state which has the new information
        return GameState(new_board, opponent, self._value_pack), (old_pos, new_pos)

    def generate_random_game_state(self):
        """This method will generate another gamestate that can be tranformed
        by current method using each move of the piece"""
        # Get all position of curretn team's piece into a list and randomly shuffle it
        team_positions = list()
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                notation = self.board[i][j]

                if Team[notation[0]] is self._current_team:
                    team_positions.append((i, j))

        shuffle(team_positions)

        # Iterate through every piece in the list, generate the piece's move list and shuffle it
        for pos in team_positions:
            notation = self.board[pos[0]][pos[1]]
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

                if notation == "NN":
                    continue

                if Team[notation[0]] is self._current_team:
                    moves_list = Piece.create_instance(
                        (i, j), notation, self.board
                    ).admissible_moves

                    for new_pos in moves_list:
                        game_state = self.generate_game_state_with_move((i, j), new_pos)

                        if game_state is not None:
                            game_states_available.append(game_state)

        return game_states_available

    def get_team_win(self):
        """This method return the winning team"""

        # If the current game state has child game states, then return Team.NONE
        for i in range(self.BOARD_SIZE_X):
            for j in range(self.BOARD_SIZE_Y):
                notation = self.board[i][j]
                if notation == "NN":
                    continue
                
                if Team[notation[0]] is self._current_team:
                    moves_list = Piece.create_instance(
                        (i, j), notation, self.board
                    ).admissible_moves
                    
                    old_pos = (i, j)
                    for new_pos in moves_list:
                        old_pos_notation = self.board[old_pos[0]][old_pos[1]]
                        new_pos_notation = self.board[new_pos[0]][new_pos[1]]

                        self.board[old_pos[0]][old_pos[1]] = "NN"
                        self.board[new_pos[0]][new_pos[1]] = old_pos_notation
                        
                        if General.is_general_exposed(self.board, self._current_team, self._get_the_opponent_team()) is True:
                            self.board[old_pos[0]][old_pos[1]] = old_pos_notation
                            self.board[new_pos[0]][new_pos[1]] = new_pos_notation
                            return Team.NONE
                        
                        self.board[old_pos[0]][old_pos[1]] = old_pos_notation
                        self.board[new_pos[0]][new_pos[1]] = new_pos_notation

        # Return the opponent if current team has no admissible move
        return self._get_the_opponent_team()

    # Class method
    @classmethod
    def generate_initial_game_state(cls, value_pack: int=0):
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
        return GameState(initial_board, Team.RED, value_pack)

    # [END METHOD]


if __name__ == '__main__':
    import psutil
    queue = [GameState.generate_initial_game_state()]
    for depth in range(1, 5):
        start = time.time()

        new_queue = list()
        for game_state_ in queue:
            for state, move_ in game_state_.all_child_gamestates:
                new_queue.append(state)

        queue = new_queue
        end = time.time()
        print(depth, len(queue), end - start)

    pid = psutil.Process()
    memory_info = pid.memory_info()
    print(f"Memory Usage: {memory_info.rss/(1024**2)} megabytes")
