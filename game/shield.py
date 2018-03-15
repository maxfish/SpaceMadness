import math
from game.entity import Entity
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2


class Shield(Entity):
    def __init__(self, ship):
        super().__init__(ship._world, 0, 0)

        self._ship = ship
        self._position = self._ship.position
        self._angle = 0
        self._rad1 = ship._dim.x / 1.8
        self._rad2 = ship._dim.y / 2.9

        self._quad = QuadDrawable(0, 0, 127, 127)
        self._quad.pos = self._position
        self._quad.texture = Texture.load_from_file('resources/images/shield_arc.png')
        self._quad.anchor = Vector2(65, 65)

    def calc_angle(self, input_values):
        x, y = input_values
        return self._angle + x * 0.5

    def update(self, game_speed, input_values):
        self._angle = self.calc_angle(input_values)
        self._position = \
            self._ship._position + \
            self._ship._dim.__div__(2.0) + \
            Vector2(
                self._rad1 * math.cos(math.radians(self._angle-45)),
                self._rad2 * math.sin(math.radians(self._angle-45)),
            )

        self._quad.angle = self._angle
        self._quad.pos = self.position

    def draw(self, screen):
        self._quad.draw(screen)
