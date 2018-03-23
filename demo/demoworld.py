import math
import random

from Box2D import b2World
from mgl2d.math.vector2 import Vector2
from physics.contact_listener import ContactListener

from config import SCREEN_WIDTH, SCREEN_HEIGHT, PHYSICS_SCALE
from game.entities.asteroid import Asteroid
from game.entities.ship import Ship

INTRO_DEBUG = 0
DEBUG = 0


# noinspection PyAttributeOutsideInit
class DemoWorld:
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
        # Physical bodies should be deleted outside the simulation step.
        self.physics_to_delete = []

        self.players = []
        self.entities = []

        def batch(iterable, n=1):
            l = len(iterable)
            for ndx in range(0, l, n):
                yield iterable[ndx:min(ndx + n, l)]

        self.asteroids = []

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

        should_gen_asteroid = random.randint(0, 10000)
        if should_gen_asteroid < 10:
            self.generate_person()
        elif should_gen_asteroid < 20:
            self.generate_derelict()
        elif should_gen_asteroid < 100:
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
        angle = random.random() * math.pi*2
        direction.x = math.cos(math.radians(angle))
        direction.y = math.sin(math.radians(angle))

        # Places the asteroid outside of the screen
        position = Vector2()
        position.x = SCREEN_WIDTH / 2 + direction.x * (SCREEN_WIDTH / 1.5)
        position.y = SCREEN_HEIGHT / 2 + direction.y * (SCREEN_HEIGHT / 1.5)

        assets = [
            'resources/images/asteroides/asteroid_01.png',
            'resources/images/asteroides/asteroid_02.png',
            'resources/images/asteroides/asteroid_03.png',
            'resources/images/asteroides/asteroid_04.png',
            'resources/images/asteroides/asteroid_05.png',
            'resources/images/asteroides/asteroid_06.png',
            'resources/images/asteroides/asteroid_07.png',
            'resources/images/asteroides/asteroid_08.png',
            'resources/images/asteroides/asteroid_09.png',
            'resources/images/asteroides/asteroid_10.png',
            'resources/images/asteroides/asteroid_11.png',
            'resources/images/asteroides/asteroid_12.png',
            'resources/images/asteroides/asteroid_13.png',
            'resources/images/asteroides/asteroid_14.png',
        ]

        speed = -Vector2(direction.x, direction.y) * 500 * random.random()
        torque = 1 * random.random()
        asteroid = Asteroid(self, position.x, position.y, speed=speed, torque=torque,
                            asset=assets[random.randint(0, len(assets) - 1)])
        self.asteroids.append(asteroid)

    def generate_derelict(self):
        # Picks a random movement direction
        direction = Vector2()
        angle = random.random() * math.pi*2
        direction.x = math.cos(math.radians(angle))
        direction.y = math.sin(math.radians(angle))

        # Places the asteroid outside of the screen
        position = Vector2()
        position.x = SCREEN_WIDTH / 2 + direction.x * (SCREEN_WIDTH / 1.5)
        position.y = SCREEN_HEIGHT / 2 + direction.y * (SCREEN_HEIGHT / 1.5)

        speed = -Vector2(direction.x, direction.y) * 200 * random.random()
        torque = 0.5 * random.random()

        assets = [
            'resources/images/derelict/part_01.png',
            'resources/images/derelict/part_02.png',
            'resources/images/derelict/part_03.png'
        ]

        asteroid = Asteroid(self, position.x, position.y, speed=speed, torque=torque,
                            asset=assets[random.randint(0, len(assets) - 1)])
        self.asteroids.append(asteroid)

    def generate_person(self):
        # Picks a random movement direction
        direction = Vector2()
        angle = random.random() * math.pi*2
        direction.x = math.cos(math.radians(angle))
        direction.y = math.sin(math.radians(angle))

        # Places the asteroid outside of the screen
        position = Vector2()
        position.x = SCREEN_WIDTH / 2 + direction.x * (SCREEN_WIDTH / 1.5)
        position.y = SCREEN_HEIGHT / 2 + direction.y * (SCREEN_HEIGHT / 1.5)

        speed = -Vector2(direction.x, direction.y) * 200 * random.random()
        torque = 0.5 * random.random()

        assets = [
            'resources/images/people/pilot.png',
            'resources/images/people/gunner.png',
            'resources/images/people/technician.png'
        ]

        asteroid = Asteroid(self, position.x, position.y, speed=speed, torque=torque,
                            asset=assets[random.randint(0, len(assets) - 1)])
        self.asteroids.append(asteroid)

    def check_asteroids(self):
        for asteroid in self.asteroids:
            if asteroid.destroy():
                self.asteroids.remove(asteroid)
