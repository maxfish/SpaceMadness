import math
from Box2D import b2World
from mgl2d.math.vector2 import Vector2

from config import SCREEN_WIDTH, SCREEN_HEIGHT, PHYSICS_SCALE, SHIP_SCALE
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

    def __init__(self, bounds, controllers, debug=0):
        self.scene = self.SCENE_TITLE

        self.bounds = bounds
        self.debug = debug

        self.window_x = 0
        self.window_y = 0

        self.stage = None

        self.physicsWorld = b2World(gravity=(0, 0), contactListener=ContactListener())

        # Grabs controllers if they're present
        pilotController = shieldController = turretController = None
        if len(controllers) > 0:
            shieldController = controllers[0]
        if len(controllers) > 1:
            turretController = controllers[1]
        if len(controllers) > 2:
            pilotController = controllers[2]

        # TODO: ships should be initialised in stage
        bullet_mgr = BulletManager(self, self.physicsWorld)

        self.players = []
        self.entities = [bullet_mgr]

        def batch(iterable, n=1):
            l = len(iterable)
            for ndx in range(0, l, n):
                yield iterable[ndx:min(ndx + n, l)]

        quadrant=0
        for cs in batch(controllers, 3):
            x = 300 + (SCREEN_WIDTH-600) * (quadrant & 1) + 100 * random.uniform(-1, 1)
            y = 200 + (SCREEN_HEIGHT-400) * (quadrant >> 1 & 1) + 50 * random.uniform(-1, 1)
            ship = Ship(
                self,
                bullet_mgr,
                controllers=cs,
                x=x,
                y=y,
                angle=math.degrees(math.atan2(y, x))-180
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
        )

        self.players.append(ship)
        self.entities.append(ship)

        self.asteroids = []
        self.asteroids.append(
            Asteroid(self, 400, 400, Vector2(0, 0), 0, 'resources/images/derelict/part_01.png', SHIP_SCALE))
        self.asteroids.append(
            Asteroid(self, 390, 440, Vector2(0, 0), 0, 'resources/images/derelict/part_02.png', SHIP_SCALE))
        self.asteroids.append(
            Asteroid(self, 410, 445, Vector2(0, 0), 0, 'resources/images/derelict/part_03.png', SHIP_SCALE))

    def set_stage(self, stage):
        self.stage = stage

    def restart_game(self):
        # This is not enough, you need to re-init players
        self.init(self.bounds, self.stage, self.debug)

    def begin(self):
        self.scene = self.SCENE_GAME
        # for character in self.characters:
        #     character.begin()

    def update(self, game_speed):
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

    def game_over(self):
        self.scene = self.SCENE_GAME_OVER

    def generate_asteroid(self):
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
