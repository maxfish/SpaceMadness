import math
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

from game.stage import Stage
from game.entity import Entity
from game.turret_state import TurretState


# copied from game.py
GAME_FPS = 50
GAME_FRAME_MS = 1000 / GAME_FPS


class Turret(Entity):

    def __init__(self, ship, offset_x, offset_y):
        self._ship = ship
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.turret_quad = QuadDrawable(0, 0, 13*self._ship.scale, 46*self._ship.scale)
        self.turret_quad.texture = Texture.load_from_file('resources/images/guns/minigun_right.png')
        self.turret_quad.anchor = Vector2(7*self._ship.scale, 35*self._ship.scale)

        self.turret_state = TurretState()

        self.update(0, 0, 0)

    def fire(self):
        self.turret_state.fire()

    def hold_fire(self):
        self.turret_state.hold_fire()

    def draw(self, screen):
        self.turret_quad.draw(screen)

    def update(self, game_speed, x, y):
        """x and y are the x and y from the controller joystick"""
        self.turret_state.advance_time(
            time_passed_ms=(game_speed * GAME_FRAME_MS),
        )

        self.turret_quad.pos = self._ship._quad.pos + Vector2(self.offset_x, self.offset_y)
        angle = math.degrees(math.atan2(y, x))
        self.turret_quad.angle = angle


class TurretStage(Stage):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.quad = QuadDrawable(0, 0, width, height)
        self.quad.texture = Texture.load_from_file('resources/images/bg.png')
        self.turret = Turret(None, 100, 100)


    def get_width(self):
        return self.width

    def update(self, game_speed):
        self.turret.update(game_speed)

    def draw_background(self, surface, window_x, window_y):
        self.quad.draw(surface)

    def draw_foreground(self, surface, window_x, window_y):
        self.turret.draw(surface)
