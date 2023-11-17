from piece import Piece


class General(Piece):
    """Class representing a general"""

    _piece_value =  0
    
    def get_admissible_moves(self) -> list:
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
                if self.is_position_free(new_position):
                    admissible_moves.append(new_position)

                # Check if the piece on the new position is on the enemy team
                elif self.is_position_opponent(new_position):
                    admissible_moves.append(new_position)

        return admissible_moves

    def create_copy(self, new_board):
        return General(self.position, self.team, new_board)


if __name__ == "__main__":
    # Test the class here Mortdog
    pass
