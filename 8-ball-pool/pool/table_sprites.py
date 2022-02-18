import numpy as np
import pygame

import config
import gamestate


class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(
            (2 * config.hole_radius, 2 * config.hole_radius))
        # color which will be ignored
        self.image.fill((200, 200, 200))
        self.image.set_colorkey((200, 200, 200))

        pygame.draw.circle(self.image, (0, 0, 0),
                           (config.hole_radius, config.hole_radius), config.hole_radius, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = np.array([x, y])


# this class holds properties of a table side line, but doesn't actually
# draw it
class TableSide():
    def __init__(self, line):
        self.line = np.array(line)
        self.middle = (self.line[0] + self.line[1]) / 2
        self.size = np.round(np.abs(self.line[0] - self.line[1]))
        self.length = np.hypot(*self.size)
        if np.count_nonzero(self.size) != 2:
            # line is perpendicular to y or x axis
            if self.size[0] == 0:
                self.size[0] += 1
            else:
                self.size[1] += 1


# draws the yellow part of the table
class TableColoring(pygame.sprite.Sprite):
    def __init__(self, table_size, color, table_points):
        pygame.sprite.Sprite.__init__(self)
        self.points = table_points
        self.image = pygame.Surface(table_size)
        self.image.fill(color)
        color_key = (200, 200, 200)
        self.image.set_colorkey(color_key)
        pygame.draw.polygon(self.image, color_key, table_points)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.font = config.get_default_font(config.ball_radius)
        # generates text at the bottom of the table
        self.target_ball_text = [
            self.font.render(
                '', #config.player1_target_text, 
                False, config.player1_cue_color
            ),
            self.font.render(
                '', #config.player2_target_text, 
                False, config.player2_cue_color
            )
        ]

    def redraw(self):
        self.image.fill(config.table_side_color)
        color_key = (200, 200, 200)
        self.image.set_colorkey(color_key)
        pygame.draw.polygon(self.image, color_key, self.points)

    def update(self, game_state):
        self.redraw()
        self.generate_top_left_label(game_state)

    def generate_top_left_label(self, game_state):
        # generates the top left label (which players turn is it and if he can move the ball)
        top_left_text = ""
        if game_state.can_move_white_ball:
            top_left_text += config.penalty_indication_text
        if game_state.current_player.value == 1:
            top_left_rendered_text = self.font.render(config.player1_turn_label + top_left_text,
                                                      False, config.player1_cue_color)
        else:
            top_left_rendered_text = self.font.render(config.player2_turn_label + top_left_text,
                                                      False, config.player2_cue_color)
        text_pos = [config.table_margin + config.hole_radius * 3,
                    config.table_margin - self.font.size(top_left_text)[1] / 2]
        self.image.blit(top_left_rendered_text, text_pos)
