import pygame as pg
from tiles import *
import os
from pygame_textinput import *
import time
import pygame.gfxdraw

CAPTION = "Lyra's Checkers"
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
brown_color = (91, 63, 27)
white_color = (255, 255, 255)

modified_red_outline = (181, 13, 113)
modified_red_color = (255, 0, 100)
modified_black_outline = (50, 47, 100)
modified_black_color = (0, 0, 50)
modified_gold_color = (233, 218, 110)
modified_gold_outline = (216, 171, 123)

is_mac = os.name == 'java'

def draw_red_circle(x, y, circle_radius, outline_radius, window: pg.Surface):
    if not is_mac:
        pg.gfxdraw.aacircle(window, x, y, outline_radius, modified_red_outline)
        pg.gfxdraw.filled_circle(window, x, y, outline_radius, red_outline)
        pg.gfxdraw.aacircle(window, x, y, circle_radius, modified_red_color)
        pg.gfxdraw.filled_circle(window, x, y, circle_radius, red_color)
    else:
        pg.gfxdraw.aacircle(window, x, y, outline_radius, red_outline)
        pg.gfxdraw.filled_circle(window, x, y, outline_radius, red_outline)
        pg.gfxdraw.aacircle(window, x, y, circle_radius, red_color)
        pg.gfxdraw.filled_circle(window, x, y, circle_radius, red_color)
    # pg.draw.circle(window, red_outline, (x, y), outline_radius)
    # pg.draw.circle(window, red_color, (x, y), circle_radius, 0)

def select_red_circle(x, y, circle_radius, outline_radius, window: pg.Surface):
    pg.draw.circle(window, light_green, (x, y), outline_radius + 5, 10)

def draw_black_circle(x, y, circle_radius, outline_radius, window: pg.Surface):
    if is_mac:
        pg.gfxdraw.aacircle(window, x, y, outline_radius, black_outline)
        pg.gfxdraw.filled_circle(window, x, y, outline_radius, black_outline)
        pg.gfxdraw.aacircle(window, x, y, circle_radius, black_color)
        pg.gfxdraw.filled_circle(window, x, y, circle_radius, black_color)
    else:
        pg.gfxdraw.aacircle(window, x, y, outline_radius, modified_black_outline)
        pg.gfxdraw.filled_circle(window, x, y, outline_radius, black_outline)
        pg.gfxdraw.aacircle(window, x, y, circle_radius, modified_black_color)
        pg.gfxdraw.filled_circle(window, x, y, circle_radius, black_color)

    # pg.draw.circle(window, black_outline, (x, y), outline_radius)
    # pg.draw.circle(window, black_color, (x, y), circle_radius)

def select_black_circle(x, y, circle_radius, outline_radius, window: pg.Surface):
    pg.draw.circle(window, light_green, (x, y), outline_radius + 5, 10)

def draw_circle(x, y, color, outline_color, circle_radius, outline_radius, window: pg.Surface):
    if is_mac:
        pg.gfxdraw.aacircle(window, x, y, outline_radius, outline_color)
        pg.gfxdraw.filled_circle(window, x, y, outline_radius, outline_color)
        pg.gfxdraw.aacircle(window, x, y, circle_radius, color)
        pg.gfxdraw.filled_circle(window, x, y, circle_radius, color)
    else:
        if color == gold_color: #gold
            pg.gfxdraw.aacircle(window, x, y, outline_radius, modified_gold_outline)
            pg.gfxdraw.filled_circle(window, x, y, outline_radius, outline_color)
            pg.gfxdraw.aacircle(window, x, y, circle_radius, modified_gold_color)
            pg.gfxdraw.filled_circle(window, x, y, circle_radius, color)
        elif color == red_color: # red
            pg.gfxdraw.aacircle(window, x, y, outline_radius, modified_red_outline)
            pg.gfxdraw.filled_circle(window, x, y, outline_radius, outline_color)
            pg.gfxdraw.aacircle(window, x, y, circle_radius, modified_red_color)
            pg.gfxdraw.filled_circle(window, x, y, circle_radius, color)
        else: # black
            pg.gfxdraw.aacircle(window, x, y, outline_radius, modified_black_outline)
            pg.gfxdraw.filled_circle(window, x, y, outline_radius, outline_color)
            pg.gfxdraw.aacircle(window, x, y, circle_radius, modified_black_color)
            pg.gfxdraw.filled_circle(window, x, y, circle_radius, color)
    # pg.draw.circle(window, outline_color, (x, y), outline_radius)
    # pg.draw.circle(window, color, (x, y), circle_radius)

def border(window):
    for x in range(0, 10, 10):
        for y in range(0, 900, 10):
            window.blit(Tiles.blackTile, (x, y))
    for x in range(590, 600, 10):
        for y in range(0, 900, 10):
            window.blit(Tiles.blackTile, (x, y))

    for x in range(0, 620, 10):
        for y in range(0, 10, 10):
            window.blit(Tiles.blackTile, (x, y))

    for x in range(0, 620, 10):
        for y in range(440, 450, 10):
            window.blit(Tiles.blackTile, (x, y))

def render_text(font_size, message, color):
    scale = 1 if is_mac else 0.8
    # Copyright (c) 2010-2013 by tyPoland Lukasz Dziedzic with Reserved Font Name "Carlito".
    myfont = pg.font.Font("Carlito-BoldItalic.ttf", int(font_size * scale))
    textsurface = myfont.render(message, True, color)
    return textsurface, textsurface.get_rect()

def render_centered_text(font_size, message, color, top_left_x, top_left_y, width, height, image):
    surf, rect = render_text(font_size, message, color)
    rect.center = ((top_left_x + (width / 2)), top_left_y + (height / 2))
    image.blit(surf, rect)

def render_centered_text_with_background(font_size, message, color, top_left_x, top_left_y, width, height, image, background):
    pg.draw.rect(image, background, [top_left_x, top_left_y, width, height])
    pg.draw.rect(image, brown_color, [top_left_x, top_left_y, width, height], 2)
    render_centered_text(font_size, message, color, top_left_x, top_left_y, width, height, image)

def render_centered_text_with_surface(surface, top_left_x, top_left_y, width, height, image, background):
    pg.draw.rect(image, background, [top_left_x, top_left_y, width, height])
    pg.draw.rect(image, brown_color, [top_left_x, top_left_y, width, height], 2)
    rect = surface.get_rect()
    rect.center = ((top_left_x + (width / 2)), top_left_y + (height / 2))
    image.blit(surface, rect)

def load_chatbox(window, messages, scroll, textinput, cursor_position):
    for x in range(437, 547, tile_size):
        for y in range(140, 315, tile_size):
            window.blit(Tiles.tanTile, (x, y))
        pg.draw.rect(window, (54, 32, 3), [437, 290, 120, 50], 3)

    text = wrap_text('\n'.join(messages), 15)
    new_scroll =  drawText(window, text, black_color, [440, 140, 120, 150], scroll)

    if textinput:
        message = wrap_text(textinput, 15)
        cursor = get_cursor_position(message, cursor_position)
        drawText(window, message, black_color, [440, 290, 120, 50], 0, num_lines = 3, cursor_position = cursor)
    return new_scroll

def get_cursor_position(message, cursor_position):
    index = 0
    length_so_far = 0
    for line in message:
        cursor_location_in_line = cursor_position - length_so_far
        length_so_far += len(line)
        if length_so_far >= cursor_position:
            return index, cursor_location_in_line
        index += 1
    return (len(message) - 1, cursor_position - len(''.join(message[:-1])))


# Modified wrap_text from https://github.com/ColdrickSotK/yamlui/blob/master/yamlui/util.py#L82-L143
def wrap_text(text, num_chars):
    text_lines = text.replace('\t', '    ').split('\n')

    wrapped_lines = []
    for line in text_lines:
        line = line.rstrip() + ' '
        if line == ' ':
            wrapped_lines.append(line)
            continue

        # Get the leftmost space ignoring leading whitespace
        start = len(line) - len(line.lstrip())
        start = line.index(' ', start)
        while start + 1 < len(line):
            # Get the next potential splitting point
            next = line.index(' ', start + 1)
            if next <= num_chars:
                start = next
            else:
                wrapped_lines.append(line[:start])
                line = line[start+1:]
                start = line.index(' ')
        line = line[:-1]
        if line:
            while line:
                wrapped_lines.append(line[:num_chars])
                line = line[num_chars:]
    return wrapped_lines

# modified drawText from https://www.reddit.com/r/pygame/comments/5lhp28/how_do_i_get_mouse_wheel_events/
# draw some text into an area of a surface
def drawText(window, text, color, rectangle, scroll, button = None, height = None, num_lines = 8, onClickButton = None, ids = None, cursor_position = None):
    y = rectangle[1]
    lineSpacing = 2
    myfont = pg.font.SysFont('Arial', 20)
    # get the height of the font
    fontHeight = height if height else myfont.size("Tg")[1]

    # get scroll. don't let scroll get too big.
    if scroll > 0:
        scroll = 0
    elif abs(scroll) > len(text):
        scroll = len(text) * -1
    begin = max(scroll + len(text) - num_lines, 0)
    end = max(scroll + len(text), num_lines)
    for i in range(begin, min(end, len(text))):
        if button:
            button(text[i], rectangle[0], y, 180, 30, tan_color, tan_highlight, lambda : onClickButton(ids[i], text[i]))
        else:
            image = myfont.render(text[i], True, color)
            window.blit(image, (rectangle[0], y))
            if cursor_position and i == cursor_position[0] and int(round(time.time()*1000.0)) % 1000 > 500:
                cursor_y_pos = myfont.size(text[i][:cursor_position[1]])[0]
                image = myfont.render("|", True, color)
                window.blit(image, (rectangle[0] + cursor_y_pos, y))
        y += fontHeight + lineSpacing
    return scroll
