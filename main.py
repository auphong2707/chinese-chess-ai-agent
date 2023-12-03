from time import time
from concurrent.futures import ProcessPoolExecutor
import threading
import pygame
import resources
import sys
from gui_utilities import Button, DropDown, InputBox
from game_state import GameState
from game_tree import GameTreeMinimax, GameTreeMCTS
from team import Team
from piece import Piece

moves_queue = list()
winner = dict()
is_end = False

pygame.init()

# Set up the window
SCREEN = pygame.display.set_mode((661, 660))
pygame.display.set_caption("Xiangqi")

# Set the refresh rate
REFRESH_RATE = 30

# Create a clock object
clock = pygame.time.Clock()


def bot_run(althea_type, althea_value, althea_ap, beth_type, beth_value, beth_ap):
    althea = althea_type(Team.RED, althea_ap, althea_value)
    beth = beth_type(Team.BLACK, beth_ap, beth_value)
    turn, max_turn = 1, 150
    global is_end

    while turn <= max_turn:
        # [ALTHEA'S TURN]
        # Check whether Althea has been checkmated
        if althea.is_lost() is True:
            winner[beth.team.name] = winner.get(beth.team.name, 0) + 1
            print("Checkmate! {} wins!".format(beth.team.name))
            print()
            is_end = True
            return
        print("Turn: {}".format(turn))
        old_pos, new_pos = althea.process(moves_queue)
        beth.move_to_child_node_with_move(old_pos, new_pos)

        # [END ALTHEA'S TURN]

        # [BETH'S TURN]
        # Check whether Beth has been checkmated
        if beth.is_lost() is True:
            winner[althea.team.name] = winner.get(althea.team.name, 0) + 1
            print("Checkmate! {} wins!".format(althea.team.name))
            print()
            is_end = True
            return
        old_pos, new_pos = beth.process(moves_queue)
        althea.move_to_child_node_with_move(old_pos, new_pos)

        # [END BETH'S TURN]

        turn += 1

    winner["Draw"] = winner.get("Draw", 0) + 1
    is_end = True
    print("Draw")


def draw_gamestate(_screen, _game_state):
    """This method will draw a gamestate"""

    board_img, board_position = resources.board_sprite()
    _screen.blit(board_img, board_position)

    for x in range(GameState.BOARD_SIZE_X):
        for y in range(GameState.BOARD_SIZE_Y):
            notation = _game_state.board[x][y]
            if notation == "NN":
                continue

            piece = Piece.create_instance((x, y), notation, _game_state.board)
            piece_img, piece_position = resources.piece_sprite(piece)
            _screen.blit(piece_img, piece_position)


def simulation(red_type, red_value, red_another_property,
               black_type, black_value, black_another_property,
               number_of_simulations):
    def str_to_type(type_str):
        if type_str == 'Minimax':
            return GameTreeMinimax
        elif type_str == 'MCTS':
            return GameTreeMCTS

    def str_to_value_pack(value_pack_str):
        if value_pack_str == 'Default':
            return 0
        elif value_pack_str == 'Moded':
            return 1

    red_type, black_type = str_to_type(red_type), str_to_type(black_type)
    red_value, black_value = str_to_value_pack(
        red_value), str_to_value_pack(black_value)

    red_another_property, black_another_property = int(
        red_another_property), int(black_another_property)
    number_of_simulations = int(number_of_simulations)

    # Main game loop
    global is_end
    is_end = True
    done = False
    gamestate, bot_run_thread = None, None
    games_done_count = 0
    while not done:
        if is_end is True:
            games_done_count += 1
            if games_done_count > number_of_simulations:
                break

            is_end = False
            if bot_run_thread is not None:
                bot_run_thread.join()
            bot_run_thread = threading.Thread(target=bot_run, args=(
                red_type, red_value, red_another_property,
                black_type, black_value, black_another_property
            ))

            moves_queue.clear()
            gamestate = GameState.generate_initial_game_state()
            bot_run_thread.start()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Try update_board
        try:
            move = moves_queue.pop(0)
            gamestate = gamestate.generate_game_state_with_move(move[0], move[1])[0]
        except IndexError:
            pass

        # Clear the screen
        SCREEN.fill((241, 203, 157))

        # Draw here
        draw_gamestate(SCREEN, gamestate)

        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)

    print(winner)
    # Quit Pygame
    pygame.quit()
    sys.exit()

