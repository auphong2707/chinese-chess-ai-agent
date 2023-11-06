# written by Kleecon

from piece import Piece
from team import Team


class Pawn(Piece):
    def __init__(self, position: tuple, init_team: Team) -> None:
        super().__init__(self, position, init_team)
        self._has_crossed_river = False

    @property
    def _has_crossed_river(self):
        if self._has_crossed_river is True:
            return True

        self._has_crossed_river = (
            abs(self.position[0] + 9 * (self.team.value - 1) / 2) < 5
        )

    # Searching admissible moves for the pawn
    def get_admissible_moves(self):
        possible_moves = []

        # Movement
        pos = (self.position[0] - self.team.value, self.position[1])
        if self.is_position_on_board(pos) and not self.is_position_teammate(pos):
            possible_moves.append(pos)

        if self._has_crossed_river is True:
            new_pos = (self.position[0], self.position[1] + 1)
            if self.is_position_on_board(pos) and not self.is_position_teammate(pos):
                possible_moves.append(new_pos)

            new_pos = (self.position[0], self.position[1] - 1)
            if self.is_position_on_board(pos) and not self.is_position_teammate(pos):
                possible_moves.append(new_pos)

        # Capture (it's the same with movement, dang it)

        return possible_moves


if __name__ == "__main__":
    # test the class here Mortdog
    pass
