import math
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

from game.entity import Entity


class Trail(Entity):

    def __init__(self, ship, offset_x, offset_y):
        self._ship = ship
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.full_dimensions = Vector2(130*self._ship.scale, 344*self._ship.scale)
        self._quad = QuadDrawable(0, 0, self.full_dimensions.x, self.full_dimensions.y)
        self._quad.texture = Texture.load_from_file('resources/images/ship/trail.png')
        # Don't ask why 173...
        self._quad.anchor = Vector2(65*self._ship.scale, 173*self._ship.scale)

        self.update(0, 0)

    def draw(self, screen):
        self._quad.draw(screen)

    def update(self, game_speed, trigger_intensity):
        """`trigger_intensity` is a number from 0 to 1 representing how much a player is
        pressing the controller's right trigger.
        """
        self._quad.scale = self.full_dimensions * trigger_intensity
        self._quad.pos = Vector2(
            self._ship._quad.pos.x + self.offset_x,
            self._ship._quad.pos.y + self.offset_y,
        )
        self._quad.angle = self._ship._quad._angle
