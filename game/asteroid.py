import math

from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2
from mgl2d.input.game_controller import GameController

from config import PHYSICS_SCALE
from game.entity import Entity
from game.shield import Shield
from game.turret import Turret
from physics.physics_asteroid import PhysicAsteroid

SCALE = 0.67


class Asteroid(Entity):
    def __init__(
            self,
            world,
            x,
            y,
            z=0,
    ):
        super().__init__(world, x, y, z)

        self._dim = Vector2(130 * SCALE, 344 * SCALE)
        self._angle = 0
        self._physicAsteroid = PhysicAsteroid(world.physicsWorld, x / PHYSICS_SCALE, y / PHYSICS_SCALE)

        # Used by ship components to scale themselves
        self.scale = SCALE

        self._quad = QuadDrawable(0, 0, self._dim.x, self._dim.y)
        self._quad.pos = self._position
        self._quad.anchor = self._dim.__div__(2.0)
        self._quad.texture = Texture.load_from_file('resources/images/ship/hull.png')

    def update(self, game_speed):
        pass

    def draw(self, screen):
        pass
