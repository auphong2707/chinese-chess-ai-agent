from time import time
from concurrent.futures import ProcessPoolExecutor
import threading
import pygame
import resources
import sys
import gc
from gui_utilities import Button, DropDown, InputBox
from game_state import GameState
from game_tree import GameTree, GameTreeMinimax, GameTreeMCTS, GameTreeDynamicMinimax, GameTreeDeepeningMinimax, GameTreeExcavationMinimax
from team import Team
from piece import Piece
import os

# [BEGIN INITIALIZING CONSTANT]
# Limit the memory usage
os.environ['PYPY_GC_MAX_DELTA'] = '3000 MB'
os.environ['PYPY_GC_MAX_EXTERNAL_SIZE'] = '1000 MB'

# Create global variables
# contains move and the game state value solved in bot run thread
moves_queue, value_queue = list(), list()
winner = dict()                             # result of the EvE mode
# global variable to control the game flow
is_end, force_end = False, False

# Initialize Pygame
pygame.init()

# Set up the window
SCREEN = pygame.display.set_mode((661, 660))
pygame.display.set_caption("Xiangqi")
pygame.display.set_icon(resources.icon())

# Set the refresh rate
REFRESH_RATE = 30

# Create a clock object
clock = pygame.time.Clock()
# [END INITIALIZING CONSTANT]

# [BEGIN MAIN FUNCTION]
# Additional functions
def str_to_type(type_str: str) -> GameTree:
    """This function returns the type of GameTree corresponding to the input string"""
    if type_str == 'Minimax':
        return GameTreeMinimax
    elif type_str == 'MCTS':
        return GameTreeMCTS
    elif type_str == 'DyMinimax':
        return GameTreeDynamicMinimax
    elif type_str == 'DeMinimax':
        return GameTreeDeepeningMinimax
    elif type_str == 'ExMinimax':
        return GameTreeExcavationMinimax


def draw_gamestate(game_state: GameState, inverse: bool = False) -> None:
    """This function draws a gamestate"""

    # Draw board
    board_img, board_position = resources.board_sprite()
    SCREEN.blit(board_img, board_position)

    # Draw pieces
    for x in range(GameState.BOARD_SIZE_X):
        for y in range(GameState.BOARD_SIZE_Y):
            notation = game_state.board[x][y]

            # Skip if there is no piece in the position
            if notation == "NN":
                continue

            # Create an instance of the piece using notation
            piece = Piece.create_instance(
                (abs(x - int(inverse) * 9), y),
                notation, game_state.board, None, None
            )

            # Get the piece sprite and draw it
            piece_img, piece_position = resources.piece_sprite(piece)
            SCREEN.blit(piece_img, piece_position)

# Screen function


def pve_screen(
    bot_type: GameTree,
    bot_value: int,
    bot_another_property: int,
    player_team: Team
) -> None:
    """This function is the game screen in the PvE mode"""

    # Create bot variables
    bot = bot_type(Team.get_reverse_team(player_team), bot_another_property, bot_value)
    is_bot_process = False

    # Create player variables
    player_turn = player_team is Team.RED
    player_gamestate = GameState.generate_initial_game_state()

    # Create move variables
    position_chosen, piece_chosen = None, None
    last_move = None

    # Create ultilites
    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 530),
                         text_input="QUIT", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 530),
                         text_input="BACK", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    # Start the game loop
    while True:
        # Get the current game status
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()
        win_status = player_gamestate.get_team_win()

        # Handle event
        for event in events_list:
            # Quit the game if the exit button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If the game is end, the button can be used
            if win_status is not Team.NONE and event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if back_button.check_for_input(mouse_pos):
                    pve_menu()

        # Draw
        # .Background
        SCREEN.fill(((241, 203, 157)))

        # .Gamestate
        draw_gamestate(player_gamestate, player_team is Team.BLACK)

        # .Chosen piece
        if position_chosen is not None:
            chosen_ring_img, draw_pos = resources.chosen_ring_sprite(position_chosen)
            SCREEN.blit(chosen_ring_img, draw_pos)

        # .Last move's chosen ring
        if last_move is not None:
            chosen_ring_img, draw_pos = resources.chosen_ring_sprite(last_move[0], player_team is Team.BLACK)
            SCREEN.blit(chosen_ring_img, draw_pos)

            chosen_ring_img, draw_pos = resources.chosen_ring_sprite(last_move[1], player_team is Team.BLACK)
            SCREEN.blit(chosen_ring_img, draw_pos)

        # If the game is end, draw the announcement and button
        if win_status is not Team.NONE:
            # .Announcement
            pygame.draw.rect(SCREEN, "#AB001B", pygame.Rect(0, 270, 660, 120))
            pygame.draw.rect(SCREEN, "#F6F5E0", pygame.Rect(4, 274, 652, 112))

            if win_status is player_team:
                text = resources.get_font(50, 0).render("Congratulation, you win!", True, "Black")
            else:
                text = resources.get_font(50, 0).render("Better luck next time", True, "Black")
            rect = text.get_rect(center=(330.5, 330))
            SCREEN.blit(text, rect)

            # .Buttons
            for button in [quit_button, back_button]:
                button.draw(SCREEN)

        # Otherwise, solve a movement
        else:
            # If the current turn is for player
            if player_turn:
                for event in events_list:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Calculate the click position in the UI, click position in the game state's board
                        click_pos = resources.get_piece_position(mouse_pos)
                        board_pos = resources.get_piece_position(mouse_pos, player_team is Team.BLACK)

                        # If the click position is out of the board or on the chosen piece
                        # then unchoose the piece
                        if click_pos is None or click_pos == position_chosen:
                            position_chosen, piece_chosen = None, None
                            continue

                        notation = player_gamestate.board[board_pos[0]][board_pos[1]]
                        # If the piece belongs to the player, choose the piece
                        if Team[notation[0]] is player_team:
                            position_chosen = click_pos
                            piece_chosen = Piece.create_instance(
                                board_pos, 
                                notation, 
                                player_gamestate.board, 
                                None, None
                            )

                        # If the click position is in the list of admissible moves of the chosen piece
                        elif piece_chosen is not None and board_pos in piece_chosen.admissible_moves:
                            new_gamestate = player_gamestate.generate_game_state_with_move(piece_chosen.position, board_pos)
                            # If the move is valid, then move to the position
                            if new_gamestate is not None:
                                player_gamestate = new_gamestate[0]
                                bot.move_to_child_node_with_move(piece_chosen.position, board_pos)

                                last_move = (piece_chosen.position, board_pos)
                                position_chosen, piece_chosen = None, None
                                player_turn = False

            # If the current turn is for bot
            else:
                # Process the bot if the bot hasn't
                if is_bot_process is False:
                    # Create a thread to run the bot
                    bot_thread = threading.Thread(
                        target=bot.process, args=(moves_queue,))
                    bot_thread.start()

                    # Mark that the bot has ran
                    is_bot_process = True

                # Try to take a move
                try:
                    # Move the piece in the player's gamestate
                    old_pos, new_pos = moves_queue.pop(0)
                    player_gamestate = player_gamestate.generate_game_state_with_move(old_pos, new_pos)[0]

                    # End the bot run thread
                    bot_thread.join()

                    # Post process
                    is_bot_process = False
                    player_turn = True
                    last_move = (old_pos, new_pos)
                except IndexError:
                    pass

        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)


def pve_menu() -> None:
    """This function is the PvE menu screen"""

    # Create uilities
    bot_type = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        20, 270, 100, 30,
        pygame.font.SysFont(None, 25),
        "Type", ["Minimax", "MCTS", "DyMinimax", "DeMinimax", "ExMinimax"])

    bot_value = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        180, 270, 100, 30,
        pygame.font.SysFont(None, 25),
        "Pack", ["0", "1", "2"])

    team_select = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        430, 220, 150, 50,
        pygame.font.SysFont(None, 30),
        "Team", ["BLACK", "RED"])

    bot_another_property = InputBox(165, 210, 40, 30, pygame.font.SysFont(
        None, 25), "Black", "Red", "Depth/Time allowed")

    start_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(330.5, 430),
                          text_input="Simulate", font=resources.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 530),
                         text_input="QUIT", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 530),
                         text_input="BACK", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    # Start the game loop
    while True:
        # Get the current game status
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Draw
        # .Background
        bg_img, bg_pos = resources.background()
        SCREEN.blit(bg_img, bg_pos)

        # .Text
        menu_text = resources.get_font(70, 0).render("PvE Menu", True, "Black")
        menu_rect = menu_text.get_rect(center=(330.5, 60))
        SCREEN.blit(menu_text, menu_rect)

        text = resources.get_font(50, 0).render("Bot select", True, "Black")
        rect = text.get_rect(center=(165, 165))
        SCREEN.blit(text, rect)

        text = resources.get_font(30, 0).render("Bot type", True, "Black")
        rect = text.get_rect(center=(70, 250))
        SCREEN.blit(text, rect)

        text = resources.get_font(30, 0).render("Value pack", True, "Black")
        rect = text.get_rect(center=(230, 250))
        SCREEN.blit(text, rect)

        text = resources.get_font(50, 0).render("Team Select", True, "Black")
        rect = text.get_rect(center=(495, 165))
        SCREEN.blit(text, rect)

        # .Button
        for button in [start_button, quit_button, back_button]:
            button.draw(SCREEN)

        # .List
        for lst in [bot_type, bot_value, team_select]:
            selected_option = lst.update(events_list)
            if selected_option >= 0:
                lst.main = lst.options[selected_option]

            lst.draw(SCREEN)

        # .Input box
        for input_box in [bot_another_property]:
            input_box.update()
            input_box.draw(SCREEN)

        # Handle events
        for event in events_list:
            # Quit the game if the exit button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle the button click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check_for_input(mouse_pos):
                    if (
                        bot_type.main == "Type"
                        or bot_value.main == "Pack"
                        or team_select.main == "Team"
                        or not bot_another_property.text.isnumeric()
                    ):
                        continue

                    pve_screen(
                        str_to_type(bot_type.main),
                        int(bot_value.main),
                        int(bot_another_property.text),
                        Team[team_select.main]
                    )
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if back_button.check_for_input(mouse_pos):
                    main_menu()

            # Handle the input box events
            for input_box in [bot_another_property]:
                input_box.handle_event(event)

         # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)


def eve_result(red_type: str, black_type: str) -> None:
    """This function is EvE result screen"""

    # Set the screen to normal size
    SCREEN = pygame.display.set_mode((661, 660))

    # Get the global variable
    global winner

    # Create utilities
    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(165, 550),
                         text_input="QUIT", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    back_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(495, 550),
                         text_input="BACK", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    # Start the game loop
    while True:
        # Get the current game status
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Draw main menu
        # .Background
        bg_img, bg_pos = resources.background()
        SCREEN.blit(bg_img, bg_pos)

        # .Text
        text = resources.get_font(70, 0).render("Result", True, "Black")
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

        # .Button
        for button in [quit_button, back_button]:
            button.draw(SCREEN)

        # Handle event
        for event in events_list:
            # Quit the game if the exit button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle the button click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if back_button.check_for_input(mouse_pos):
                    winner = dict()
                    eve_menu()

        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)


def bot_run(
    althea_type: GameTree,
    althea_value: int,
    althea_ap: int,
    beth_type: GameTree,
    beth_value: int,
    beth_ap: int
) -> None:
    """This function creates a background game thread"""

    # Create the bots
    althea = althea_type(Team.RED, althea_ap, althea_value)
    beth = beth_type(Team.BLACK, beth_ap, beth_value)

    # Set the variable
    turn, max_turn = 1, 200
    global is_end, force_end, winner

    # Start the game loop
    while turn <= max_turn:
        # If there is a force end signal, break the loop
        if force_end is True:
            break

        print("Turn: {}".format(turn))

        # [ALTHEA'S TURN]
        # Check whether Althea has been checkmated
        if althea.is_lost() is True:
            if althea.current_node.game_state.get_team_win() is Team.NONE:
                break
            winner[beth.team.name] = winner.get(beth.team.name, 0) + 1
            print("Checkmate! {} wins!\n".format(beth.team.name))
            is_end = True
            return

        # Move solving
        old_pos, new_pos = althea.process(moves_queue)
        beth.move_to_child_node_with_move(old_pos, new_pos)

        # Post process
        value_queue.append((althea.current_node.game_state.value, beth.current_node.game_state.value))
        gc.collect()

        # [END ALTHEA'S TURN]

        if force_end is True:
            break
        # [BETH'S TURN]
        # Check whether Beth has been checkmated
        if beth.is_lost() is True:
            if beth.current_node.game_state.get_team_win() is Team.NONE:
                break
            winner[althea.team.name] = winner.get(althea.team.name, 0) + 1
            print("Checkmate! {} wins!\n".format(althea.team.name))
            is_end = True
            return

        # Move solving
        old_pos, new_pos = beth.process(moves_queue)
        althea.move_to_child_node_with_move(old_pos, new_pos)

        # Post process
        value_queue.append((althea.current_node.game_state.value, beth.current_node.game_state.value))
        gc.collect()

        # [END BETH'S TURN]

        turn += 1

    # If the game loop is break then the game is considered draw
    winner["DRAW"] = winner.get("DRAW", 0) + 1
    is_end = True
    print("DRAW")


def simulation_screen(
    red_type: str,
    red_value: str,
    red_another_property: str,
    black_type: str,
    black_value: str,
    black_another_property: str,
    number_of_simulations: str
) -> None:
    """This function is the simulation screen"""

    def get_bot_full_type(bot_type, bot_property, bot_value):
        """This function is used to get the full name of the bot
        which is used for the result screen"""
        res = bot_type + ' '

        if (
            bot_type == 'Minimax'
            or bot_type == 'DyMinimax'
            or bot_type == 'DeMinimax'
            or bot_type == 'ExMinimax'
        ):
            res += 'Depth ' + bot_property + ' '
        elif bot_type == 'MCTS':
            res += 'Time allowed ' + bot_property + 's '

        res += 'Value ' + bot_value
        return res

    # Change the string to a proper type
    red_full_type = get_bot_full_type(red_type, red_another_property, red_value)
    black_full_type = get_bot_full_type(black_type, black_another_property, black_value)

    red_type, black_type = str_to_type(red_type), str_to_type(black_type)
    red_value, black_value = int(red_value), int(black_value)

    red_another_property = int(red_another_property)
    black_another_property = int(black_another_property)
    number_of_simulations = int(number_of_simulations)

    # Create ultilities
    pause_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(765, 450),
                          text_input="Pause", font=resources.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    skip_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(765, 550),
                         text_input="Skip", font=resources.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    # Expand the size of the screen
    SCREEN = pygame.display.set_mode((900, 660))
    MOVE_TIME = 0.5

    # Create necessary variables
    global is_end, force_end, winner
    winner = {"BLACK": 0, "DRAW": 0, "RED": 0}
    is_end, is_paused = True, False
    check_point = time()
    gamestate, move, bot_run_thread = None, None, None
    games_done_count = 0
    black_win, red_win, draw = 0, 0, 0

    start = time()  # Start the time counter

    # Start the game loop
    while True:
        # Get the current game status
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Handle events
        for event in events_list:
            # Quit the game if the exit button is clicked
            if event.type == pygame.QUIT:
                force_end = True
                pygame.quit()
                sys.exit()

            # Handle the button click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.check_for_input(mouse_pos):
                    is_paused = not is_paused
                elif skip_button.check_for_input(mouse_pos):
                    is_paused = False
                    force_end = True
                    is_end = True
                    bot_run_thread.join()
                    moves_queue.clear()
                    value_queue.clear()

        # If the game is not paused, then update the board
        if is_paused is False:
            # If the game is end
            if is_end is True and len(moves_queue) == 0:
                # Update the result
                black_win, red_win, draw = winner["BLACK"], winner["RED"], winner["DRAW"]
                games_done_count += 1

                # If the number of simulations is reached, break the loop
                if games_done_count > number_of_simulations:
                    bot_run_thread.join()
                    break

                # Reset the variables
                value_queue.clear()
                current_red_value, current_black_value = 0, 0
                is_end = False
                move = None
                gamestate = GameState.generate_initial_game_state()

                if bot_run_thread is not None:
                    bot_run_thread.join()

                bot_run_thread = threading.Thread(target=bot_run, args=(
                    red_type, red_value, red_another_property,
                    black_type, black_value, black_another_property
                ))
                bot_run_thread.start()

            # Try to make a move
            try:
                if time() - check_point > MOVE_TIME:
                    move = moves_queue.pop(0)
                    gamestate = gamestate.generate_game_state_with_move(move[0], move[1])[0]
                    current_red_value, current_black_value = value_queue.pop(0)

                    check_point = time()
            # If the bot hasn't generated a move yet, then pass
            except IndexError:
                pass

        # Clear the screen
        SCREEN.fill((241, 203, 157))

        # Draw here
        # .Game state
        draw_gamestate(gamestate)

        # .Chosen ring
        if move is not None:
            chosen_ring_img, draw_pos = resources.chosen_ring_sprite(move[0])
            SCREEN.blit(chosen_ring_img, draw_pos)

            chosen_ring_img, draw_pos = resources.chosen_ring_sprite(move[1])
            SCREEN.blit(chosen_ring_img, draw_pos)

        # .Button
        for button in [pause_button, skip_button]:
            button.draw(SCREEN)

        # .Text
        pygame.draw.rect(SCREEN, "#AB001B", pygame.Rect(658, 18, 208, 79))
        pygame.draw.rect(SCREEN, "#F6F5E0", pygame.Rect(662, 22, 200, 71))
        text = resources.get_font(25, 0).render("Black " + str(black_win), True, "Black")
        SCREEN.blit(text, (670, 30))

        text = resources.get_font(25, 0).render("Red " + str(red_win), True, "Red")
        SCREEN.blit(text, (790, 30))

        text = resources.get_font(25, 0).render("Draw " + str(draw), True, "#56000E")
        SCREEN.blit(text, (730, 60))

        pygame.draw.rect(SCREEN, "#AB001B", pygame.Rect(658, 110, 208, 109))
        pygame.draw.rect(SCREEN, "#F6F5E0", pygame.Rect(662, 114, 200, 101))

        text = resources.get_font(25, 0).render("Statistic", True, "#56000E")
        SCREEN.blit(text, (730, 118))

        text = resources.get_font(25, 0).render(
            "Black        " + str(round(float(current_black_value), 2)), True, "Black")
        SCREEN.blit(text, (670, 148))

        text = resources.get_font(25, 0).render(
            "Red          " + str(round(float(current_red_value), 2)), True, "Red")
        SCREEN.blit(text, (670, 178))

        pygame.draw.rect(SCREEN, "#AB001B", pygame.Rect(658, 240, 208, 92))
        pygame.draw.rect(SCREEN, "#F6F5E0", pygame.Rect(662, 244, 200, 84))

        # .Piece status
        piece_position = resources.get_piece_position(mouse_pos)
        if piece_position is not None:
            notation = gamestate.board[piece_position[0]][piece_position[1]]
            # If the mouse in on a piece, then draw that piece status
            if notation != "NN":
                if Team[notation[0]] is Team.RED:
                    number_of_team_piece = gamestate.number_of_red_pieces
                else:
                    number_of_team_piece = gamestate.number_of_black_pieces

                piece = Piece.create_instance(
                    piece_position, notation, gamestate.board,
                    gamestate.number_of_black_pieces + gamestate.number_of_red_pieces,
                    number_of_team_piece
                )

                text = pygame.font.SysFont(None, 26).render(
                    "Piece Type: " + piece._piece_type.capitalize(), True, "#56000E")
                SCREEN.blit(text, (670, 250))

                text = pygame.font.SysFont(None, 26).render(
                    "Piece Team: " + str(piece.team).capitalize(), True, "#56000E")
                SCREEN.blit(text, (670, 275))

                if piece.team is Team.RED:
                    text = pygame.font.SysFont(None, 26).render(
                        "Piece Value: " + str(round(piece.piece_value(red_value), 2)), True, "#56000E")
                else:
                    text = pygame.font.SysFont(None, 26).render(
                        "Piece Value: " + str(round(piece.piece_value(black_value), 2)), True, "#56000E")
                SCREEN.blit(text, (670, 300))

        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)

    # Post process
    print(winner)
    end = time()
    print("Total time: {} s\n".format(end - start))

    # Move to the result screen
    eve_result(red_full_type, black_full_type)


def eve_menu():
    # Create ultilites
    black_type = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        20, 290, 100, 30,
        pygame.font.SysFont(None, 25),
        "Type", ["Minimax", "MCTS", "DyMinimax", "DeMinimax", "ExMinimax"])

    black_value = DropDown(
        ["#000000", "#202020"],
        ["#404040", "#606060"],
        180, 290, 100, 30,
        pygame.font.SysFont(None, 25),
        "Pack", ["0", "1", "2"])

    red_type = DropDown(
        ["#DC1C13", "#EA4C46"],
        ["#F07470", "#F1959B"],
        350, 290, 100, 30,
        pygame.font.SysFont(None, 25),
        "Type", ["Minimax", "MCTS", "DyMinimax", "DeMinimax", "ExMinimax"])

    red_value = DropDown(
        ["#DC1C13", "#EA4C46"],
        ["#F07470", "#F1959B"],
        510, 290, 100, 30,
        pygame.font.SysFont(None, 25),
        "Pack", ["0", "1", "2"]
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

    # Start the game loop
    while True:
        # Get the current game status
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Draw main menu
        # .Background
        bg_img, bg_pos = resources.background()
        SCREEN.blit(bg_img, bg_pos)

        # Text
        menu_text = resources.get_font(70, 0).render("Bots select", True, "Black")
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

        # .Button
        for button in [start_button, quit_button, back_button]:
            button.draw(SCREEN)

        # .List
        for lst in [black_type, black_value, red_type, red_value]:
            selected_option = lst.update(events_list)
            if selected_option >= 0:
                lst.main = lst.options[selected_option]

            lst.draw(SCREEN)

        # .Input box
        for input_box in [num_box, black_another_property, red_another_property]:
            input_box.update()
            input_box.draw(SCREEN)

        # Handle events
        for event in events_list:
            # Quit the game if the exit button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle the button click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If all information is filled up, the simulation button is unlocked
                if start_button.check_for_input(mouse_pos):
                    if (
                        red_type.main == "Type" or black_type.main == "Type"
                        or red_value.main == "Pack" or black_value.main == "Pack"
                        or not num_box.text.isnumeric()
                        or not red_another_property.text.isnumeric()
                        or not black_another_property.text.isnumeric()
                    ):
                        continue
                    simulation_screen(
                        red_type.main, red_value.main, red_another_property.text,
                        black_type.main, black_value.main, black_another_property.text,
                        num_box.text
                    )
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if back_button.check_for_input(mouse_pos):
                    main_menu()

            for input_box in [num_box, black_another_property, red_another_property]:
                input_box.handle_event(event)

         # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)


def main_menu():
    """This function is the main menu screen"""

    # Create utilities
    pve_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(165, 250),
                        text_input="PvE", font=resources.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    eve_button = Button(image=pygame.image.load("resources/button/normal_rect.png"), pos=(495, 250),
                        text_input="EvE", font=resources.get_font(40, 0), base_color="#AB001B", hovering_color="Black")

    quit_button = Button(image=pygame.image.load("resources/button/small_rect.png"), pos=(330.5, 350),
                         text_input="QUIT", font=resources.get_font(30, 0), base_color="Black", hovering_color="#AB001B")

    # Start the game loop
    while True:
        # Get the current game status
        mouse_pos = pygame.mouse.get_pos()
        events_list = pygame.event.get()

        # Draw main menu
        # .Background
        bg_img, bg_pos = resources.background()
        SCREEN.blit(bg_img, bg_pos)

        # .Menu_text
        menu_text = resources.get_font(100, 0).render("Xiangqi", True, "Black")
        menu_rect = menu_text.get_rect(center=(330.5, 100))
        SCREEN.blit(menu_text, menu_rect)

        # .Button
        for button in [pve_button,  eve_button, quit_button]:
            button.draw(SCREEN)

        # Handle events
        for event in events_list:
            # Quit the game if the exit button is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle the button click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pve_button.check_for_input(mouse_pos):
                    pve_menu()
                if eve_button.check_for_input(mouse_pos):
                    eve_menu()
                if quit_button.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(REFRESH_RATE)

# [END MAIN FUNCTIONS]


if __name__ == "__main__":
    # Run the main menu when main.py is executed
    main_menu()
