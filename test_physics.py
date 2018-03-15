"""2D drawing examples."""
import sys

from Box2D import b2World, b2FixtureDef, b2BodyDef
from mgl2d.app import App
from mgl2d.input.game_controller_manager import GameControllerManager
from random import randint
import sdl2
import sdl2.ext
from Box2D import (b2PolygonShape, b2CircleShape)

from physics.physic_ship import PhysicShip

GAME_FPS = 50
GAME_FRAME_MS = 1000 / GAME_FPS

app = App()


def draw_line(surface, x1, y1, x2, y2):
    color = sdl2.ext.Color(255, 255, 255)
    sdl2.ext.line(surface, color, (x1, y1, x2, y2))


def draw_rects(surface, width, height):
    # Fill the whole surface with a black color.
    sdl2.ext.fill(surface, 0)
    for k in range(15):
        x, y = randint(0, width), randint(0, height)
        w, h = randint(1, width // 2), randint(1, height // 2)
        color = sdl2.ext.Color(randint(0, 255),
                               randint(0, 255),
                               randint(0, 255))
        sdl2.ext.fill(surface, color, (x, y, w, h))


physicsWorld = b2World(gravity=(0, 0))
pShip = PhysicShip(physicsWorld, 10, 30)

timeStep = 1.0 / GAME_FPS
vel_iters, pos_iters = 6, 2

sdl2.ext.init()
window = sdl2.ext.Window("2D drawing primitives", size=(1920, 1080))
window.show()

windowsurface = window.get_surface()


def draw_polygon(screen, body, polygon):
    vertices = [(body.transform * v) * 10 for v in polygon.vertices]
    vertices = [(v[0], 1080 - v[1]) for v in vertices]
    for i in range(0, len(vertices)):
        draw_line(screen, int(vertices[i][0]), int(vertices[i][1]), int(vertices[(i + 1) % len(vertices)][0]),
                  int(vertices[(i + 1) % len(vertices)][1]))


# b2PolygonShape.draw = my_draw_polygon
controllerManager = GameControllerManager()
controllerManager.load_joysticks_database('resources/gamecontrollerdb.txt')
controller = controllerManager.grab_controller()

timeStep = 1.0 / GAME_FPS
vel_iters, pos_iters = 6, 2


def run():
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        sdl2.ext.fill(windowsurface, 0)
        physicsWorld.Step(timeStep, vel_iters, pos_iters)
        physicsWorld.ClearForces()
        pShip.update_forces(controller)
        for fixture in pShip.body.fixtures:
            draw_polygon(windowsurface, pShip.body, fixture.shape)
        window.refresh()
    sdl2.ext.quit()
    return 0


#     b2PolygonShape *polygonShape = new b2PolygonShape();
#     b2Vec2 points[7];
#     points[0] = b2Vec2(0, h * 0.5f);
#     points[1] = b2Vec2(-w * 0.5f, h * 0.5f - w * 0.5f);
#     points[2] = b2Vec2(-w * 0.5f, -h * 0.5f + w * 0.3f);
#     points[3] = b2Vec2(-w * 0.25f, -h * 0.5f);
#     points[4] = b2Vec2(w * 0.25f, -h * 0.5f);
#     points[5] = b2Vec2(w * 0.5f, -h * 0.5f + w * 0.3f);
#     points[6] = b2Vec2(w * 0.5f, h * 0.5f - w * 0.5f);
#     polygonShape->Set(points, 7);


if __name__ == "__main__":
    sys.exit(run())
