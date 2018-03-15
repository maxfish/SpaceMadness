import math

from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2
from mgl2d.input.game_controller import GameController

from game.entity import Entity
from game.shield import Shield
from game.turret import Turret

SCALE=0.67



class Ship(Entity):
    def __init__(
        self,
        world,
        controllers,
        x,
        y,
        z=0,
    ):
        super().__init__(world, x, y, z)

        self._dim = Vector2(130*SCALE, 344*SCALE)
        self._angle = 0

        # Used by ship components to scale themselves
        self.scale = SCALE

        self._quad = QuadDrawable(0, 0, self._dim.x, self._dim.y)
        self._quad.pos = self._position
        self._quad.anchor = self._dim.__div__(2.0)
        self._quad.texture = Texture.load_from_file('resources/images/ship/hull.png')

        self.controllers = controllers
        self.shieldController = None
        self.pilotController = None
        self.turretController = None

        self.shields = [
            Shield(self),
            Shield(self),
        ]
        self.turrets = [
            Turret(self, offset_x=-59*SCALE, offset_y=2*SCALE),
            Turret(self, offset_x=59*SCALE, offset_y=2*SCALE),
        ]

    def update(self, game_speed):
        for c in self.controllers:
            c.update()
            if c.is_button_pressed(GameController.BUTTON_DPAD_UP):
                if self.turretController == c:
                    self.turretController = None
                if self.shieldController == c:
                    self.shieldController = None
                self.pilotController = c
            elif c.is_button_pressed(GameController.BUTTON_DPAD_DOWN):
                if self.pilotController == c:
                    self.pilotController = None
                if self.shieldController == c:
                    self.shieldController = None
                self.turretController = c
            elif c.is_button_pressed(GameController.BUTTON_DPAD_LEFT):
                if self.turretController == c:
                    self.turretController = None
                if self.pilotController == c:
                    self.pilotController = None
                self.shieldController = c

        if self.pilotController:
            pass

        if self.shieldController:
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

        if self.turretController:
            turret_left_x, turret_left_y =  (
                self.turretController.get_axis(0) or 0.0,
                self.turretController.get_axis(1) or 0.0,
            )
            turret_right_x, turret_right_y =  (
                self.turretController.get_axis(2) or 0.0,
                self.turretController.get_axis(3) or 0.0,
            )
            self.turrets[0].update(game_speed, turret_left_x, turret_left_y)
            self.turrets[1].update(game_speed, turret_right_x, turret_right_y)

        self._quad.pos = self._position
        self._quad.angle = self._angle

    def draw(self, screen):
        for shield in self.shields:
            shield.draw(screen)
        self._quad.draw(screen)
        for turret in self.turrets:
            turret.draw(screen)
