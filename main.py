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


def bots_menu():
    black_type = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        20, 290, 100, 30,
        pygame.font.SysFont(None, 25),
        "Type", ["Minimax", "MCTS"])

    black_value = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        180, 290, 100, 30,
        pygame.font.SysFont(None, 25),
        "Pack", ["Default", "Moded"])

    red_type = DropDown(
        ["#DC1C13", "#EA4C46"],
        ["#F07470", "#F1959B"],
        350, 290, 100, 30,
        pygame.font.SysFont(None, 25),
        "Type", ["Minimax", "MCTS"])

    red_value = DropDown(
        ["#DC1C13", "#EA4C46"],
        ["#F07470", "#F1959B"],
        510, 290, 100, 30,
        pygame.font.SysFont(None, 25),
        "Pack", ["Default", "Moded"]
    )

    num_box = InputBox(330, 125, 40, 40, pygame.font.SysFont(
        None, 35), "Black", "Red", "Number of simulations")

    black_another_property = InputBox(165, 230, 40, 30, pygame.font.SysFont(
        None, 25), "Black", "Red", "Depth/Time allowed")
    red_another_property = InputBox(495, 230, 40, 30, pygame.font.SysFont(
        None, 25), "Red", "Black", "Depth/Time allowed")

    start_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(330.5, 450),
                          text_input="Simulate", font=resources.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    quit_button = Button(image=pygame.image.load("resources/button/quit_rect.png"), pos=(330.5, 550),
                         text_input="QUIT", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    while True:
        # Draw main menu
        # .background
        bg_img, bg_pos = resources.background()
        SCREEN.blit(bg_img, bg_pos)

        # Text
        menu_text = resources.get_font(70, 0).render(
            "Bots select", True, "Black")
        menu_rect = menu_text.get_rect(center=(330.5, 60))
        SCREEN.blit(menu_text, menu_rect)

        text = resources.get_font(60, 0).render("Black", True, "Black")
        rect = text.get_rect(center=(165, 185))
        SCREEN.blit(text, rect)

        text = resources.get_font(30, 0).render("Bot type", True, "Black")
        rect = text.get_rect(center=(70, 270))
        SCREEN.blit(text, rect)

        text = resources.get_font(30, 0).render("Value pack", True, "Black")
        rect = text.get_rect(center=(230, 270))
        SCREEN.blit(text, rect)

        text = resources.get_font(60, 0).render("Red", True, "#AB001B")
        rect = text.get_rect(center=(495, 185))
        SCREEN.blit(text, rect)

        text = resources.get_font(30, 0).render("Bot type", True, "#AB001B")
        rect = text.get_rect(center=(400, 270))
        SCREEN.blit(text, rect)

        text = resources.get_font(30, 0).render("Value pack", True, "#AB001B")
        rect = text.get_rect(center=(560, 270))
        SCREEN.blit(text, rect)

        # Button
        for button in [start_button, quit_button]:
            button.draw(SCREEN)

        event_list = pygame.event.get()
        # List
        for lst in [black_type, black_value, red_type, red_value]:
            selected_option = lst.update(event_list)
            if selected_option >= 0:
                lst.main = lst.options[selected_option]

            lst.draw(SCREEN)

        # Input box
        for input_box in [num_box, black_another_property, red_another_property]:
            input_box.update()
            input_box.draw(SCREEN)

        # Handle events
        mouse_pos = pygame.mouse.get_pos()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkForInput(mouse_pos):
                    if (
                        red_type.main == "Type" or black_type.main == "Type"
                        or red_value.main == "Pack" or red_value.main == "Pack"
                    ):
                        continue
                    simulation(
                        red_type.main, red_value.main, red_another_property.text,
                        black_type.main, black_value.main, black_another_property.text,
                        num_box.text
                    )
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

            for input_box in [num_box, black_another_property, red_another_property]:
                input_box.handle_event(event)

         # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)


def main_menu():
    pve_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(165, 250),
                    text_input="PvE", font=resources.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    eve_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(495, 250),
                        text_input="EvE", font=resources.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(330.5, 350),
                            text_input="QUIT", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")
    
    while True:
        # Draw main menu
        # .background
        bg_img, bg_pos = resources.background()
        SCREEN.blit(bg_img, bg_pos)

        # .menu_text
        menu_text = resources.get_font(100, 0).render("Xiangqi", True, "Black")
        menu_rect = menu_text.get_rect(center=(330.5, 100))
        SCREEN.blit(menu_text, menu_rect)

        # .button
        for button in [pve_button,  eve_button, quit_button]:
            button.draw(SCREEN)

        # Handle events
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pve_button.checkForInput(mouse_pos):
                    pass
                if eve_button.checkForInput(mouse_pos):
                    bots_menu()
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)


if __name__ == "__main__":
    main_menu()
