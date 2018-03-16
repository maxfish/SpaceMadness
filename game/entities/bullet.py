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
    def __init__(self, bullet_mgr, graphics_world, physics_world=None, owner=None):
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
        self._physics = PhysicsBullet(self, physics_world, -100, -100, 0.5, owner)
        # Set the angle in the initialize method
        self._direction = None
        self._angle = None
        self.bullet_mgr = bullet_mgr

    @property
    def active(self):
        return self._active

    def initialize(self, x, y, direction, speed, owner):
        self._physics = PhysicsBullet(self, self._physics_world, -100, -100, 0.5, owner)

        # x, y - starting coordinates of the bullet (point at which the bullet was fired)
        self._direction = direction
        self._quad.pos = Vector2(x, y)
        self._quad.angle = math.degrees(math.atan2(-self._direction.x, self._direction.y))
        # Physics object corresponding to the bullet
        self._physics.body.position = (x / PHYSICS_SCALE, y / PHYSICS_SCALE)
        #self._physics.body.angle = math.radians(self._quad.angle)

        dir = b2Vec2(float(self._direction.x), float(self._direction.y))
        pos = self._physics.body.GetWorldPoint(localPoint=(0.0, 0.0))
        self._physics.body.ApplyForce(dir * speed, pos, True)
        self._active = True

    def draw(self, screen):
        if self.active:
            self._quad.draw(screen)

    def update(self, screen):
        pos = self._physics.body.position * PHYSICS_SCALE
        self._quad.pos = Vector2(pos[0], pos[1])

    def collide(self, other, began):
        self.bullet_mgr.recycle(self)
