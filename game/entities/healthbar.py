from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

from game.entities.ship_state import ShipState
from game.entity import Entity


class HealthBar(Entity):
    def __init__(self, ship, world):
        super().__init__(world, ship.position.x, ship.position.y)
        self._ship = ship
        self._quad = QuadDrawable(0, 0, ship._dim.x, 5)
        self._quad.texture = Texture.load_from_file('resources/images/health.png')

    def update(self, game_speed):
        self._quad.scale = Vector2(
            self._ship._dim.x * self._ship.ship_state.energy / ShipState.MAX_ENERGY,
            self._quad.scale.y,
        )
        self._quad.pos = self._position + Vector2(-self._ship._dim.x / 2, -self._ship._dim.y / 3)

    def draw(self, screen):
        self._quad.draw(screen)
