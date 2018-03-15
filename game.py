#!/usr/bin/env python
import logging

from mgl2d.app import App
from mgl2d.graphics.post_processing_step import PostProcessingStep
from mgl2d.graphics.screen import Screen
from mgl2d.graphics.shader import Shader
from mgl2d.input.game_controller_manager import GameControllerManager

from game.stage_1 import Stage1
from game.world import World

from Box2D import (b2PolygonShape, b2World)

logging.basicConfig(level=logging.INFO)

GAME_FPS = 50
GAME_FRAME_MS = 1000 / GAME_FPS

app = App()
screen = Screen(1920, 1080, '!!!')
screen.print_info()

world = World(bounds=screen.viewport)
world.set_stage(Stage1())


controllerManager = GameControllerManager()
controllerManager.load_joysticks_database('resources/gamecontrollerdb.txt')

# controller = controllerManager.grab_controller()

# ppe = PostProcessingStep(screen.width, screen.height)
# ppe.drawable.shader = Shader.from_files('resources/shaders/base.vert', 'resources/shaders/postprocessing_retro.frag')
# screen.add_postprocessing_step(ppe)

physicsWorld = b2World()  # default gravity is (0,-10) and doSleep is True
groundBody = physicsWorld.CreateStaticBody(position=(0, -10),
                                    shapes=b2PolygonShape(box=(50, 10)),
                                    )

# Create a dynamic body at (0, 4)
body = physicsWorld.CreateDynamicBody(position=(0, 4))

# And add a box fixture onto it (with a nonzero density, so it will move)
box = body.CreatePolygonFixture(box=(1, 1), density=1, friction=0.3)

timeStep = 1.0 / GAME_FPS
vel_iters, pos_iters = 6, 2


def draw_frame(screen):
    world.draw(screen)

def update_frame(delta_ms):
    # world.update(delta_ms / GAME_FRAME_MS)

    physicsWorld.Step(timeStep, vel_iters, pos_iters)
    physicsWorld.ClearForces()
    print(body.position, body.angle)

    for p in world.players:
        p.handle_input()


app.run(screen, draw_frame, update_frame, fps=GAME_FPS)
