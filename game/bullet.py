from mgl2d.math.vector2 import Vector2
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable

from game.entity import Entity
from game.stage import Stage


class Bullet(Entity):
    def __init__(self, world):
        super().__init__(world, 0, 0, 0)
        # TODO: we should get the dimensions of the texture
        self._quad = QuadDrawable(self.position.x, self.position.y, 8, 13)
        self._quad.texture = Texture.load_from_file('resources/images/bullet.png')
        # By default, bullet is not visible after it has been created for the first time
        self._active = False

    @property
    def active(self):
        return self._active

    def initialize(self, x, y, angle, speed):
        # x, y - starting coordinates of the bullet (point at which the bullet was fired)
        self._position = Vector2(x, y)
        self._active = True

    def draw(self, screen):
        if self.active:
            self._quad.draw(screen)

    def update(self, screen):
        # TODO: this should call the physics object to update the position
        self._position += Vector2(0, 1)
        self._quad.pos = self.position


class BulletStage(Stage):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.quad = QuadDrawable(0, 0, width, height)
        self.quad.texture = Texture.load_from_file('resources/images/bg.png')
        self.bullet = Bullet(None)
        self.bullet.initialize(0, 0, 0, 0)

    def get_width(self):
        return self.width

    def update(self, game_speed):
        self.bullet.update(game_speed)

    def draw_background(self, surface, window_x, window_y):
        self.quad.draw(surface)

    def draw_foreground(self, surface, window_x, window_y):
        self.bullet.draw(surface)