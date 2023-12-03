# [MODULE]
"""Module providing the UI of the game"""
import pygame
# [END MODULE]

# [CONSTANTS]
ORIGIN_X, ORIGIN_Y = 45, 10
START_X, START_Y = 47, 8
STEP_X, STEP_Y = 63, 65
RESOURCES_PATH = 'resources/'
# [END CONSTANTS]

def piece_sprite(piece):
    """This method will return the sprite of the piece 
    which contains: image of the piece and position (in pixel) of the piece"""

    position_x = START_X + piece.position[1]*STEP_X
    position_y = START_Y + piece.position[0]*STEP_Y

    piece_img = pygame.image.load(RESOURCES_PATH + 'board/' + str(piece) + '.png')

    return piece_img, (position_x, position_y)


def board_sprite():
    """This method will return the board sprite
    which contains: image of the board and position (in pixel) of the piece"""

    chess_board_img = pygame.image.load(RESOURCES_PATH + 'board/' + 'chess_board.png')
    return chess_board_img, (ORIGIN_X, ORIGIN_Y)

def background():
    background_img = pygame.image.load(RESOURCES_PATH + 'background.png')
    return background_img, (0, 0)
    

def icon():
    icon_img = pygame.image.load(RESOURCES_PATH + 'xiangqi_icon.png')
    return icon_img

def get_font(size, index):
    if index == 0:
        return pygame.font.Font(RESOURCES_PATH + "fonts/" + "Real Chinese.otf", size)
    elif index == 1:
        return pygame.font.Font(RESOURCES_PATH + "fonts/" + "Analogist.ttf", size)