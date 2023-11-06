from piece import Piece
from team import Team
from abc import ABC

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

            if self.is_position_free(new_pos)

