import pygame

import collisions
import event
import gamestate
import graphics
import config

import time

game = gamestate.GameState()
game.start_pool()
events = event.events()
i = 0

start_time = 0
end_time = 0
avg_time = 0
hits = 0

print(f"fps_limit: {config.fps_limit}")

while not (events["closed"] or game.is_game_over or events["quit_to_main_menu"]):
    events = event.events()
    collisions.resolve_all_collisions(game.balls, game.holes, game.table_sides)

    if (i % 100 == 0):
        game.redraw_all(update=True) 
    else:
        game.redraw_all(update=False)

    i += 1

    if (not game.all_not_moving()):
        if (start_time == 0):
            start_time = time.time()

    if (game.all_not_moving()):
        if (start_time != 0):
            end_time = time.time()
            print(end_time-start_time)
            hits += 1
            avg_time += end_time - start_time
            start_time = 0
            end_time = 0

    
    
    if game.all_not_moving():
        game.check_pool_rules()
        game.cue.make_visible(game.current_player)
        while not (
            (events["closed"] or events["quit_to_main_menu"]) or game.is_game_over) and game.all_not_moving():
            game.redraw_all()
            events = event.events()
            if game.cue.is_clicked(events):
                game.cue.cue_is_active(game, events)
            elif game.can_move_white_ball and game.white_ball.is_clicked(events):
                game.white_ball.is_active(game, game.is_behind_line_break())

print(f"Average time per hit:\t{avg_time / hits}") # Average time per hit:   3.115713675816854

pygame.quit()


# ---------------------------ORIGINAL---------------------------

# was_closed = False
# while not was_closed:
#     game = gamestate.GameState()
#     button_pressed = graphics.draw_main_menu(game)

#     if button_pressed == config.play_game_button:
#         game.start_pool()
#         events = event.events()
#         while not (events["closed"] or game.is_game_over or events["quit_to_main_menu"]):
#             events = event.events()
#             collisions.resolve_all_collisions(game.balls, game.holes, game.table_sides)
#             game.redraw_all()

#             if game.all_not_moving():
#                 game.check_pool_rules()
#                 game.cue.make_visible(game.current_player)
#                 while not (
#                     (events["closed"] or events["quit_to_main_menu"]) or game.is_game_over) and game.all_not_moving():
#                     game.redraw_all()
#                     events = event.events()
#                     if game.cue.is_clicked(events):
#                         game.cue.cue_is_active(game, events)
#                     elif game.can_move_white_ball and game.white_ball.is_clicked(events):
#                         game.white_ball.is_active(game, game.is_behind_line_break())
#         was_closed = events["closed"]

#     if button_pressed == config.exit_button:
#         was_closed = True

# pygame.quit()