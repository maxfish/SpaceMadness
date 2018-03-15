from game.entity import Entity
from .bullet import Bullet


class BulletManager(Entity):
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
            bullet._active = False
            self.active_bullets.remove(bullet)
            self.bullets_pool.append(bullet)

    def draw(self, screen):
        #print("active bullets: {0}".format(len(self.active_bullets)))
        for bullet in self.active_bullets:
            bullet.draw(screen)

    def update(self, screen):
        for bullet in self.active_bullets:
            bullet.update(screen)
