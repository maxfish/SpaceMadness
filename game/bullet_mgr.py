from game.entity import Entity
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2


class BulletManager:
    def __init__(self, world):
        self.world = world
        self.bullet_list = []
        self.recycled_bullet_list = []

    def gen_bullet(self):
        bullet = None
        if len(self.recycled_bullet_list) == 0:
            bullet = QuadDrawable(0, 0, 255, 255)
            bullet.texture = Texture.load_from_file(
                'resources/images/bullet.png')
            self.bullet_list.append(bullet)
            return bullet
        else:
            tmp_bullet = self.recycled_bullet_list.pop()
            self.bullet_list.append(tmp_bullet)
            return tmp_bullet

    def recycle_bullet(self, bullet):
        if bullet in self.bullet_list:
            self.bullet_list.remove(bullet)
            self.recycled_bullet_list.append(bullet)

    def update(self):
        pass

    def draw(self, screen):
        pass

