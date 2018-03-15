import math
from game.entity import Entity
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2

class Ship(Entity):
    def __init__(self, world, x, y, z=0):
        super().__init__(world, x, y, z)

        self._dim = Vector2(130, 344)

        self._quad = QuadDrawable(0, 0, self._dim.x, self._dim.y)
        self._quad.pos = self._position
        self._quad.texture = Texture.load_from_file('resources/images/ship/hull.png')

    def update(self, game_speed):
        pass

    def draw(self, screen):
        self._quad.draw(screen)
