import math

from mgl2d.graphics.shader import Shader
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2
from mgl2d.input.game_controller import GameController

from config import PHYSICS_SCALE
from game.entity import Entity
from game.entities.shield import Shield
from game.entities.turret import Turret
from game.entities.trail import Trail
from game.entities.side_trail import SideTrail
from physics.physics_ship import PhysicsShip
from game.entities.ship_state import ShipState


SCALE = 0.67


# copied from game.py
GAME_FPS = 50
GAME_FRAME_MS = 1000 / GAME_FPS


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
        self._quad.shader = Shader.from_files('resources/shaders/base.vert', 'resources/shaders/rgba.frag')

        self.controllers = controllers
        self.shieldController = None
        self.pilotController = controllers[0] if len(controllers) else None
        self.turretController = None

        self.shields = [
            Shield(self, world),
            Shield(self, world),
        ]
        self.turrets = [
            Turret(self, bullet_mgr, offset_x=-59*SCALE, offset_y=2*SCALE),
            Turret(self, bullet_mgr, offset_x=59*SCALE, offset_y=2*SCALE),
        ]
        self.ship_state = ShipState(self)

        self.trail = Trail(self, 0, 0)
        self.side_trail_left = SideTrail(self, 28*SCALE, 40*SCALE, -45)
        self.side_trail_right = SideTrail(self, -25*SCALE, 40*SCALE, 225)

        self._healthbar = QuadDrawable(0, 0, self._dim.x, 5)
        self._healthbar.pos = self._position
        self._healthbar.texture = Texture.load_from_file('resources/images/health.png')

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
            trigger_intensity = self.pilotController.get_axis(GameController.AXIS_TRIGGER_RIGHT) or 0.0
            self.trail.update(game_speed, trigger_intensity)

            axis_intensity = self.pilotController.get_axis(GameController.AXIS_LEFT_X) or 0.0
            self.side_trail_left.update(game_speed, axis_intensity)
            self.side_trail_right.update(game_speed, -axis_intensity)

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
                self.turretController.get_axis(GameController.AXIS_LEFT_X) or 0.0,
                self.turretController.get_axis(GameController.AXIS_LEFT_Y) or 0.0,
            )
            turret_right_x, turret_right_y = (
                self.turretController.get_axis(GameController.AXIS_RIGHT_X) or 0.0,
                self.turretController.get_axis(GameController.AXIS_RIGHT_Y) or 0.0,
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

        self.ship_state.update(game_speed)

        self._healthbar.scale = Vector2(
            self._dim.x * self.ship_state.energy / ShipState.MAX_ENERGY,
            self._healthbar.scale.y,
        )
        self._healthbar.pos = self._position + Vector2(-self._dim.x/2, -self._dim.y/3)

    def draw(self, screen):
        if self.ship_state.state == ShipState.LIVE:
            for shield in self.shields:
                shield.draw(screen)

            self.trail.draw(screen)
            self.side_trail_left.draw(screen)
            self.side_trail_right.draw(screen)

            # Important: this has to be drawn AFTER the trails (to be positioned on
            # top of them)
            self._quad.draw(screen)

            for turret in self.turrets:
                turret.draw(screen)
            self._healthbar.draw(screen)

    def collide(self, other, began):
        self.ship_state.damage(energy=10.0)