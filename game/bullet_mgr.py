from game.entity import Entity
from game.entities.bullet import Bullet


class BulletManager(Entity):
    def __init__(self, world):
        self.world = world
        self.bullets_pool = [self._create_bullet() for _ in range(100)]
        self.active_bullets = []
        self.bullets_to_recycle = set()

    def _create_bullet(self):
        return Bullet(self, self.world)

    def gen_bullet(self):
        if not self.bullets_pool:
            bullet = self._create_bullet()
        else:
            bullet = self.bullets_pool.pop()

        self.active_bullets.append(bullet)
        return bullet

    def mark_for_recycle(self, bullet):
        # will be in active bullets and bullets to recycle
        assert bullet._physics
        self.bullets_to_recycle.add(bullet)

    def recycle_all(self):
        bodies = []
        for bullet in self.bullets_to_recycle:
            bodies.append(bullet._physics.body)
            self.recycle(bullet)
        self.bullets_to_recycle = set()

        for body in bodies:
            self.world.physicsWorld.DestroyBody(body)
        #print("--- NUM bodies: {0}".format(len(self.world.physicsWorld.bodies)))

    def recycle(self, bullet):
        bullet.owner = None
        bullet._physics = None
        self.active_bullets.remove(bullet)

    def draw(self, screen):
        for bullet in self.active_bullets:
            bullet.draw(screen)

    def update(self, screen):
        # print("NUM of active  bullets: {0}, in pool: {1}".format(len(self.active_bullets), len(self.bullets_pool)))
        for bullet in self.active_bullets:
            bullet.update(screen)
