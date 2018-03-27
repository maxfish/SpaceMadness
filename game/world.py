import math
import random

from Box2D import b2World, b2PolygonShape, b2CircleShape
from mgl2d.graphics.color import Color
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.shapes import Shapes
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

import config
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from game.bullet_mgr import BulletManager
from game.entities.asteroid import Asteroid
from game.entities.ship import SHIP_TEXTURES
from game.entities.ship import Ship
from physic_config import PhysicConfig
from physics.contact_listener import ContactListener

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

        self.game_over_quad = QuadDrawable(
            SCREEN_WIDTH / 2 - 496 / 2,
            SCREEN_HEIGHT / 2 - 321 / 2,
            496,
            321,
        )
        self.game_over_quad.texture = Texture.load_from_file('resources/images/game_over.png')

        self.bounds = bounds
        self.debug = debug

        self.window_x = 0
        self.window_y = 0

        self.physicsWorld = b2World(gravity=(0, 0), contactListener=ContactListener())
        # Physical bodies should be deleted outside the simulation step.
        self.physics_to_delete = []
        self._shapes = Shapes()

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
                color=SHIP_TEXTURES[list(SHIP_TEXTURES.keys())[quadrant]],
            )
            self.players.append(ship)
            self.entities.append(ship)
            quadrant += 1

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
        time_delta = game_speed * config.GAME_FRAME_MS
        alive = 0
        for p in self.players:
            if p.is_live():
                alive += 1

        if alive <= 1 and self.game_over_timer <= 0:
            self.game_over_timer = 45000

        if self.game_over_timer > 0 and self.game_over_timer < time_delta:
            self.restart_game()
            return

        self.game_over_timer -= time_delta

        if self.game_over_timer <= 0:
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
            elif pos.x > self.bounds.w / PhysicConfig.ptm_ratio:
                force_dir = Vector2(-1, 0)
            elif pos.y < 0:
                force_dir = Vector2(0, 1)
            elif pos.y > self.bounds.h / PhysicConfig.ptm_ratio:
                force_dir = Vector2(0, -1)

            force_dir *= config.BORDER_REPULSION_FORCE
            force_apply_pos = e._physicsShip.body.GetWorldPoint(localPoint=(0.0, 0.0))
            e._physicsShip.body.ApplyForce((force_dir.x, force_dir.y), force_apply_pos, True)

    def draw(self, screen):
        self.stage.draw_background(screen, self.window_x, self.window_y)

        for e in self.asteroids:
            e.draw(screen)
        for e in self.entities:
            e.draw(screen)

        self.stage.draw_foreground(screen, self.window_x, self.window_y)
        if config.PHYSICS_DEBUG_DRAW_BODIES:
            self._draw_physics_bodies(screen)

        if self.game_over_timer > 0:
            self.game_over_quad.draw(screen)

    def _draw_physics_bodies(self, screen):
        for body in self.physicsWorld.bodies:
            for fixture in body.fixtures:
                color = Color(0, 1, 0, 1) if fixture.sensor else Color(1, 0, 0, 1)
                if isinstance(fixture.shape, b2PolygonShape):
                    vertices = [(body.transform * v) * PhysicConfig.ptm_ratio for v in fixture.shape.vertices]
                    vertices = [(v[0], v[1]) for v in vertices]
                    # Add the first point again to close the polygon
                    vertices.append(vertices[0])
                    self._shapes.draw_polyline(screen, vertices, color)
                elif isinstance(fixture.shape, b2CircleShape):
                    center = (body.transform * fixture.shape.pos) * PhysicConfig.ptm_ratio
                    radius = fixture.shape.radius * PhysicConfig.ptm_ratio
                    self._shapes.draw_circle(screen, center.x, center.y, radius, color, start_angle=body.angle)

    def game_over(self):
        self.scene = self.SCENE_GAME_OVER

    def generate_asteroid(self):
        # Picks a random movement direction
        direction = Vector2()
        angle = random.random() * math.pi * 2
        direction.x = math.cos(angle)
        direction.y = math.sin(angle)

        # Places the asteroid outside of the screen
        position = Vector2()
        position.x = SCREEN_WIDTH / 2 + direction.x * (SCREEN_WIDTH / 1.5)
        position.y = SCREEN_HEIGHT / 2 + direction.y * (SCREEN_HEIGHT / 1.5)

        speed = -Vector2(direction.x, direction.y) * config.ASTEROID_VELOCITY * random.random()
        torque = 1 * random.random()
        asteroid = Asteroid(self, position.x, position.y, speed=speed, torque=torque)
        self.asteroids.append(asteroid)

    def check_asteroids(self):
        for asteroid in self.asteroids:
            if asteroid.destroy():
                self.asteroids.remove(asteroid)
