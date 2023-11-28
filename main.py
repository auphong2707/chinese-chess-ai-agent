from time import time
from concurrent.futures import ProcessPoolExecutor
import threading
import pygame
import resources
from game_state import GameState
from game_tree import GameTreeMinimax, GameTreeMCTS
from team import Team

moves_queue = list()

def draw_gamestate(_screen, _game_state):
    """This method will draw a gamestate"""

    board_img, board_position = resources.get_board_sprite()
    _screen.blit(board_img, board_position)

    for piece in _game_state.pieces_list_current + _game_state.pieces_list_opponent:
        piece_img, piece_position = resources.get_piece_sprite(piece)
        _screen.blit(piece_img, piece_position)


def bot_run():
    althea = GameTreeMCTS(Team.RED, 10)
    beth = GameTreeMinimax(Team.BLACK, 3)
    turn = 1

    while True:
        print("Turn {}:".format(turn))
        # [ALTHEA'S TURN]
        # Check whether Althea has been checkmated
        if althea.is_lost() is True:
            print("Checkmate. {} wins.".format(beth.team.name))
            break
        old_pos, new_pos = althea.process(moves_queue)
        beth.move_to_child_node_with_move(old_pos, new_pos)

        # [END ALTHEA'S TURN]

        # [BETH'S TURN]
        # Check whether Beth has been checkmated
        if beth.is_lost() is True:
            print(("Checkmate. {} wins.".format(althea.team.name)))
            break
        old_pos, new_pos = beth.process(moves_queue)
        althea.move_to_child_node_with_move(old_pos, new_pos)

        # [END BETH'S TURN]

        turn += 1

if __name__ == '__main__':
    # Initialize Pygame
    pygame.init()
    bot_run_thread = threading.Thread(target=bot_run)

    # Set up the window
    size = (661, 660)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Xiangqi")

    # Set the refresh rate
    REFRESH_RATE = 30

    # Create a clock object
    clock = pygame.time.Clock()

    # Create game_state
    gamestate = GameState.generate_initial_game_state()

    # Main game loop

    with ProcessPoolExecutor(8) as exe:
        bot_run_thread.start()
    done = False
    while not done:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Try update_board
        try:
            move = moves_queue[0]
            moves_queue.pop(0)
            gamestate = gamestate.generate_game_state_with_move(move[0], move[1])[0]
        except IndexError:
            pass

        # Clear the screen
        screen.fill((241, 203, 157))

        # Draw here
        draw_gamestate(screen, gamestate)

        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)

    bot_run_thread.join()

    # Quit Pygame
    pygame.quit()