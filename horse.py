#written by Kleecon

from piece import Piece

class Horse(Piece):
    #why horse, why?

    def get_admissible_moves(self):
        # Movement
        admissible_moves = []

        # possible goal positions
        x_orient = [2,2,1,-1,-2,-2,-1,1]
        y_orient = [1,-1,-2,-2,-1,1,2,2]
        maximum_move_count = 8

        # possible middle move positions
        p_orient = [1,0,-1,0]
        q_orient = [0,-1,0,1]

        for cnt in range(maximum_move_count):

            # middle position
            pos = (self.position[0] + p_orient[cnt//2], self.position[1] + q_orient[cnt//2])

            # check the middle position
            if self.is_position_on_board(pos) and self.is_position_free(pos):

                # goal position
                pos = (self.position[0] + x_orient[cnt], self.position[1] + y_orient[cnt])

                # check the goal position
                if self.is_position_on_board(pos) and self.get_piece_team_on_position(pos) != self.team.value:
                    admissible_moves.append(pos)

        # Capture: wtf

        return admissible_moves

if __name__ == "__main__":
    #test the class here Mortdog
    pass
