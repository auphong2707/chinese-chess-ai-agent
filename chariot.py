# TheSyx
from piece import Piece


class Chariot(Piece):
    """Class representing a chariot"""
    
    _piece_value = 9

    def get_admissible_moves(self) -> list:
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
                    if self.is_position_free(new_position) is False:
                        # Check if the piece on the new position is on the enemy team
                        if self.is_position_opponent(new_position):
                            admissible_moves.append(new_position)
                        break

                    admissible_moves.append(new_position)

        return admissible_moves


if __name__ == "__main__":
    # test the class here Mortdog
    pass
