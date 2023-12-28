# [MODULE]
"""Module providing the UI of the game"""
import pygame
# [END MODULE]

# [CONSTANTS]
ORIGIN_X, ORIGIN_Y = 45, 10
START_X, START_Y = 47, 8
STEP_X, STEP_Y = 63, 65
PIECE_SIZE = 60
RESOURCES_PATH = 'resources/'
# [END CONSTANTS]

def piece_sprite(piece):
    """This method returns the sprite of the piece 
    which contains: image of the piece and position (in pixel) of the piece"""

    position_x = START_X + piece.position[1]*STEP_X
    position_y = START_Y + piece.position[0]*STEP_Y

    piece_img = pygame.image.load(RESOURCES_PATH + 'board/' + str(piece) + '.png')

    return piece_img, (position_x, position_y)

def chosen_ring_sprite(pos, inverse: bool = False):
    """This method returns the sprite of the chosen ring sprite
    which contains: image of the chosen ring and chosen piece position (in pixel)"""
    chosen_ring_img = pygame.image.load(RESOURCES_PATH + 'chosen_ring.png')
    pos = (abs(pos[0] - 9 * int(inverse)), pos[1])
    
    position_x = START_X + pos[1]*STEP_X
    position_y = START_Y + pos[0]*STEP_Y
    
    return chosen_ring_img, (position_x, position_y)

def get_piece_position(pos, inverse: bool = False):
    """This method returns the position of the piece in game board"""
    position_x = (pos[1] - START_Y)//STEP_Y
    position_y = (pos[0] - START_X)//STEP_X
    
    if (
        position_x not in range(0, 10) 
        or position_y not in range(0, 9)
    ):
        return None
    return abs(position_x - 9 * int(inverse)), position_y

def board_sprite():
    """This method will return the board sprite
    which contains: image of the board and position (in pixel) of the piece"""

    chess_board_img = pygame.image.load(RESOURCES_PATH + 'board/' + 'chess_board.png')
    return chess_board_img, (ORIGIN_X, ORIGIN_Y)

def background():
    """This method return background sprite"""
    background_img = pygame.image.load(RESOURCES_PATH + 'background.png')
    return background_img, (0, 0)
    

def icon():
    """This method return the icon image"""
    icon_img = pygame.image.load(RESOURCES_PATH + 'xiangqi_icon.png')
    return icon_img


def get_font(size, index):
    """This method return prepared fonts"""
    if index == 0:
        return pygame.font.Font(RESOURCES_PATH + "fonts/" + "Real Chinese.otf", size)
    elif index == 1:
        return pygame.font.Font(RESOURCES_PATH + "fonts/" + "Analogist.ttf", size)
    elif index == 2:
        return pygame.font.Font(RESOURCES_PATH + "fonts/" + "sanva font.ttf", size)