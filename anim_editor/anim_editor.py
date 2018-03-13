#!/usr/bin/env python3
import json
import sys
from time import sleep

from pygame.math import Vector2

import os
import pygame
from collections import OrderedDict
from lib.frames_store import FramesStore
from lib.gamepad import GamePad
from lib.gfx import Gfx
from lib.sprite import Sprite
from lib.utils import Utils

FPS = 30
SURFACE_WIDTH = 500
SURFACE_HEIGHT = 500
FULL_SCREEN = False

BG_COLOR = (20, 40, 40)
HIGHLIGHT_BG_COLOR = (50, 0, 0)
VALUE_COLOR = (255, 255, 255)
KEY_COLOR = (200, 200, 200)

SPRITE_Y = 300

SPRITES_PATH = '../resources/sprites'
SPRITES_JSON = 'sprites.json'

# ==== set up the display
screen_args = []
SCREEN_WIDTH = SURFACE_WIDTH * 2
SCREEN_HEIGHT = SURFACE_HEIGHT * 2

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), *screen_args)
render_surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT)).convert()
clock = pygame.time.Clock()

# =================================

def load_available_sprite_names():
    characters = []
    characters_list = os.listdir(SPRITES_PATH)
    for c in characters_list:
        if not c.startswith('.'):
            characters.append(c)
    return characters


def change_selected_sprite(character_index, animation_index=0):
    sprite_name = available_sprites_names[character_index]
    file_name = SPRITES_PATH + '/' + sprite_name + '/' + SPRITES_JSON
    time_changed = os.stat(file_name).st_mtime
    framesstore = FramesStore()
    framesstore.load(SPRITES_PATH + '/' + sprite_name + '/', SPRITES_JSON)

    sprite = Sprite(framesstore)
    sprite.x = SURFACE_WIDTH / 2
    sprite.y = SPRITE_Y
    anim_name = list(framesstore.animations.keys())[animation_index]
    sprite.play_animation(anim_name, FramesStore.FLAG_LOOP_ANIMATION)
    return {
        'name': sprite_name,
        'sprite': sprite,
        'framesstore': framesstore,
        'file_name': file_name,
        'time_changed': time_changed
    }


def change_animation(current_character, animation_index):
    sprite = current_character['sprite']
    sprite.x = SURFACE_WIDTH / 2
    sprite.y = SPRITE_Y
    anim_name = list(current_character['framesstore'].animations.keys())[animation_index]
    sprite.play_animation(anim_name, FramesStore.FLAG_LOOP_ANIMATION)

    return current_character


def draw_values(sprite):
    text_lines = []
    text_lines.append(('anchor', [('x', sprite.frame.anchor.x), ('y', sprite.frame.anchor.y), ]))
    text_lines.append(('hit-box', [
        ('x', sprite.frame.hit_box.x),
        ('y', sprite.frame.hit_box.y),
        ('w', sprite.frame.hit_box.w),
        ('h', sprite.frame.hit_box.h),
    ]))
    text_lines.append(('attack-box', [
        ('x', sprite.frame.attack_box.x),
        ('y', sprite.frame.attack_box.y),
        ('w', sprite.frame.attack_box.w),
        ('h', sprite.frame.attack_box.h),
    ]))

    text_lines.append(('delay', [('f', sprite.animation.frames[sprite.animation_frame_index].delay)]))

    start_offset_x = 60
    start_offset_y = SPRITE_Y + 10
    font_size = 14
    value_color = VALUE_COLOR
    fg_color = KEY_COLOR
    bg_color = BG_COLOR

    def draw_key_value_text(text_key, text_value, x, y):
        text_key_rect = Gfx.text_rect(text_key, font_size)
        Gfx.render_text(render_surface, str(text_key), x - text_key_rect.w, y, size=font_size, color=fg_color,
                        bg_color=bg_color)
        Gfx.render_text(render_surface, str(text_value), x, y, size=font_size, color=value_color, bg_color=bg_color)

    for line in text_lines:
        name = line[0]
        value_list = line[1]

        if mode == name:
            pygame.draw.rect(render_surface, HIGHLIGHT_BG_COLOR, (0, start_offset_y - 2, SURFACE_WIDTH, font_size + 1))
            bg_color = HIGHLIGHT_BG_COLOR
        else:
            bg_color = BG_COLOR

        text_rect = Gfx.text_rect(name, 14)
        Gfx.render_text(render_surface, name, start_offset_x - text_rect.w, start_offset_y, size=14, color=fg_color,
                        bg_color=bg_color)
        offset_x = start_offset_x + 20
        if value_list:
            for (key, value) in value_list:
                draw_key_value_text(key + ': ', value, offset_x, start_offset_y)
                offset_x += 40

        start_offset_y += 15


def draw_ui(sprite):
    render_surface.fill(BG_COLOR)
    pygame.draw.line(render_surface, (70, 70, 70), (SURFACE_WIDTH / 2, 0), (SURFACE_WIDTH / 2, SPRITE_Y), 1)
    pygame.draw.line(render_surface, (255, 255, 255), (0, SPRITE_Y), (SURFACE_WIDTH, SPRITE_Y), 1)

    Gfx.render_text(render_surface, current_sprite_data['name'], 4, 3, size=20, bg_color=BG_COLOR)
    Gfx.render_text(render_surface, sprite.animation.name, 4, 21, size=14, bg_color=BG_COLOR)
    Gfx.render_text(render_surface, sprite.frame.name, 4, 32, size=14, bg_color=BG_COLOR)
    Gfx.render_text(render_surface, "%i / %i" % (sprite.animation_frame_index + 1, len(sprite.animation.frames)), 4, 43,
                    size=14, bg_color=BG_COLOR)
    current_fps = 'PAUSED' if paused else '%.2fFPS' % (FPS * speed)
    Gfx.render_text(render_surface, current_fps, SURFACE_WIDTH - 45, 4, size=14, bg_color=BG_COLOR)
    draw_values(sprite)
    Gfx.render_centered_text(render_surface, mode, center_x=SURFACE_WIDTH / 2, center_y=10, size=18, color=(0, 120, 0),
                             bg_color=BG_COLOR)

    mode_instructions = {
        'view': '',
        'save': 'A: save',
        'anchor': 'LS or ARROWS: move',
        'hit-box': 'LS or ARROWS: move · RS: resize · X: remove',
        'attack-box': 'LS or ARROWS: move · RS: resize · X: remove',
        'delay': 'ARROWS: change value',
    }

    font_size = 14
    y = SURFACE_HEIGHT - font_size
    for text in [
        'GUIDE: mode · BACK: next sprite · START: next animation',
        'Y: pause · LB: prev frame · RB: next frame · B: change fps ',
        mode_instructions[mode],
    ]:
        Gfx.render_text(render_surface, text, 8, y, size=font_size, color=(80, 80, 80), bg_color=BG_COLOR)
        y -= font_size


def dictionary_from_sprites(frames_store_data):
    data = frames_store_data.to_dictionary()
    data['frames'] = OrderedDict(sorted(data['frames'].items(), key=lambda x: x[0]))
    data['animations'] = OrderedDict(sorted(data['animations'].items(), key=lambda x: x[0]))
    return data


def save_sprites(dictionary_data):
    sprite_name = current_sprite_data['name']
    file_name = SPRITES_PATH + '/' + sprite_name + '/' + SPRITES_JSON
    text_file = open(file_name, 'w')
    text_file.write(json.dumps(dictionary_data, sort_keys=False, indent=4, separators=(',', ': ')))
    text_file.close()


# =================================

available_sprites_names = load_available_sprite_names()
current_sprite_index = 0
current_animation_index = 0
current_sprite_data = change_selected_sprite(current_sprite_index)

Sprite.DEBUG = True

current_speed_index = 4
paused = False
MODES = ['view', 'anchor', 'hit-box', 'attack-box', 'delay', 'save']
mode = MODES[0]
gamepad = None

shouldQuit = False
while not shouldQuit:
    # Quit event
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            shouldQuit = True  # Flag that we are done so we exit this loop
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        shouldQuit = True

    if not gamepad:
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            gamepad = GamePad(pygame.joystick.Joystick(0))
        else:
            Gfx.render_centered_text(render_surface, 'Connect a joystick!', center_x=SURFACE_WIDTH / 2, center_y=20,
                                     size=22, color=(200, 0, 0), bg_color=(0, 0, 0))
            pygame.transform.scale(render_surface, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
            pygame.display.update()
            pygame.joystick.quit()
            sleep(1)
            continue

    gamepad.update()
    speed = 0 if paused else [0.01, 0.05, 0.1, 0.25, 0.5, 0.7, 1][current_speed_index]

    # Check if the current player's file has changed
    # if os.stat(current_character['file_name']).st_mtime > current_character['time_changed']:
    #     current_character = change_character(current_character_index, current_animation_index)

    # Anim speed control
    if gamepad.is_button_pressed('B'):
        current_speed_index = Utils.clamp_mod(current_speed_index - 1, 7)
    elif gamepad.is_button_pressed('Y'):
        paused = not paused
    elif paused:
        if gamepad.is_button_pressed('LB'):
            current_sprite_data['sprite'].previous_animation_frame()
        elif gamepad.is_button_pressed('RB'):
            current_sprite_data['sprite'].next_animation_frame()

    # Change character / anim
    if gamepad.is_button_pressed('BACK'):
        current_sprite_index += 1
        current_sprite_index = Utils.clamp_mod(current_sprite_index, len(available_sprites_names))
        current_sprite_data = change_selected_sprite(current_sprite_index)
    elif gamepad.is_button_pressed('START'):
        current_animation_index += 1
        current_animation_index = Utils.clamp_mod(current_animation_index,
                                                  len(current_sprite_data['framesstore'].get_animations()))
        current_sprite_data = change_animation(current_sprite_data, current_animation_index)

    current_sprite = current_sprite_data['sprite']

    # If the sprite doesn't have a hit-box or a attack-box, let's create them
    if current_sprite.frame.hit_box is None:
        current_sprite.frame.hit_box = pygame.Rect(0, 0, 0, 0)
    if current_sprite.frame.attack_box is None:
        current_sprite.frame.attack_box = pygame.Rect(0, 0, 0, 0)

    if gamepad.is_button_pressed('GUIDE'):
        mode = MODES[Utils.clamp_mod(MODES.index(mode) + 1, len(MODES))]

    dpad = Vector2(0, 0)
    if gamepad.is_button_pressed('LEFT') or gamepad.get_axis_digital_value('LS_H') == -1:
        dpad.x = 1
    elif gamepad.is_button_pressed('RIGHT') or gamepad.get_axis_digital_value('LS_H') == 1:
        dpad.x = -1
    if gamepad.is_button_pressed('UP') or gamepad.get_axis_digital_value('LS_V') == -1:
        dpad.y = 1
    elif gamepad.is_button_pressed('DOWN') or gamepad.get_axis_digital_value('LS_V') == 1:
        dpad.y = -1

    if mode == 'anchor':
        # Move current frame's anchor
        current_sprite.frame.anchor += dpad
    elif mode == 'hit-box':
        hit_box = current_sprite.frame.hit_box
        if gamepad.is_button_pressed('X'):
            current_sprite.frame.hit_box = pygame.Rect(0, 0, 0, 0)
        else:
            current_sprite.frame.hit_box.x -= dpad.x
            current_sprite.frame.hit_box.y -= dpad.y
            current_sprite.frame.hit_box.w += gamepad.get_axis_digital_value('RS_H')
            current_sprite.frame.hit_box.h += gamepad.get_axis_digital_value('RS_V')
    elif mode == 'attack-box':
        if gamepad.is_button_pressed('X'):
            current_sprite.frame.attack_box = pygame.Rect(0, 0, 0, 0)
        else:
            attack_box = current_sprite.frame.attack_box
            attack_box.x -= dpad.x
            attack_box.y -= dpad.y
            attack_box.w += gamepad.get_axis_digital_value('RS_H')
            attack_box.h += gamepad.get_axis_digital_value('RS_V')
    elif mode == 'delay':
        delay = current_sprite.animation.frames[current_sprite.animation_frame_index].delay
        delay -= dpad.x * 10
        delay += dpad.y
        current_sprite.animation.frames[current_sprite.animation_frame_index].delay = Utils.clamp_mod(delay, 100)
    elif mode == 'save':
        if gamepad.is_button_pressed('A'):
            sprite_dictionary_data = dictionary_from_sprites(current_sprite_data['framesstore'])
            save_sprites(sprite_dictionary_data)

    draw_ui(current_sprite)

    current_sprite.update(speed)
    current_sprite.draw(render_surface)

    # update the display
    pygame.transform.scale(render_surface, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    pygame.display.update()
    clock.tick(FPS)

# Close the game
pygame.quit()
sys.exit()
