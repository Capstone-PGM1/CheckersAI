import pygame as pg
from tiles import *

CAPTION = "Lyra'a Checkers"
SCREEN_START_SIZE = (600, 450)

# Circle sizes
intro_circle_radius = 70
intro_outline_radius = 80
settings_circle_radius = 25
settings_outline_radius = 30

# Board
tile_size = 40

""" ********
___COLORS___
******** """
black_color = (0, 0, 0)
black_outline = (50, 47, 47)
red_color = (255, 0, 0)
red_outline = (181, 13, 13)
gold_color = (233, 218, 10)
gold_outline = (216, 171, 23)
tan_color = (242, 221, 179)
tan_highlight = (242, 235, 222)
light_green = (83, 249, 88)


def draw_red_circle(x, y, circle_radius, outline_radius, window: pg.Surface):
    pg.draw.circle(window, red_outline, (x, y), outline_radius)
    pg.draw.circle(window, red_color, (x, y), circle_radius, 0)


def draw_black_circle(x, y, circle_radius, outline_radius, window: pg.Surface):
    pg.draw.circle(window, black_outline, (x, y), outline_radius)
    pg.draw.circle(window, black_color, (x, y), circle_radius)


def draw_circle(x, y, color, outline_color, circle_radius, outline_radius, window: pg.Surface):
    pg.draw.circle(window, outline_color, (x, y), outline_radius)
    pg.draw.circle(window, color, (x, y), circle_radius)


def render_text(font_size, message, color):
    myfont = pg.font.SysFont('Arial', font_size)
    textsurface = myfont.render(message, False, color)
    return textsurface, textsurface.get_rect()

def render_centered_text(font_size, message, color, top_left_x, top_left_y, width, height, image):
    surf, rect = render_text(font_size, message, color)
    rect.center = ((top_left_x + (width / 2)), top_left_y + (height / 2))
    image.blit(surf, rect)

def render_centered_text_with_background(font_size, message, color, top_left_x, top_left_y, width, height, image, background):
    pg.draw.rect(image, background, [top_left_x, top_left_y, width, height])
    render_centered_text(font_size, message, color, top_left_x, top_left_y, width, height, image)

def load_grey_tiles(window, lower1, upper1, lower2, upper2, n):
    for i in range(n):
        for x in range(lower1, upper1, tile_size):
            for y in range(lower2, upper2 , tile_size):
                window.blit(Tiles.greyTile, (x, y))
                pg.draw.rect(window, black_color, (x, y, tile_size, tile_size), 1)
            lower1 += 40
            upper1 += 40
            lower2 += 40
            upper2 += 40


def load_white_tiles(window, lower1, upper1, lower2, upper2, n):
    for i in range(n):
        for x in range(lower1, upper1, tile_size):
            for y in range(lower2, upper2, tile_size):
                window.blit(Tiles.whiteTile, (x, y))
                pg.draw.rect(window, black_color, (x, y, tile_size, tile_size), 1)
            lower1 += 40
            upper1 += 40
            lower2 += 40
            upper2 += 40


def load_chatbox(window, gamestate=1):
    if gamestate == 1:
        for x in range(437, 547, tile_size):
            for y in range(140, 315, tile_size):
                window.blit(Tiles.tanTile, (x, y))
            pg.draw.rect(window, (54, 32, 3), [437, 290, 120, 50], 3)
        else:
            return



#  MOVE IT TO SCREEN CONTROL METHOD
def check_win(game, window):
    if game.is_game_over():
        if game.is_draw():
            print("The game is a draw.")
        else:
            winningPlayer = 'red' if game.is_win() == 0 else 'black'
            # if (winningPlayer == 'red'):
                # window.blit(Wood, (0, 0))
                # loadWinPage(1)
            # else:
                # window.blit(Wood, (0, 0))
                # loadWinPage(0)
        return True
    return False