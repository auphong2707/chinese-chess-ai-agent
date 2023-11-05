#written by Kleecon

from piece import Piece

class Advisor(Piece):

    def get_admissible_moves(self):
        # Movement
        admissible_moves = []

        # possible goal positions
        x_orient = [1,1,-1,-1]
        y_orient = [1,-1,-1,1]
        maximum_move_count = 4

        # iteration through all positions
        for cnt in range(maximum_move_count):

            # Possible position setting
            pos = (self.position[0] + x_orient[cnt], self.position[1] + y_orient[cnt])

            # Checkment
            if self.get_piece_team_on_position(pos) != self.team.value:
                if self.is_position_in_palace(pos):
                    admissible_moves.append(pos)

        # return
        return admissible_moves

if __name__ == "__main__":
    #test the class here Mortdog
    pass
