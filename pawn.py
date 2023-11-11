# written by Kleecon

from piece import Piece
from team import Team


class Pawn(Piece):
    """Class representing a pawn"""

    _has_crossed_river = False

    @property
    def has_crossed_river(self):
        """Return True if the pawn is crossed the river"""
        if self._has_crossed_river is True:
            return True

        self._has_crossed_river = (
            abs(self.position[0] + 9 * (self.team.value - 1) / 2) < 5
        )

    def _get_piece_value(self):
        if self.has_crossed_river is True:
            return 2
        else:
            return 1
        
    # Searching admissible moves for the pawn
    def get_admissible_moves(self):
        possible_moves = []

        # Movement
        new_pos = (self.position[0] - self.team.value, self.position[1])
        if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos):
            possible_moves.append(new_pos)

        if self.has_crossed_river is True:
            new_pos = (self.position[0], self.position[1] + 1)
            if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos):
                possible_moves.append(new_pos)

            new_pos = (self.position[0], self.position[1] - 1)
            if self.is_position_on_board(new_pos) and not self.is_position_teammate(new_pos):
                possible_moves.append(new_pos)

        # Capture (it's the same with movement, dang it)

        return possible_moves


if __name__ == "__main__":
    # test the class here Mortdog
    pass
