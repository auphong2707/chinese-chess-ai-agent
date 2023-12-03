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


if __name__ == "__main__":
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

    # Main game loop
    is_end = True
    done = False
    gamestate, bot_run_thread = None, None
    number_of_games = 0
    while not done:
        if is_end is True:
            number_of_games += 1
            if number_of_games > 50:
                break

            is_end = False
            if bot_run_thread is not None:
                bot_run_thread.join()
            bot_run_thread = threading.Thread(target=bot_run)

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
        screen.fill((241, 203, 157))

        # Draw here
        draw_gamestate(screen, gamestate)

        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)

    # Quit Pygame
    pygame.quit()

    print(winner)
