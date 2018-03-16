from game.entity import Entity
from game.entities.bullet import Bullet


class BulletManager(Entity):
    def __init__(self, gWorld, pWorld):
        self.gWorld = gWorld
        self.pWorld = pWorld
        self.bullets_pool = [self._create_bullet() for i in range(100)]
        self.active_bullets = []

    def _create_bullet(self, owner=None):
        return Bullet(self, self.gWorld, self.pWorld, owner)

    def gen_bullet(self, owner):
        if not self.bullets_pool:
            bullet = self._create_bullet(owner)
        else:
            bullet = self.bullets_pool.pop()
            bullet.owner = owner

        self.active_bullets.append(bullet)
        return bullet

    def recycle(self, bullet):
        bullet.owner = None
        bullet._active = False
        try:
            self.active_bullets.remove(bullet)
        except ValueError:
            pass
        else:
            # If we encounter a ValueError,
            # it means, bullet is not in active bullets, probably
            # becaase there were multiple collisions and therefore
            # multiple calls to recycle.
            # We assume that the bullet was recycled correctly.
            self.bullets_pool.append(bullet)

    def deactivate(self, bullet):
        if bullet in self.active_bullets:
            self.recycle(bullet)

    def draw(self, screen):
        for bullet in self.active_bullets:
            bullet.draw(screen)

    def update(self, screen):
        for bullet in self.active_bullets:
            bullet.update(screen)
