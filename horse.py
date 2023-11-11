# Written by Kleecon

from piece import Piece

class Horse(Piece):
    """Class representing a horse"""
    
    def _get_piece_value(self):
        return 4

    def get_admissible_moves(self):

        # Movement
        admissible_moves = []

        # Possible goal positions
        x_orient = [2,2,1,-1,-2,-2,-1,1]
        y_orient = [1,-1,-2,-2,-1,1,2,2]
        maximum_move_count = 8

        # Possible middle move positions
        p_orient = [1,0,-1,0]
        q_orient = [0,-1,0,1]

        for cnt in range(maximum_move_count):

            # Middle position
            pos = (self.position[0] + p_orient[cnt//2], self.position[1] + q_orient[cnt//2])

            # Check the middle position
            if self.is_position_on_board(pos)\
            and self.is_position_free(pos):

                # Goal position
                pos = (self.position[0] + x_orient[cnt], self.position[1] + y_orient[cnt])

                # Check the goal position
                if self.is_position_on_board(pos)\
                and not self.is_position_teammate(pos):
                    admissible_moves.append(pos)

        # Return
        return admissible_moves

if __name__ == "__main__":
    # Test the class here Mortdog
    pass
