from game.entity import Entity
from game.entities.bullet import Bullet


class BulletManager(Entity):
    def __init__(self, world):
        self.world = world
        self.active_bullets = set()
        self.bullets_to_recycle = set()

    def _create_bullet(self):
        return Bullet(self, self.world)

    def gen_bullet(self):
        bullet = self._create_bullet()
        self.active_bullets.add(bullet)
        return bullet

    def mark_for_recycle(self, bullet):
        self.bullets_to_recycle.add(bullet)

    def recycle_all(self):
        for bullet in self.bullets_to_recycle:
            body = bullet._physics.body
            self.world.physicsWorld.DestroyBody(body)
            self.active_bullets.remove(bullet)
        self.bullets_to_recycle = set()

        print("--- NUM bodies: {0}".format(len(self.world.physicsWorld.bodies)))

    def draw(self, screen):
        for bullet in self.active_bullets:
            bullet.draw(screen)

    def update(self, screen):
        for bullet in self.active_bullets:
            bullet.update(screen)
