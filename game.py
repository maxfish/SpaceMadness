#!/usr/bin/env python
import argparse
import logging

from mgl2d.app import App
from mgl2d.graphics.screen import Screen
from mgl2d.input.game_controller_manager import GameControllerManager

from config import GAME_FPS, GAME_FRAME_MS, SCREEN_HEIGHT, SCREEN_WIDTH, PHYSICS_TIME_STEP, PHYSICS_NUM_POS_ITERS, \
    PHYSICS_NUM_VEL_ITERS
from game.stages.stage_sky import StageSky
from game.world import World

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--stage", help="stage to initiate the game with. Defaults to the default stage.py")
parser.add_argument("--width", default=SCREEN_WIDTH, type=int, help="screen width. Defaults to 1920")
parser.add_argument("--height", default=SCREEN_HEIGHT, type=int, help="screen height. Defaults to 1080.")
parser.add_argument("--fullscreen", default=False, type=bool, help="Do fullscreen, baby!")
args = parser.parse_args()

app = App()

controllerManager = GameControllerManager()
controllerManager.load_joysticks_database('resources/gamecontrollerdb.txt')
# debug: add keyboard
num_joysticks = max(controllerManager.num_joysticks, 1)
controllers = [
    controllerManager.grab_controller()
    for n in range(num_joysticks)
]

screen = Screen(args.width, args.height, 'Space Madness')
if args.fullscreen:
    screen.full_screen = True
screen.print_info()

world = World(
    bounds=screen.viewport,
    controllers=controllers,
    stage=StageSky(screen.width, screen.height)
)


def draw_frame(screen):
    world.draw(screen)


def update_frame(delta_ms):
    world.bullet_mgr.recycle_all()

    world.physicsWorld.ClearForces()
    world.update(delta_ms / GAME_FRAME_MS)
    for p in world.players:
        p.handle_input()
    world.physicsWorld.Step(PHYSICS_TIME_STEP, PHYSICS_NUM_VEL_ITERS, PHYSICS_NUM_POS_ITERS)


app.run(screen, draw_frame, update_frame, fps=GAME_FPS)
