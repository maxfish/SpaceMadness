"""2D drawing examples."""
import sys

import sdl2
import sdl2.ext
from Box2D import b2World
from mgl2d.app import App
from mgl2d.input.game_controller_manager import GameControllerManager
from mgl2d.math.vector2 import Vector2
from physics.contact import ContactListener

from physics.physics_asteroid import PhysicsAsteroid
from physics.physics_shield import PhysicsShield
from physics.physics_ship import PhysicsShip

GAME_FPS = 50
GAME_FRAME_MS = 1000 / GAME_FPS

app = App()


class MockCollidable:
    def __init__(self, name):
        self.name = name

    def collide(self, other, began=False, **kwargs):
        state = 'began' if began else 'ended'


def draw_line(surface, x1, y1, x2, y2):
    color = sdl2.ext.Color(255, 255, 255)
    sdl2.ext.line(surface, color, (x1, y1, x2, y2))


def draw_rect(surface, x, y, width, height):
    color = sdl2.ext.Color(255, 0, 0)
    sdl2.ext.fill(surface, color, ((x - width / 2) * 10, (y - height / 2) * 10, width * 10, height * 10))


contact_listener = ContactListener()
physicsWorld = b2World(gravity=(0, 0), contactListener=contact_listener)

pShip = PhysicsShip(object(), physicsWorld, 50, 50)
pShip2 = PhysicsShip(object(), physicsWorld, 80, 80)
pShield = PhysicsShield(object(), physicsWorld, Vector2(60, 60), 20)
# pBullet = PhysicsBullet(object(), physicsWorld, 10, 20, 8, 13)
pAsteroid = PhysicsAsteroid(object(), physicsWorld, 100, 100)

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
        pAsteroid.update_forces()
        draw_polygon(windowsurface, pAsteroid.body, fixture.shape)

        physicsWorld.ClearForces()
        pShip.update_forces(controller)

        for fixture in pShip.body.fixtures:
            draw_polygon(windowsurface, pShip.body, fixture.shape)
        for fixture in pShip2.body.fixtures:
            draw_polygon(windowsurface, pShip2.body, fixture.shape)
        # draw_rect(windowsurface, pShield.body.position.x, pShield.body.position.y, 40,40)
        for fixture in pShip._gun_left.body.fixtures:
            draw_polygon(windowsurface, pShip._gun_left.body, fixture.shape)

        draw_rect(windowsurface, pShield.body.position.x, pShield.body.position.y, 40, 40)
        # for fixture in pBullet.body.fixtures:
        #     draw_polygon(windowsurface, pBullet.body, fixture.shape)
        physicsWorld.Step(timeStep, vel_iters, pos_iters)
        window.refresh()
    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(run())
