import math

from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2
from mgl2d.input.game_controller import GameController

from config import PHYSICS_SCALE
from game.entity import Entity
from game.shield import Shield
from game.turret import Turret
from physics.physics_asteroid import PhysicsAsteroid
from physics.physics_ship import PhysicsShip

SCALE = 0.67


class Asteroid(Entity):
    def __init__(
            self,
            world,
            x,
            y,
            speed_x,
            speed_y,
            z=0,
    ):
        super().__init__(world, x, y, z)

        size = 100;
        self._physicAsteroid = PhysicsAsteroid(
            self,
            world.physicsWorld,
            center=Vector2(x/PHYSICS_SCALE, y/PHYSICS_SCALE),
            radius=5.0,
            speed_x=speed_x,
            speed_y=speed_y
        )

        pos = self._physicAsteroid.body.position
        self._position = Vector2(pos[0] - 50, pos[1] - 50)

        self._quad = QuadDrawable(self._position.x, self._position.y, size, size)
        self._quad.texture = Texture.load_from_file('resources/images/asteroides/asteroid_01.png')

    def update(self, game_speed):
        self._physicAsteroid.update_forces()
        pos = self._physicAsteroid.body.position * PHYSICS_SCALE
        self._position = Vector2(pos[0] - 50, pos[1] - 50)
        self._quad.pos = self._position
        pass

    def draw(self, screen):
        self._quad.draw(screen)
        pass

    def collide(self, *args):
        pass

