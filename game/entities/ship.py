import math
from random import random

from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.shader import Shader
from mgl2d.graphics.texture import Texture
from mgl2d.input.game_controller import GameController
from mgl2d.math.vector2 import Vector2
from game.entities.asteroid import Asteroid

import config
# from game.entities.healthbar import HealthBar
from game.entities.shield import Shield
from game.entities.ship_state import ShipState
from game.entities.side_trail import SideTrail
from game.entities.trail import Trail
from game.entities.turret import Turret
from game.entity import Entity
from physics.physics_ship import PhysicsShip


SCALE = 0.67

SHIP_TEXTURES = {
    'standard': 'resources/images/ship/hull.png',
    'green': 'resources/images/ship/hull_green.png',
    'red': 'resources/images/ship/hull_red.png',
}


class Ship(Entity):
    def __init__(
        self,
        world,
        bullet_mgr,
        controllers,
        x,
        y,
        z=0,
        angle=0,
        color='standard',
    ):
        super().__init__(world, x, y, z)
        self.world = world

        self._dim = Vector2(130 * SCALE, 344 * SCALE)
        self._angle = angle
        self._physicsShip = PhysicsShip(
            self,
            world.physicsWorld,
            x / config.PHYSICS_SCALE,
            y / config.PHYSICS_SCALE,
            angle=angle,
        )

        # Used by ship components to scale themselves
        self.scale = SCALE

        self._quad = QuadDrawable(0, 0, self._dim.x, self._dim.y)
        self._quad.pos = self._position
        self._quad.anchor = self._dim.__div__(2.0)

        texture_file = SHIP_TEXTURES.get(color, SHIP_TEXTURES['standard'])
        self._quad.texture = Texture.load_from_file(texture_file)
        self._quad.shader = Shader.from_files('resources/shaders/base.vert', 'resources/shaders/rgba.frag')

        self.controllers = controllers
        self.pilotController = controllers[0] if len(controllers) else None
        self.shieldController = controllers[1] if len(controllers) > 1 else None
        self.turretController = controllers[2] if len(controllers) > 2 else None

        self.shields = [
            Shield(self, world),
            Shield(self, world),
        ]

        self.turret_right = Turret(self, bullet_mgr, offset_x=-59*SCALE, offset_y=2*SCALE)
        self.turret_left = Turret(self, bullet_mgr, offset_x=59*SCALE, offset_y=2*SCALE)

        self.ship_state = ShipState(self)

        self.trail = Trail(self, 0, 0)
        self.side_trail_left = SideTrail(self, 28*SCALE, 40*SCALE, -45)
        self.side_trail_right = SideTrail(self, -25*SCALE, 40*SCALE, 225)

        # self._healthbar = HealthBar(self, world)

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

        if self.pilotController and self.ship_state.state == ShipState.LIVE:
            boost = self.pilotController.is_button_down(GameController.BUTTON_A)

            trigger_intensity = self.pilotController.get_axis(GameController.AXIS_TRIGGER_RIGHT) or 0.0
            self.trail.update(game_speed, trigger_intensity, boost)

            axis_intensity = self.pilotController.get_axis(GameController.AXIS_LEFT_X) or 0.0
            self.side_trail_left.update(game_speed, axis_intensity)
            self.side_trail_right.update(game_speed, -axis_intensity)

        if self.shieldController and self.ship_state.state == ShipState.LIVE:
            shield0_input_values = (
                self.shieldController.get_axis(GameController.AXIS_LEFT_X) or 0.0,
                self.shieldController.get_axis(GameController.AXIS_LEFT_Y) or 0.0,0.0,
            )
            shield1_input_values = (
                self.shieldController.get_axis(GameController.AXIS_RIGHT_X) or 0.0,
                self.shieldController.get_axis(GameController.AXIS_RIGHT_Y) or 0.0,0.0,
            )
        else:
            shield0_input_values = (0.0, 0.0, 0.0)
            shield1_input_values = (0.0, 0.0, 0.0)

        self.shields[0].update(game_speed, shield0_input_values)
        self.shields[1].update(game_speed, shield1_input_values)

        if self.turretController and self.ship_state.state == ShipState.LIVE:
            turret_left_x, turret_left_y = (
                self.turretController.get_axis(GameController.AXIS_LEFT_X) or 0.0,
                self.turretController.get_axis(GameController.AXIS_LEFT_Y) or 0.0,
            )
            turret_right_x, turret_right_y = (
                self.turretController.get_axis(GameController.AXIS_RIGHT_X) or 0.0,
                self.turretController.get_axis(GameController.AXIS_RIGHT_Y) or 0.0,
            )

            threshold = 0.2
            turret_left_fire = (self.turretController.get_axis(GameController.AXIS_TRIGGER_LEFT) or 0.0) > threshold
            turret_right_fire = (self.turretController.get_axis(GameController.AXIS_TRIGGER_RIGHT) or 0.0) > threshold

        else:
            turret_left_x, turret_left_y = (0,0)
            turret_right_x, turret_right_y = (0,0)
            turret_left_fire = turret_right_fire = False

        self.turret_left.update(
            game_speed,
            turret_left_x,
            turret_left_y,
            turret_left_fire,
            is_right_wing=False,
        )
        self.turret_right.update(
            game_speed,
            turret_right_x,
            turret_right_y,
            turret_right_fire,
            is_right_wing=True,
        )

        self._angle = math.degrees(self._physicsShip.body.angle) + 180
        pos = self._physicsShip.body.position * config.PHYSICS_SCALE
        self._position = Vector2(pos[0], pos[1])
        self._quad.pos = self._position
        self._quad.angle = self._angle

        self.ship_state.update(
            time_passed_ms=(game_speed * config.GAME_FRAME_MS),
        )

        # self._healthbar.update(game_speed)

    def draw(self, screen):
        if self.is_live():
            for shield in self.shields:
                shield.draw(screen)

            self.trail.draw(screen)
            self.side_trail_left.draw(screen)
            self.side_trail_right.draw(screen)

            if self.has_recent_damage():
                energy_ratio = self.ship_state.energy / self.ship_state.MAX_ENERGY
                damage_ratio = 1.0 - energy_ratio
                self._quad.shader.bind()
                self._quad.shader.set_uniform_float('mul_r', 0.0)
                self._quad.shader.set_uniform_float('mul_g', 0.2 + 0.8 * damage_ratio)
                self._quad.shader.set_uniform_float('mul_b', 0.2 + 0.8 * damage_ratio)
            else:
                self._quad.shader.bind()
                self._quad.shader.set_uniform_float('mul_r', 0.0)
                self._quad.shader.set_uniform_float('mul_g', 0.0)
                self._quad.shader.set_uniform_float('mul_b', 0.0)

            self.turret_left.draw(screen)
            self.turret_right.draw(screen)

            # Important: this has to be drawn AFTER the trails and turrets (to
            # be positioned on top of them)
            self._quad.draw(screen)

    def destroy_ship(self):
        pos = self._physicsShip.body.position * config.PHYSICS_SCALE
        x, y = pos

        self.world.asteroids.append(Asteroid(
            self.world,
            x, y - 30,
            Vector2(random() * 30 - 15, random() * -100),
            random() * 3.0,
            'resources/images/derelict/part_01.png', config.SHIP_SCALE
        ))
        self.world.asteroids.append(Asteroid(
            self.world,
            x + 30, y + 30,
            Vector2(random() * 60 + 30, random() * 60 + 30),
            random() * 3.0,
            'resources/images/derelict/part_02.png', config.SHIP_SCALE
        ))
        self.world.asteroids.append(Asteroid(
            self.world,
            x - 30, y + 30,
            Vector2(random() * -60 - 30, random() * 60 + 30),
            random() * 3.0,
            'resources/images/derelict/part_03.png', config.SHIP_SCALE
        ))

        self.world.asteroids.append(Asteroid(
            self.world,
            x, y - 30,
            Vector2(random() * 3.0 - 1.5, random() * -10),
            random() * 3.0,
            'resources/images/people/pilot.png', config.SHIP_SCALE
        ))
        self.world.asteroids.append(Asteroid(
            self.world,
            x + 30, y + 30,
            Vector2(random() * 6.0 + 3.0, random() * 6.0 + 3.0),
            random() * 3.0,
            'resources/images/people/gunner.png', config.SHIP_SCALE
        ))
        self.world.asteroids.append(Asteroid(
            self.world,
            x - 30, y + 30,
            Vector2(random() * -6.0 - 3.0, random() * 6.0 + 3.0),
            random() * 3.0,
            'resources/images/people/technician.png', config.SHIP_SCALE
        ))

    def is_live(self):
        return self.ship_state.state == ShipState.LIVE

    def has_recent_damage(self):
        return self.ship_state.has_recent_damage

    def collide(self, other, intensity=10.0, **kwargs):
        # TODO: Calculate the damage:
        # Collision between shield and bullet (sensor)
        # Collision between shield and everything else
        self.ship_state.damage(energy=10.0)

    def heal(self, amount):
        self.ship_state.heal(amount)
