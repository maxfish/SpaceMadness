import math

from Box2D import b2Vec2
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

from config import PHYSICS_SCALE
from game.entity import Entity
from physics.physics_bullet import PhysicsBullet


class Bullet(Entity):
    def __init__(self, bullet_mgr, world):
        super().__init__(world, 0, 0, 0)
        # The visual representation of the bullet.
        self.owner = None
        self._world = world
        self._quad = QuadDrawable()
        self._quad.texture = Texture.load_from_file('resources/images/bullet.png')
        self._quad.size = Vector2(self._quad.texture.width, self._quad.texture.height)
        self._quad.anchor_to_center()
        # Attach physics only in the initialize method
        self.bullet_radius = min(self._quad.size.x, self._quad.size.y) / PHYSICS_SCALE / 2
        self._angle = None
        self.bullet_mgr = bullet_mgr

    def initialize(self, x, y, direction, speed, owner):
        self.owner = owner
        self._physics = PhysicsBullet(self, self._world.physicsWorld, x / PHYSICS_SCALE, y / PHYSICS_SCALE,
                                      self.bullet_radius, owner)

        # Physics object corresponding to the bullet
        # self._physics.body.userData = {'type': 'bullet', 'obj': self, 'owner': owner}
        # self._physics.body.position = (x / PHYSICS_SCALE, y / PHYSICS_SCALE)
        self._physics.body.angle = math.atan2(-direction.x, direction.y)
        force_dir = b2Vec2(float(direction.x), float(direction.y))
        force_pos = self._physics.body.GetWorldPoint(localPoint=(0.0, 0.0))
        self._physics.body.ApplyLinearImpulse(force_dir * speed, force_pos, True)

    def draw(self, screen):
        self._quad.draw(screen)

    def update(self, screen):
        pos = self._physics.body.position
        if pos.x < 0 or pos.x > self._world.bounds.w / PHYSICS_SCALE or \
                        pos.y < 0 or pos.y > self._world.bounds.h / PHYSICS_SCALE:
            # Bullet is outside the screen
            self.remove_bullet()
        else:
            # Update the position of the bullet
            pos *= PHYSICS_SCALE
            self._quad.pos = Vector2(pos[0], pos[1])
            self._quad.angle = self._physics.body.angle
            pos /= PHYSICS_SCALE

    def collide(self, other, began=False, **kwargs):
        # Don't do anything if a bullet is hitting a bullet.
        if isinstance(other, type(self)):
            return
        # If a bullet is hit by anything else, recycle it.
        if not began:
            self.remove_bullet()

    def remove_bullet(self):
        # Mark the associated physical object for deletion
        self.bullet_mgr.mark_for_recycle(self)
