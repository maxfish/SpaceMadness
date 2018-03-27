from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

from game.entity import Entity
from physic_config import PhysicConfig


class SideTrail(Entity):
    def __init__(self, ship, offset_x, offset_y, offset_angle):
        self._ship = ship
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_angle = offset_angle

        self.side_trail_dimensions = Vector2(56 * self._ship.size, 11 * self._ship.size)
        self.side_trail = QuadDrawable(0, 0, self.side_trail_dimensions.x, self.side_trail_dimensions.y)
        self.side_trail.texture = Texture.load_from_file('resources/images/ship/side_trail.png')
        self.side_trail.anchor = Vector2(56 * self._ship.size, 5 * self._ship.size)
        self.side_trail.angle = offset_angle

        self.update(0, 0)

    def draw(self, screen):
        self.side_trail.draw(screen)

    def update(self, game_speed, axis):
        if axis > 0:
            self.side_trail.size = self.side_trail_dimensions
            self.side_trail.pos = PhysicConfig.ptm_ratio * (
                self._ship._physicsShip.body.transform * (
                self.offset_x / PhysicConfig.ptm_ratio, self.offset_y / PhysicConfig.ptm_ratio))
            self.side_trail.angle = self.offset_angle + self._ship._quad.angle
        else:
            self.side_trail.size = Vector2(0, 0)
