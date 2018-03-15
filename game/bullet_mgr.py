from game.entity import Entity
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2
from .bullet import Bullet


class BulletManager:
    def __init__(self, gWorld, pWorld):
        self.gWorld = gWorld
        self.pWorld = pWorld
        self.bullets_pool = [self._create_bullet()] * 100
        self.active_bullets = []

    def _create_bullet(self):
        bullet = Bullet(self.gWorld, self.pWorld)
        return bullet

    def gen_bullet(self):
        if len(self.bullets_pool) == 0:
            bullet = self._create_bullet()
            self.active_bullets.append(bullet)
        else:
            bullet = self.bullets_pool.pop()
            self.active_bullets.append(bullet)
        return bullet

    def deactivate(self, bullet):
        if bullet in self.active_bullets:
            self.active_bullets.remove(bullet)
            self.bullets_pool.append(bullet)

