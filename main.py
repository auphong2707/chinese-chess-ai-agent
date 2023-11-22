from time import time
import threading
import pygame
import resources
from game_state import GameState
from game_tree import GameTreeMinimax
from team import Team

move_queues = list()

def draw_gamestate(_screen, _game_state):
    """This method will draw a gamestate"""

    board_img, board_position = resources.get_board_sprite()
    _screen.blit(board_img, board_position)

    for piece in _game_state.pieces_list_current + _game_state.pieces_list_opponent:
        piece_img, piece_position = resources.get_piece_sprite(piece)
        _screen.blit(piece_img, piece_position)


def bot_run():
    althea = GameTreeMinimax(Team.RED)
    beth = GameTreeMinimax(Team.BLACK)

    turn = 1
    global moves_queue

    while True:  # Chưa tìm điều kiện để dừng vòng lặp
        # [ALTHEA'S TURN]
        start = time()  # Start time counter

        print("Turn {}:".format(turn))

        althea.minimax(althea.current_node, 0, True)
        old_pos_althea, new_pos_althea = althea.move_to_best_child()
        move_queues.append((old_pos_althea, new_pos_althea))

        print("Red moves:", old_pos_althea, "->", new_pos_althea)
        print(althea.count)

        end = time()  # End time counter

        # Print used time
        print("{:.2f}".format(end - start), "s")

        # [END ALTHEA'S TURN]

        # [BETH'S TURN]
        start = time()  # Start time counter

        beth.move_to_child_node_with_move(old_pos_althea, new_pos_althea)
        beth.minimax(beth.current_node, 0, False)
        old_pos_beth, new_pos_beth = beth.move_to_best_child()
        move_queues.append((old_pos_beth, new_pos_beth))

        print()
        print("Black moves:", old_pos_beth, "->", new_pos_beth)
        print(beth.count)

        end = time()  # End time counter

        # Print used time
        print("{:.2f}".format(end - start), "s")
        print()
        # [END BETH'S TURN]

        # [POST PROCESS]
        althea.move_to_child_node_with_move(old_pos_beth, new_pos_beth)
        althea.count = 0
        beth.count = 0
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
    bot_run_thread.start()
    done = False
    while not done:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Try update_board
        try:
            move = move_queues[0]
            move_queues.pop(0)
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
