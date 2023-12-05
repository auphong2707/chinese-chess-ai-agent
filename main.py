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
force_end = False
pygame.init()

# Set up the window
SCREEN = pygame.display.set_mode((661, 660))
pygame.display.set_caption("Xiangqi")
pygame.display.set_icon(resources.icon())

# Set the refresh rate
REFRESH_RATE = 30

# Create a clock object
clock = pygame.time.Clock()

def pve_screen():
    bot = GameTreeMinimax(Team.BLACK, 3, 1)
    is_bot_process = False
    position_chosen = None
    player_turn, player_gamestate  = True, GameState.generate_initial_game_state()
    while True:
        # Handle event
        events_list = pygame.event.get()
        for event in events_list:
            if event.type == pygame.QUIT:
                force_end = True
                pygame.quit()
                sys.exit()
                
        if player_turn:
            for event in events_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    click_pos = resources.get_piece_position(mouse_pos)
                    print(mouse_pos, click_pos)
                    if position_chosen is None:
                        if click_pos is None:
                            continue
                        if player_gamestate.board[click_pos[0]][click_pos[1]][0] == "R":
                            position_chosen = click_pos
                    else:
                        if click_pos is None or click_pos == position_chosen:
                            position_chosen = None
                            continue
                        
                        piece = Piece.create_instance(
                            position_chosen,
                            player_gamestate.board[position_chosen[0]][position_chosen[1]],
                            player_gamestate.board
                        )
                        
                        if click_pos in piece.admissible_moves:
                            new_gamestate = player_gamestate.generate_game_state_with_move(position_chosen, click_pos)
                            if new_gamestate is not None:
                                player_gamestate = new_gamestate[0]
                                bot.move_to_child_node_with_move(position_chosen, click_pos)
                                position_chosen = None
                                player_turn = False

        else:
            if is_bot_process is False:
                bot_thread = threading.Thread(target=bot.process, args=(moves_queue,))
                bot_thread.start()
                is_bot_process = True
                
            try:
                old_pos, new_pos = moves_queue.pop(0)
                player_gamestate = player_gamestate.generate_game_state_with_move(old_pos, new_pos)[0]
                player_turn = True
                bot_thread.join()
                is_bot_process = False
            except IndexError:
                pass
            
        # Draw
        SCREEN.fill(((241, 203, 157)))
        draw_gamestate(player_gamestate)
        if position_chosen is not None:
            chosen_ring_img, draw_pos = resources.chosen_ring_sprite(position_chosen)
            SCREEN.blit(chosen_ring_img, draw_pos)
        
        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)
    

def result_bots(red_type, black_type):
    global winner
    
    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 550),
                         text_input="QUIT", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 550),
                         text_input="BACK", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")
    
    while True:
        # Draw main menu
        # .background
        bg_img, bg_pos = resources.background()
        SCREEN.blit(bg_img, bg_pos)

        # Text
        text = resources.get_font(70, 0).render(
            "Result", True, "Black")
        rect = text.get_rect(center=(330.5, 60))
        SCREEN.blit(text, rect)
        
        text = resources.get_font(60, 0).render("Black", True, "Black")
        rect = text.get_rect(center=(145, 185))
        SCREEN.blit(text, rect)
        
        text = resources.get_font(12, 2).render(black_type, True, "Black")
        rect = text.get_rect(center=(145, 220))
        SCREEN.blit(text, rect)
        
        text = resources.get_font(60, 0).render(str(winner.get("BLACK", 0)), True, "Black")
        rect = text.get_rect(center=(145, 280))
        SCREEN.blit(text, rect)
        
        text = resources.get_font(12, 2).render(red_type, True, "#AB001B")
        rect = text.get_rect(center=(515, 220))
        SCREEN.blit(text, rect)
        
        text = resources.get_font(60, 0).render("Red", True, "#AB001B")
        rect = text.get_rect(center=(515, 185))
        SCREEN.blit(text, rect)
        
        text = resources.get_font(60, 0).render(str(winner.get("RED", 0)), True, "#AB001B")
        rect = text.get_rect(center=(515, 280))
        SCREEN.blit(text, rect)
        
        
        text = resources.get_font(60, 0).render("Draw", True, "#56000E")
        rect = text.get_rect(center=(330.5, 185))
        SCREEN.blit(text, rect)
        
        text = resources.get_font(60, 0).render(str(winner.get("DRAW", 0)), True, "#56000E")
        rect = text.get_rect(center=(330.5, 280))
        SCREEN.blit(text, rect)
        
        # Button
        for button in [quit_button, back_button]:
            button.draw(SCREEN)
        
        # Handle event
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if back_button.checkForInput(mouse_pos):
                    winner = dict()
                    bots_menu()
        
        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)
    

def bot_run(althea_type, althea_value, althea_ap, beth_type, beth_value, beth_ap):
    althea = althea_type(Team.RED, althea_ap, althea_value)
    beth = beth_type(Team.BLACK, beth_ap, beth_value)
    turn, max_turn = 1, 150
    global is_end, force_end, winner

    while turn <= max_turn:
        if force_end is True:
            return
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

        if force_end is True:
            return
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

    winner["DRAW"] = winner.get("DRAW", 0) + 1
    is_end = True
    print("DRAW")


def draw_gamestate(game_state):
    """This method will draw a gamestate"""

    board_img, board_position = resources.board_sprite()
    SCREEN.blit(board_img, board_position)

    for x in range(GameState.BOARD_SIZE_X):
        for y in range(GameState.BOARD_SIZE_Y):
            notation = game_state.board[x][y]
            if notation == "NN":
                continue

            piece = Piece.create_instance((x, y), notation, game_state.board)
            piece_img, piece_position = resources.piece_sprite(piece)
            SCREEN.blit(piece_img, piece_position)


def simulation(red_type, red_value, red_another_property,
               black_type, black_value, black_another_property,
               number_of_simulations):
    def get_bot_full_type(bot_type, bot_property, bot_value):
        res = bot_type + ' '
        
        if bot_type == 'Minimax':
            res += 'Depth ' + bot_property + ' '
        elif bot_type == 'MCTS':
            res += 'Time allowed ' + bot_property + 's '
        
        res += 'Value ' + bot_value    
            
        return res
    
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
    
    red_full_type = get_bot_full_type(red_type, red_another_property, red_value)
    black_full_type = get_bot_full_type(black_type, black_another_property, black_value)
    
    red_type, black_type = str_to_type(red_type), str_to_type(black_type)
    red_value, black_value = str_to_value_pack(
        red_value), str_to_value_pack(black_value)

    red_another_property, black_another_property = int(
        red_another_property), int(black_another_property)
    number_of_simulations = int(number_of_simulations)

    # Main game loop
    start = time()
    global is_end, force_end
    is_end = True
    gamestate, bot_run_thread = None, None
    games_done_count = 0
    while True:
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
                force_end = True
                pygame.quit()
                sys.exit()   

        # Try update_board
        try:
            move = moves_queue.pop(0)
            gamestate = gamestate.generate_game_state_with_move(move[0], move[1])[0]
        except IndexError:
            pass

        # Clear the screen
        SCREEN.fill((241, 203, 157))

        # Draw here
        draw_gamestate(gamestate)

        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)

    print(winner)
    end = time()
    print("Total time: {} s".format(end - start))
    print()
    # Quit Pygame
    result_bots(red_full_type, black_full_type)


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

    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 550),
                         text_input="QUIT", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 550),
                         text_input="BACK", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")
    
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
        for button in [start_button, quit_button, back_button]:
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
                        or not num_box.text.isnumeric()
                        or not red_another_property.text.isnumeric()
                        or not black_another_property.text.isnumeric()
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
                if back_button.checkForInput(mouse_pos):
                    main_menu()

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
                    pve_screen()
                    pve_screen()
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
