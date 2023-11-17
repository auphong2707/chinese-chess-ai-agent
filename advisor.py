# Written by Kleecon

from piece import Piece


class Advisor(Piece):
    """Class representing an advisor"""

    _piece_value = 2
    
    def get_admissible_moves(self):
        # Movement
        admissible_moves = []

        # Possible goal positions
        x_orient = [1, 1, -1, -1]
        y_orient = [1, -1, -1, 1]
        maximum_move_count = 4

        # Iteration through all positions
        for cnt in range(maximum_move_count):
            # Possible position setting
            pos = (self.position[0] + x_orient[cnt], self.position[1] + y_orient[cnt])

            # Checkment
            if (
                self.is_position_on_board(pos)
                and not self.is_position_teammate(pos)
                and self.is_position_in_palace(pos)
            ):
                admissible_moves.append(pos)

        # Return
        return admissible_moves

    def create_copy(self, new_board):
        return Advisor(self.position, self.team, new_board)

if __name__ == "__main__":
    # Test the class here Mortdog
    pass
