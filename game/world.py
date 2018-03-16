from Box2D import b2World

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

        ship = Ship(
            self,
            bullet_mgr,
            controllers=controllers[:3],
            x=200,
            y=300,
        )

        ship2 = Ship(
            self,
            bullet_mgr,
            controllers=[],
            x=500,
            y=300,
        )

        self.players = [
            ship,
            ship2,
        ]
        self.entities = [
            ship,
            ship2,
            bullet_mgr,
        ]
        self.asteroids = []
        self.val = 0
        # self.item_frames = FramesStore()
        # self.item_frames.load('resources/sprites/items', 'sprites.json')

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
        # for i in self.items:
        #     i.update(game_speed)
        for e in self.entities:
            e.update(game_speed)
        for e in self.asteroids:
            e.update(game_speed)

        self.val += 1
        if(self.val%100 == 0):
            self.generate_asteroid()

    def draw(self, screen):
        self.stage.draw_background(screen, self.window_x, self.window_y)

        # TODO: Draw objects
        for e in self.entities:
            e.draw(screen)
        for e in self.asteroids:
            e.draw(screen)

        self.stage.draw_foreground(screen, self.window_x, self.window_y)

    def game_over(self):
        self.scene = self.SCENE_GAME_OVER

    def generate_asteroid(self):
        side = random.randint(1, 4)
        speed_x = random.randint(-100, 100) / 100
        speed_y = random.randint(-100, 100) / 100
        if side == 1:
            self.generate_asteroid_left(speed_x, speed_y)
        elif side == 2:
            self.generate_asteroid_right(speed_x, speed_y)
        elif side == 3:
            self.generate_asteroid_top(speed_x, speed_y)
        else:
            self.generate_asteroid_bottom(speed_x, speed_y)

    def generate_asteroid_left(self, speed_x, speed_y):
        asteroid = Asteroid(self, 0, random.randint(0, self.stage.height), speed_x=abs(speed_x), speed_y=speed_y)
        self.asteroids.append(asteroid)

    def generate_asteroid_right(self, speed_x, speed_y):
        asteroid = Asteroid(self, self.stage.width, random.randint(0, self.stage.height), speed_x=- abs(speed_x), speed_y=speed_y)
        self.asteroids.append(asteroid)

    def generate_asteroid_top(self, speed_x, speed_y):
        asteroid = Asteroid(self, random.randint(0, self.stage.width), 0, speed_x=speed_x, speed_y=abs(speed_y))
        self.asteroids.append(asteroid)

    def generate_asteroid_bottom(self, speed_x, speed_y):
        asteroid = Asteroid(self, random.randint(0, self.stage.width), self.stage.height, speed_x=speed_x, speed_y=- abs(speed_y) )
        self.asteroids.append(asteroid)
