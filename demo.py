#!/usr/bin/env python
import argparse
import logging

import sdl2
import sdl2.ext as sdl2ext
from mgl2d.app import App
from mgl2d.graphics.screen import Screen

from config import GAME_FPS, SCREEN_HEIGHT, SCREEN_WIDTH, PHYSICS_TIME_STEP, PHYSICS_NUM_VEL_ITERS, \
    PHYSICS_NUM_POS_ITERS
from demo.demoworld import DemoWorld
from demo.stage_demo import StageDemo

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--stage", help="stage to initiate the game with. Defaults to the default stage.py")
parser.add_argument("--width", default=SCREEN_WIDTH, type=int, help="screen width. Defaults to 1920")
parser.add_argument("--height", default=SCREEN_HEIGHT, type=int, help="screen height. Defaults to 1080.")
args = parser.parse_args()

app = App()
screen = Screen(args.width, args.height, 'Space Madness')
world = DemoWorld(bounds=screen.viewport, controllers=None)
world.set_stage(StageDemo(screen.width, screen.height))


def draw_line(surface, x1, y1, x2, y2):
    color = sdl2.ext.Color(255, 255, 255)
    sdl2.ext.line(surface, color, (x1, y1, x2, y2))


def draw_frame(screen):
    world.draw(screen)


def update_frame(delta_ms):
    for body in world.physics_to_delete:
        body.position = (-100, -100)
    world.physics_to_delete = []

    world.physicsWorld.ClearForces()
    world.update(delta_ms)
    world.physicsWorld.Step(PHYSICS_TIME_STEP, PHYSICS_NUM_VEL_ITERS, PHYSICS_NUM_POS_ITERS)


app.run(screen, draw_frame, update_frame, fps=GAME_FPS)
