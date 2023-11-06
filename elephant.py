# By Khanh

from piece import Piece
from team import Team

class Elephant:
    def get_admissible_moves(self):

        admissible_moves = []

        # Possible goal positions
        x_direction = [2, 2, -2, -2]
        y_direction = [2, -2, 2, -2]
        maximum_move_count = 4
        
        # Possible block positions
        x_block = [1, 1, -1, -1]
        y_block = [1, -1, 1, -1]

        for direction in range (maximum_move_count):
            
            new_pos = (self.position[0] + x_direction[direction], self.position[0] + y_direction[direction])
            
            block_pos =(self.position[0] + x_block[direction], self.position[0] + y_block[direction])

            # Check if the new position is in board and there is no piece between old position and new position
            if self.is_position_on_board(new_pos) and self.is_position_free(block_pos):

                # Check if the new position is free or have piece to catch
                if self.is_position_free(new_pos) or self.is_position_opponent(new_pos):
                    
                    admissible_moves.append(new_pos)
        
        return admissible_moves                  

if __name__ == "__main__":
    #test the class here Mortdog
    pass

