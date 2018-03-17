import math

from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.shader import Shader
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

from config import SCREEN_WIDTH, SCREEN_HEIGHT, PHYSICS_SCALE
from game.entity import Entity
from physics.physics_asteroid import PhysicsAsteroid


class Asteroid(Entity):
    def __init__(
            self,
            world,
            x,
            y,
            speed,
            torque,
            asset='resources/images/asteroides/asteroid_01.png',
            scale=1,
    ):
        super().__init__(world, x, y, 0)
        # Slightly smaller than the image
        texture = Texture.load_from_file(asset)
        image_size = min(texture.width, texture.height)

        radius = ((image_size / PHYSICS_SCALE) / 2) * 0.8

        self._quad = QuadDrawable(x, y, texture.width * scale, texture.height * scale)
        self._quad.anchor = self._quad.scale / 2
        self._quad.texture = texture
        self._quad.shader = Shader.from_files('resources/shaders/base.vert', 'resources/shaders/rgba.frag')

        self._physicAsteroid = PhysicsAsteroid(
            self,
            world.physicsWorld,
            center=Vector2(x / PHYSICS_SCALE, y / PHYSICS_SCALE),
            radius=radius,
            speed=speed,
            torque=torque,
        )

    def update(self, game_speed):
        self._physicAsteroid.update_forces()
        self._quad.pos = self._physicAsteroid.body.position * PHYSICS_SCALE
        self._quad.angle = math.degrees(self._physicAsteroid.body.angle)
        pass

    def draw(self, screen):
        self._quad.shader.bind()
        self._quad.shader.set_uniform_float('mul_r', 0.3)
        self._quad.shader.set_uniform_float('mul_g', 0.3)
        self._quad.shader.set_uniform_float('mul_b', 0.3)
        self._quad.draw(screen)
        pass

    def collide(self, other, **kwargs):
        pass

    def destroy(self):
        goes_to_left = self._physicAsteroid.body.linearVelocity.x < 0
        goes_to_right = not goes_to_left
        goes_to_top = self._physicAsteroid.body.linearVelocity.y < 0
        goes_to_bottom = not goes_to_top

        return (goes_to_left and
                self._physicAsteroid.body.position.x <
                0 - self._physicAsteroid.shape.radius) or \
               (goes_to_right and
                (self._physicAsteroid.body.position.x * PHYSICS_SCALE >
                 SCREEN_WIDTH + self._physicAsteroid.shape.radius)) or \
               (goes_to_top and
                (self._physicAsteroid.body.position.y <
                 0 - self._physicAsteroid.shape.radius)) or \
               (goes_to_bottom and
                (self._physicAsteroid.body.position.y * PHYSICS_SCALE >
                 SCREEN_HEIGHT + - self._physicAsteroid.shape.radius))
