import math

from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2
from mgl2d.input.game_controller import GameController

from config import PHYSICS_SCALE
from game.entity import Entity
from game.shield import Shield
from game.turret import Turret
from physics.physics_ship import PhysicsShip


SCALE = 0.67


class Ship(Entity):
    def __init__(
        self,
        world,
        bullet_mgr,
        controllers,
        x,
        y,
        z=0,
    ):
        super().__init__(world, x, y, z)

        self._dim = Vector2(130 * SCALE, 344 * SCALE)
        self._angle = 0
        self._physicsShip = PhysicsShip(
            self,
            world.physicsWorld,
            x / PHYSICS_SCALE,
            y / PHYSICS_SCALE,
        )

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
            Turret(self, bullet_mgr, offset_x=-59*SCALE, offset_y=2*SCALE),
            Turret(self, bullet_mgr, offset_x=59*SCALE, offset_y=2*SCALE),
        ]

    def update(self, game_speed):
        self._physicsShip.update_forces(self.pilotController)
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
                self.shieldController.get_axis(GameController.AXIS_LEFT_X) or 0.0,
                self.shieldController.get_axis(GameController.AXIS_LEFT_Y) or 0.0,
                self.shieldController.get_axis(GameController.AXIS_TRIGGER_LEFT) or 0.0,
            )
            shield1_input_values = (
                self.shieldController.get_axis(GameController.AXIS_RIGHT_X) or 0.0,
                self.shieldController.get_axis(GameController.AXIS_RIGHT_Y) or 0.0,
                self.shieldController.get_axis(GameController.AXIS_TRIGGER_RIGHT) or 0.0,
            )
        else:
            shield0_input_values = (0.0,0.0,0.0)
            shield1_input_values = (0.0,0.0,0.0)

        self.shields[0].update(game_speed, shield0_input_values)
        self.shields[1].update(game_speed, shield1_input_values)

        if self.turretController:
            turret_left_x, turret_left_y = (
                self.turretController.get_axis(0) or 0.0,
                self.turretController.get_axis(1) or 0.0,
            )
            turret_right_x, turret_right_y = (
                self.turretController.get_axis(2) or 0.0,
                self.turretController.get_axis(3) or 0.0,
            )

            turret_left_fire = self.turretController.is_button_down(
                self.turretController.BUTTON_LEFTSHOULDER,
            )
            turret_right_fire = self.turretController.is_button_down(
                self.turretController.BUTTON_RIGHTSHOULDER,
            )
        else:
            turret_left_x, turret_left_y = (0,0)
            turret_right_x, turret_right_y = (0,0)
            turret_left_fire = turret_right_fire = False

        self.turrets[0].update(game_speed, turret_left_x, turret_left_y, turret_left_fire)
        self.turrets[1].update(game_speed, turret_right_x, turret_right_y, turret_right_fire)

        self._angle = math.degrees(self._physicsShip.body.angle) + 180
        pos = self._physicsShip.body.position * PHYSICS_SCALE
        self._position = Vector2(pos[0], pos[1])
        self._quad.pos = self._position
        self._quad.angle = self._angle

    def draw(self, screen):
        for shield in self.shields:
            shield.draw(screen)
        self._quad.draw(screen)
        for turret in self.turrets:
            turret.draw(screen)

    def collide(self, other, began):
        pass
