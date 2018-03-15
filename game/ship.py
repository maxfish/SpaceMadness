import math

from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2

from game.entity import Entity
from game.shield import Shield
from game.turret import Turret


class Ship(Entity):
    def __init__(
        self,
        world,
        pilotController,
        shieldController,
        x,
        y,
        z=0,
    ):
        super().__init__(world, x, y, z)

        self._dim = Vector2(130, 344)

        self._quad = QuadDrawable(0, 0, self._dim.x, self._dim.y)
        self._quad.pos = self._position
        self._quad.texture = Texture.load_from_file('resources/images/ship/hull.png')

        self.shieldController = shieldController
        self.pilotController = pilotController

        self.shields = [
            Shield(self),
            Shield(self),
        ]
        self.turret = Turret(None, 100, 100)

    def update(self, game_speed):
        if self.pilotController:
            self.pilotController.update()
        self.shieldController.update()

        shield0_input_values = (
            self.shieldController.get_axis(0) or 0.0,
            self.shieldController.get_axis(1) or 0.0,
        )
        shield1_input_values = (
            self.shieldController.get_axis(2) or 0.0,
            self.shieldController.get_axis(3) or 0.0,
        )

        self.shields[0].update(game_speed, shield0_input_values)
        self.shields[1].update(game_speed, shield1_input_values)
        self.turret.update(game_speed)

    def draw(self, screen):
        for shield in self.shields:
            shield.draw(screen)
        self._quad.draw(screen)
        self.turret.draw(screen)
