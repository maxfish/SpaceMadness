import math

from Box2D import b2Vec2
from mgl2d.math.vector2 import Vector2
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable

from config import PHYSICS_SCALE
from game.entity import Entity
from game.stage import Stage
from physics.physics_bullet import PhysicsBullet


class Bullet(Entity):
    def __init__(self, bullet_mgr, graphics_world, physics_world=None):
        super().__init__(graphics_world, 0, 0, 0)
        # TODO: we should get the dimensions of the texture
        self.width = 8
        self.length = 13
        # The visual representation of the bullet.
        self._quad = QuadDrawable(self.position.x, self.position.y, self.width, self.length)
        self._quad.texture = Texture.load_from_file('resources/images/bullet.png')
        # By default, bullet is not visible after it has been created for the first time
        self._active = False
        self._physics_world = physics_world
        # Attach physics only in the initialize method
        self._physics = PhysicsBullet(self, physics_world, -100, -100, 0.5)
        # Set the angle in the initialize method
        self._direction = None
        self._angle = None
        self.bullet_mgr = bullet_mgr

    @property
    def active(self):
        return self._active

    def initialize(self, x, y, direction, speed):
        self._physics = PhysicsBullet(self, self._physics_world, -100, -100, 0.5)

        # x, y - starting coordinates of the bullet (point at which the bullet was fired)
        self._direction = direction
        self._quad.pos = Vector2(x, y)
        self._quad.angle = math.degrees(math.atan2(self._direction.y, self._direction.x)) + 90
        print("BULLET ANGLE: {0}".format(self._quad.angle))
        # Physics object corresponding to the bullet
        # TODO remove + 100
        self._physics.body.position = ((x + 100) / PHYSICS_SCALE, (y + 100) / PHYSICS_SCALE)
        self._physics.body.angle = math.radians(self._quad.angle)

        dir = b2Vec2(float(self._direction.y), float(self._direction.x))
        pos = self._physics.body.GetWorldPoint(localPoint=(0.0, 0.0))
        self._physics.body.ApplyForce(dir * speed * 40, pos, True)
        self._active = True

    def draw(self, screen):
        if self.active:
            self._quad.draw(screen)

    def update(self, screen):
        pos = self._physics.body.position * PHYSICS_SCALE
        self._quad.pos = Vector2(pos[0], pos[1])

    def collide(self, other, began):
        pass

class BulletStage(Stage):
    def __init__(self, width, height, bullet_mgr):
        super().__init__(width, height)
        self.quad = QuadDrawable(0, 0, width, height)
        self.quad.texture = Texture.load_from_file('resources/images/bg.png')
        self.bullet_mgr = bullet_mgr
        self.bullet = self.bullet_mgr.gen_bullet()
        self.bullet.initialize(0, 0, 0, 0)

    def get_width(self):
        return self.width

    def update(self, game_speed):
        self.bullet.update(game_speed)

    def draw_background(self, surface, window_x, window_y):
        self.quad.draw(surface)

    def draw_foreground(self, surface, window_x, window_y):
        self.bullet.draw(surface)
