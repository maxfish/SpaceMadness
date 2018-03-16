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
        # The visual representation of the bullet.
        self._quad = QuadDrawable()
        self._quad.texture = Texture.load_from_file('resources/images/bullet.png')
        self._quad.scale = Vector2(self._quad.texture.width, self._quad.texture.height)
        self._quad.anchor = self._quad.scale / 2
        # By default, bullet is not visible after it has been created for the first time
        self._active = False
        self._physics_world = physics_world
        # Attach physics only in the initialize method
        self.bullet_radius = min(self._quad.scale.x, self._quad.scale.y) / PHYSICS_SCALE / 2
        self._angle = None
        self.bullet_mgr = bullet_mgr

    @property
    def active(self):
        return self._active

    def initialize(self, x, y, direction, speed, owner):
        self._physics = PhysicsBullet(self, self._physics_world, -100, -100, self.bullet_radius, owner)

        # Physics object corresponding to the bullet
        self._physics.body.position = (x / PHYSICS_SCALE, y / PHYSICS_SCALE)
        self._physics.body.angle = math.atan2(-direction.x, direction.y)

        force_dir = b2Vec2(float(direction.x), float(direction.y))
        force_pos = self._physics.body.GetWorldPoint(localPoint=(0.0, 0.0))
        self._physics.body.ApplyLinearImpulse(force_dir * speed, force_pos, True)
        self._active = True

    def draw(self, screen):
        if self.active:
            self._quad.draw(screen)

    def update(self, screen):
        pos = self._physics.body.position * PHYSICS_SCALE
        self._quad.pos = Vector2(pos[0], pos[1])
        self._quad.angle = math.degrees(self._physics.body.angle)

    def collide(self, other, began=False, **kwargs):
        # Don't do anything if a bullet is hitting a bullet.
        if isinstance(other, type(self)):
            return
        # If a bullet is hit by anything else, recycle it.
        if began:
            self.bullet_mgr.recycle(self)
