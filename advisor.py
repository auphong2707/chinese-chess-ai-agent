#written by Kleecon

from piece import Piece
from team import Team

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
            if self.is_valid_move(pos) and self.is_position_in_palace(pos):
                admissible_moves.append(pos)

        # Capture: Pending

        # return
        return admissible_moves

if __name__ == "__main__":
    #test the class here Mortdog
    pass