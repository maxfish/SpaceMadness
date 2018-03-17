from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.shader import Shader
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

from game.entity import Entity


class Trail(Entity):
    def __init__(self, ship, offset_x, offset_y):
        self._isBoosting = False
        self._ship = ship
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.engine_trail_dimensions = Vector2(130 * self._ship.scale, 344 * self._ship.scale)
        self.engine_trail = QuadDrawable(0, 0, self.engine_trail_dimensions.x, self.engine_trail_dimensions.y)
        self.engine_trail.texture = Texture.load_from_file('resources/images/ship/trail.png')
        # Don't ask why 173...
        self.engine_trail.anchor = Vector2(65 * self._ship.scale, 173 * self._ship.scale)
        self.engine_trail.shader = Shader.from_files('resources/shaders/base.vert', 'resources/shaders/rgba.frag')

        self.update(0, 0, False)

    def draw(self, screen):
        self.engine_trail.shader.bind()

        self.engine_trail.shader.set_uniform_float('mul_r', 0 if self._isBoosting else 0.49)
        self.engine_trail.shader.set_uniform_float('mul_g', .9 if self._isBoosting else 0.332)
        self.engine_trail.shader.set_uniform_float('mul_b', .9 if self._isBoosting else 0.059)

        self.engine_trail.draw(screen)

    def update(self, game_speed, trigger_intensity, boost):
        self._isBoosting = boost
        """`trigger_intensity` is a number from 0 to 1 representing how much a player is
        pressing the controller's right trigger.
        """
        self.engine_trail.scale = self.engine_trail_dimensions * (1 if boost else trigger_intensity)
        self.engine_trail.pos = Vector2(
            self._ship._quad.pos.x + self.offset_x,
            self._ship._quad.pos.y + self.offset_y,
        )
        self.engine_trail.angle = self._ship._quad._angle
