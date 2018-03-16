#!/usr/bin/env python
import argparse
import logging

import sdl2
import sdl2.ext as sdl2ext
from mgl2d.app import App
from mgl2d.graphics.screen import Screen
from mgl2d.input.game_controller_manager import GameControllerManager

from config import GAME_FPS, GAME_FRAME_MS, SCREEN_HEIGHT, SCREEN_WIDTH
from demo.demoworld import DemoWorld
from demo.stage_demo import StageDemo
from game.stages.stage_sky import StageSky
from game.entities.turret import TurretStage
from game.world import World

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--stage", help="stage to initiate the game with. Defaults to the default stage.py")
parser.add_argument("--width", default=SCREEN_WIDTH, type=int, help="screen width. Defaults to 1920")
parser.add_argument("--height", default=SCREEN_HEIGHT, type=int, help="screen height. Defaults to 1080.")
args = parser.parse_args()

app = App()

screen = Screen(args.width, args.height, 'Space Madness')
# sdl2.SDL_SetWindowFullscreen(screen._window, True)
screen.print_info()

controllerManager = GameControllerManager()
controllerManager.load_joysticks_database('resources/gamecontrollerdb.txt')
# debug: add keyboard
num_joysticks = max(controllerManager.num_joysticks, 1)
controllers = []


world = DemoWorld(bounds=screen.viewport, controllers=controllers)

world.set_stage(StageDemo(screen.width, screen.height))

# ppe = PostProcessingStep(screen.width, screen.height)
# ppe.drawable.shader = Shader.from_files('resources/shaders/base.vert', 'resources/shaders/postprocessing_retro.frag')
# screen.add_postprocessing_step(ppe)


timeStep = (1.0 / GAME_FPS) *4
vel_iters, pos_iters = 6, 2

global prev_deletion
global deletion_freq

def draw_line(surface, x1, y1, x2, y2):
    color = sdl2.ext.Color(255, 255, 255)
    sdl2.ext.line(surface, color, (x1, y1, x2, y2))

def draw_frame(screen):
    world.draw(screen)

def update_frame(delta_ms):
    for body in world.physics_to_delete:
        body.position = (-100, -100)
        #world.physicsWorld.DestroyBody(body)
    world.physics_to_delete = []

    world.physicsWorld.ClearForces()
    world.update(delta_ms / GAME_FRAME_MS)
    for p in world.players:
        p.handle_input()
    world.physicsWorld.Step(timeStep, vel_iters, pos_iters)

    # world.update(0)


app.run(screen, draw_frame, update_frame, fps=GAME_FPS)
