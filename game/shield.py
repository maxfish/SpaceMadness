import math
from game.entity import Entity
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2

class Shield(Entity):
    def __init__(self, ship):
        super().__init__(
            ship._world,
            ship._position.x,
            ship._position.y,
            ship._z,
        )

        self._ship = ship
        self._quad = QuadDrawable(0, 0, 255, 255)
        self._quad.pos = self.position
        self._quad.texture = Texture.load_from_file('resources/images/shield_arc.png')
        self._quad.anchor = Vector2(127,127)

        self._radius = 200

    def update(self, game_speed):
        self._quad.angle += 0.1
        self._position = \
            self._ship._position + \
            Vector2(
                self._radius * math.cos(math.radians(self._quad.angle)),
                self._radius * math.sin(math.radians(self._quad.angle)),
            )
        self._quad.pos = self.position

    def draw(self, screen):
        self._quad.draw(screen)
