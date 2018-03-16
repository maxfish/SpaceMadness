import math

from mgl2d.graphics.shader import Shader
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2

from config import PHYSICS_SCALE
from game.entity import Entity
from physics.physics_asteroid import PhysicsAsteroid

IMAGE_SIZE = 100


class Asteroid(Entity):
    def __init__(
            self,
            world,
            x,
            y,
            speed,
            torque,
    ):
        super().__init__(world, x, y, 0)
        # Slightly smaller than the image
        radius = ((IMAGE_SIZE / PHYSICS_SCALE) / 2) * 0.8

        self._physicAsteroid = PhysicsAsteroid(
            self,
            world.physicsWorld,
            center=Vector2(x / PHYSICS_SCALE, y / PHYSICS_SCALE),
            radius=radius,
            speed=speed,
            torque=torque,
        )

        self._quad = QuadDrawable(x, y, IMAGE_SIZE, IMAGE_SIZE)
        self._quad.anchor = self._quad.scale / 2
        self._quad.texture = Texture.load_from_file('resources/images/asteroides/asteroid_01.png')
        self._quad.shader = Shader.from_files('resources/shaders/base.vert', 'resources/shaders/rgba.frag')

    def update(self, game_speed):
        self._physicAsteroid.update_forces()
        self._quad.pos = self._physicAsteroid.body.position * PHYSICS_SCALE
        self._quad.angle = math.degrees(self._physicAsteroid.body.angle)
        pass

    def draw(self, screen):
        self._quad.shader.bind()
        self._quad.shader.set_uniform_float('mul_r', 0.4)
        self._quad.shader.set_uniform_float('mul_g', 0.4)
        self._quad.shader.set_uniform_float('mul_b', 0.4)
        self._quad.draw(screen)
        pass

    def collide(self, *args):
        pass
