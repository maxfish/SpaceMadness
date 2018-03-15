import math
import numpy as np
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2
from mgl2d.math.matrix4 import Matrix4


from game.stage import Stage
from game.entity import Entity
from game.turret_state import TurretState


# copied from game.py
GAME_FPS = 50
GAME_FRAME_MS = 1000 / GAME_FPS


BULLET_VELOCITY = 80


class Turret(Entity):

    def __init__(self, ship, bullet_mgr, offset_x, offset_y):
        self._ship = ship
        self._bullet_mgr = bullet_mgr
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.turret_quad = QuadDrawable(0, 0, 13*self._ship.scale, 46*self._ship.scale)
        self.turret_quad.texture = Texture.load_from_file('resources/images/guns/minigun_right.png')
        self.turret_quad.anchor = Vector2(7*self._ship.scale, 35*self._ship.scale)

        self.turret_state = TurretState(self)
        self.update(0, 0, 0, False)

    def get_angle(self, x, y):
        # Rotate 90 degrees more to compensate the resource being rotated...
        return math.degrees(math.atan2(y, x)) + 90

    def fire(self):
        self.turret_state.fire()

    def fire_bullet(self):
        # print("Bullet fired from offset : {0} {1}".format(self.offset_x, self.offset_y))
        print("Bullet fired from: {0} {1}".format(self.turret_quad.pos.x, self.turret_quad.pos.y))
        print("Bullet owner: {0}".format(id(self._ship)))
        bullet = self._bullet_mgr.gen_bullet(id(self._ship))
        x = self.turret_quad.pos.x
        y = self.turret_quad.pos.y

        angle = math.radians(self.turret_quad.angle)
        z_sin = math.sin(angle)
        z_cos = math.cos(angle)
        direction = Vector2(z_sin, -z_cos)

        muzzle_pos = Vector2(x, y) + (direction * 25)
        x = muzzle_pos.x
        y = muzzle_pos.y

        bullet.initialize(x, y, direction, BULLET_VELOCITY, id(self._ship))
        print("Angle={0}".format(angle))

    def hold_fire(self):
        self.turret_state.hold_fire()

    def draw(self, screen):
        self.turret_quad.draw(screen)

    def update(self, game_speed, x, y, fire):
        """x and y are the x and y from the controller joystick"""
        if fire:
            self.fire()
        else:
            self.hold_fire()

        self.turret_state.advance_time(
            time_passed_ms=(game_speed * GAME_FRAME_MS),
        )

        self.turret_quad.pos = self._ship._quad.pos + Vector2(self.offset_x, self.offset_y)
        if (x, y) == (0.0, 0.0):
            # Align guns with the ship if they're inactive
            angle = self._ship._quad.angle
        else:
            angle = self.get_angle(x, y)
        self.turret_quad.angle = angle

    def collide(self, other, began):
        pass


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
