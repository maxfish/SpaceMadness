#!/usr/bin/env python
import logging

from mgl2d.app import App
from mgl2d.graphics.post_processing_step import PostProcessingStep
from mgl2d.graphics.screen import Screen
from mgl2d.graphics.shader import Shader
from mgl2d.input.game_controller_manager import GameControllerManager

from game.world import World

logging.basicConfig(level=logging.INFO)

GAME_FPS = 50
GAME_FRAME_MS = 1000 / GAME_FPS

app = App()
screen = Screen(1280, 720, '!!!')
screen.print_info()

world = World(bounds=screen.viewport)
# world.set_stage(Stage2())


controllerManager = GameControllerManager()
controllerManager.load_joysticks_database('resources/gamecontrollerdb.txt')

# controller = controllerManager.grab_controller()

ppe = PostProcessingStep(screen.width, screen.height)
ppe.drawable.shader = Shader.from_files('resources/shaders/base.vert', 'resources/shaders/postprocessing_retro.frag')
screen.add_postprocessing_step(ppe)


def draw_frame(screen):
    world.draw(screen)


def update_frame(delta_ms):
    world.update(delta_ms / GAME_FRAME_MS)
    for p in world.players:
        p.handle_input()


app.run(screen, draw_frame, update_frame, fps=GAME_FPS)
