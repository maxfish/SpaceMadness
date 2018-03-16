import ctypes
import math

import sdl2
from Box2D import b2World
from mgl2d.math.vector2 import Vector2
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture

from config import SCREEN_WIDTH, SCREEN_HEIGHT, PHYSICS_SCALE, SHIP_SCALE
import config
from game.entities.ship import Ship
from game.entities.asteroid import Asteroid
from game.bullet_mgr import BulletManager
from physics.contact import ContactListener
import random

INTRO_DEBUG = 0
DEBUG = 0


# noinspection PyAttributeOutsideInit
class World:
    SCENE_NONE = 0
    SCENE_TITLE = 1
    SCENE_GAME = 2
    SCENE_GAME_OVER = 4

    def __init__(self, bounds, controllers, stage, debug=0):
        self.scene = self.SCENE_TITLE
        self.game_over_timer = 0
        self.stage = stage

        self.bounds = bounds
        self.debug = debug

        self.window_x = 0
        self.window_y = 0

        self.physicsWorld = b2World(gravity=(0, 0), contactListener=ContactListener())
        # Physical bodies should be deleted outside the simulation step.
        self.physics_to_delete = []

        self.controllers = controllers

        self.bullet_mgr = bullet_mgr = BulletManager(self)

        self.players = []
        self.entities = [bullet_mgr]

        def batch(iterable, n=1):
            l = len(iterable)
            for ndx in range(0, l, n):
                yield iterable[ndx:min(ndx + n, l)]

        quadrant = 0
        for cs in batch(controllers, 3):
            x = 300 + (SCREEN_WIDTH - 600) * (quadrant & 1) + 100 * random.uniform(-1, 1)
            y = 200 + (SCREEN_HEIGHT - 400) * (quadrant >> 1 & 1) + 50 * random.uniform(-1, 1)
            ship = Ship(
                self,
                bullet_mgr,
                controllers=cs,
                x=x,
                y=y,
                # angle=math.degrees(math.atan2(y, x)) - 180
                color='standard',
            )
            self.players.append(ship)
            self.entities.append(ship)
            quadrant += 1

        ship = Ship(
            self,
            bullet_mgr,
            controllers=[],
            x=700,
            y=400,
            color='red',
        )

        self.players.append(ship)
        self.entities.append(ship)

        ship = Ship(
            self,
            bullet_mgr,
            controllers=[],
            x=400,
            y=500,
            color='green',
        )

        self.players.append(ship)
        self.entities.append(ship)

        self.game_over_quad = QuadDrawable(
            SCREEN_WIDTH / 2 - 496 / 2,
            SCREEN_HEIGHT / 2 - 321 / 2,
            496,
            321,
        )
        self.game_over_quad.texture = Texture.load_from_file('resources/images/game_over.png')

        self.asteroids = []
        # self.generate_asteroid()

    def restart_game(self):
        # This is not enough, you need to re-init players
        self.__init__(
            bounds=self.bounds,
            controllers=self.controllers,
            stage=self.stage,
            debug=self.debug,
        )

    def begin(self):
        self.scene = self.SCENE_GAME
        # for character in self.characters:
        #     character.begin()

    def update(self, game_speed):
        # Mouse controlling an asteroid
        if len(self.asteroids)>0:
            x, y = ctypes.c_int(0), ctypes.c_int(0)
            buttonstate = sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
            self.asteroids[0]._physicAsteroid.body.velocity = (0,0)
            self.asteroids[0]._physicAsteroid.body.position = (x.value/PHYSICS_SCALE, y.value/PHYSICS_SCALE)

        time_delta = game_speed * config.GAME_FRAME_MS
        alive = 0
        for p in self.players:
            if p.is_live():
                alive += 1

        if alive <= 1 and self.game_over_timer <= 0:
            self.game_over_timer = 5000

        if self.game_over_timer > 0 and self.game_over_timer < time_delta:
            self.restart_game()
            return

        self.game_over_timer -= time_delta

        if self.game_over_timer > 0:
            # show game over
            pass
        else:
            self.game_over_timer = 0

        self.stage.update(game_speed)
        for e in self.asteroids:
            e.update(game_speed)
        for e in self.entities:
            e.update(game_speed)

        if random.randint(0, 10000) < 100:
            self.generate_asteroid()

        self.check_asteroids()

        # Check position of physical objects
        for e in self.entities:
            if not isinstance(e, Ship):
                continue

            pos = e._physicsShip.body.position
            force_dir = Vector2()
            if pos.x < 0:
                force_dir = Vector2(1, 0)
            elif pos.x > self.bounds.w / PHYSICS_SCALE:
                force_dir = Vector2(-1, 0)
            elif pos.y < 0:
                force_dir = Vector2(0, 1)
            elif pos.y > self.bounds.h / PHYSICS_SCALE:
                force_dir = Vector2(0, -1)

            intensity = 100
            force_dir *= intensity
            force_apply_pos = e._physicsShip.body.GetWorldPoint(localPoint=(0.0, 0.0))
            e._physicsShip.body.ApplyLinearImpulse((force_dir.x, force_dir.y), force_apply_pos, True)

    def draw(self, screen):
        self.stage.draw_background(screen, self.window_x, self.window_y)

        for e in self.asteroids:
            e.draw(screen)
        for e in self.entities:
            e.draw(screen)

        self.stage.draw_foreground(screen, self.window_x, self.window_y)

        if self.game_over_timer > 0:
            self.game_over_quad.draw(screen)

    def game_over(self):
        self.scene = self.SCENE_GAME_OVER

    def generate_asteroid(self):
        return
        # Picks a random movement direction
        direction = Vector2()
        angle = random.randint(0, 359)
        direction.x = math.cos(math.radians(angle))
        direction.y = math.sin(math.radians(angle))

        # Places the asteroid outside of the screen
        position = Vector2()
        position.x = SCREEN_WIDTH / 2 + direction.x * (SCREEN_WIDTH / 1.5)
        position.y = SCREEN_HEIGHT / 2 + direction.y * (SCREEN_HEIGHT / 1.5)

        speed = -Vector2(direction.x, direction.y) * 1000 * random.random()
        torque = 1 * random.random()
        asteroid = Asteroid(self, position.x, position.y, speed=speed, torque=torque)
        self.asteroids.append(asteroid)

    def check_asteroids(self):
        for asteroid in self.asteroids:
            if asteroid.destroy():
                self.asteroids.remove(asteroid)
                print('asteroid removed')
