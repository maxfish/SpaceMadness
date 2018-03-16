import math

from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

import config
from game.entities.turret_state import TurretState

from game.entity import Entity
from game.stage import Stage


class Turret(Entity):

    def __init__(self, ship, bullet_mgr, offset_x, offset_y):
        self._ship = ship
        self._bullet_mgr = bullet_mgr
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.texture = Texture.load_from_file('resources/images/guns/minigun_right.png')
        self.texture_FIRING = Texture.load_from_file('resources/images/guns/minigun_shooting.png')
        self.texture_RELOADING = Texture.load_from_file('resources/images/guns/minigun_reloading.png')

        self.turret_quad = QuadDrawable(0, 0, 13 * self._ship.scale, 46 * self._ship.scale)
        self.turret_quad.texture = self.texture
        self.turret_quad.anchor = Vector2(7 * self._ship.scale, 35 * self._ship.scale)

        self.turret_state = TurretState(self)
        self.update(0, 0, 0, False)

    def get_angle(self, x, y):
        # Rotate 90 degrees more to compensate the resource being rotated...
        return math.degrees(math.atan2(y, x)) + 90

    def fire(self):
        self.turret_state.fire()

    def fire_bullet(self):
        # print("Bullet fired from offset : {0} {1}".format(self.offset_x, self.offset_y))
        bullet = self._bullet_mgr.gen_bullet()

        # print('Bullet {} fired from: {} {}, Owner: {}'.format(
        #     id(bullet),
        #     self.turret_quad.pos.x,
        #     self.turret_quad.pos.y,
        #     id(self._ship),
        # ))

        angle = math.radians(self.turret_quad.angle)
        direction = Vector2(math.sin(angle), -math.cos(angle))

        muzzle_pos = Vector2(self.turret_quad.pos.x, self.turret_quad.pos.y) + (direction * 25)
        bullet.initialize(muzzle_pos.x, muzzle_pos.y, direction, config.BULLET_VELOCITY, id(self._ship))

    def hold_fire(self):
        self.turret_state.hold_fire()

    def draw(self, screen):
        if self.turret_state.has_recently_fired:
            self.turret_quad.texture = self.texture_FIRING
        elif self.turret_state.is_reloading:
            self.turret_quad.texture = self.texture_RELOADING
        else:
            self.turret_quad.texture = self.texture

        self.turret_quad.draw(screen)

    def update(self, game_speed, x, y, fire):
        """x and y are the x and y from the controller joystick"""
        if fire:
            self.fire()
        else:
            self.hold_fire()

        self.turret_state.advance_time(
            time_passed_ms=(game_speed * config.GAME_FRAME_MS),
        )

        self.turret_quad.pos = config.PHYSICS_SCALE * (self._ship._physicsShip.body.transform * (
            self.offset_x / config.PHYSICS_SCALE, self.offset_y / config.PHYSICS_SCALE))
        self.turret_quad.angle = self._ship._quad.angle
        if (x, y) != (0.0, 0.0):
            # Angle the turrets according the controller if we have values
            angle = self.get_angle(x, y)
            self.turret_quad.angle = angle

    def collide(self, other, **kwargs):
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
