import math

from Box2D import b2Vec2
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.shader_program import ShaderProgram
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

import config
from config import PHYSICS_SCALE
from game.entities.shield_state import ShieldState
from game.entity import Entity
from physics.physics_shield import PhysicsShield

SHIP_SIZE = Vector2(109, 156)
HALF_ARC_DEGREES = 40
INERTIA = True


class Shield(Entity):
    def __init__(self, ship, world):
        super().__init__(ship._world, 0, 0)
        self._ship = ship

        self._quad = QuadDrawable(0, 0, 0, 0)
        self._quad.texture = Texture.load_from_file('resources/images/shield_arc.png')
        self._quad.shader = ShaderProgram.from_files(vert_file='resources/shaders/base.vert', frag_file='resources/shaders/rgba.frag')
        self._quad.size = Vector2(self._quad.texture.width, self._quad.texture.height) * 0.67
        self._quad.anchor = Vector2(0, self._quad.size.y / 2)

        self._physicsShield = PhysicsShield(
            self,
            ship._physicsShip,
            world.physicsWorld,
            center=self._ship._physicsShip.body.position,
            radius=(self._quad.size.x / PHYSICS_SCALE) * 1.1,
        )
        self._collision_timer = 0

        self._rad1 = ship._dim.y / 2.9
        self._rad2 = ship._dim.y / 2.9
        self._angle = 0
        self._angle_speed = 1
        self._enable = False
        self._charge = 0
        self.shield_state = ShieldState(self)
        self.update(0, (0.0, 0.0, 0.0))

    def calc_angle(self, x, y):
        if INERTIA:
            mag = math.sqrt(x * x + y * y)
            self._angle_speed = max(1, self._angle_speed * mag)

            if mag > 0.001:
                theta = math.atan2(y, x)
                self._angle_speed = min(self._angle_speed * 1.01, 6)
            else:
                return self._angle

            delta = theta - self._angle
            delta = (delta + math.pi) % (2*math.pi) - math.pi
            step = delta * self._angle_speed / 8.0
            return self._angle + step
        else:
            return math.atan2(y, x)

    def update(self, game_speed, input_values):
        x, y, trigger = input_values
        if input_values == (0.0, 0.0, 0.0):
            # If the shields aren't being used, don't display them
            self._enable = False
        else:
            self._enable = True
            self.update_angle_position(x, y)

        self._physicsShield.body.position = self._ship._physicsShip.body.position
        self.shield_state.advance_time(
            time_passed_ms=(game_speed * config.GAME_FRAME_MS),
        )
        self._collision_timer -= game_speed * config.GAME_FRAME_MS

    def update_angle_position(self, x, y):
        self._angle = self.calc_angle(x, y)
        self._quad.pos = self._ship._position
        self._quad.angle = self._angle

    def draw(self, screen):
        if not self._enable:
            return

        self._quad.shader.bind()
        if self._collision_timer > 0:
            self._quad.shader.set_uniform_1f('mul_r', 0)
            self._quad.shader.set_uniform_1f('mul_g', 0.8)
            self._quad.shader.set_uniform_1f('mul_b', 0.8)
        else:
            self._quad.shader.set_uniform_1f('mul_g', 0)
            self._quad.shader.set_uniform_1f('mul_b', 1)
            self._quad.shader.set_uniform_1f('mul_r', 1)

        # if self.shield_state.is_healthy:
        self._quad.draw(screen)

    def collide(self, other, intensity=0.0, began=False, **kwargs):
        if not self._enable:
            return

        body = kwargs['body']
        other_body = kwargs['other_body']
        # Collision between shield and everything else
        self.shield_state.damage(energy=10.0)
        # Heal the ship so it has a purpose -- take less damage
        # self._ship.heal(5.0)
        if began:
            incoming_pos = other_body.position
            vector = incoming_pos - body.position
            direction = b2Vec2(vector.x, vector.y)
            direction.Normalize()
            incoming_angle = math.atan2(direction.y, direction.x)
            incoming_angle = (incoming_angle + math.pi*2) % (math.pi*2)
            shield_angle = (self._angle + math.pi*2) % (math.pi*2)
            shield_angle2 = (self._angle + math.pi*2) % (math.pi*2) + (math.pi*2)
            shield_angle3 = (self._angle + math.pi*2) % (math.pi*2) - (math.pi*2)
            if (shield_angle - HALF_ARC_DEGREES < incoming_angle < shield_angle + HALF_ARC_DEGREES) or \
                    (shield_angle2 - HALF_ARC_DEGREES < incoming_angle < shield_angle2 + HALF_ARC_DEGREES) or \
                    (shield_angle3 - HALF_ARC_DEGREES < incoming_angle < shield_angle3 + HALF_ARC_DEGREES):
                self._collision_timer = 400
