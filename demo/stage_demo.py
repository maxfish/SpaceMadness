from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

from game.stages.stage_sky import StageSky


class StageDemo(StageSky):
    def __init__(self, width, height):
        super().__init__(width, height)
        texture = Texture.load_from_file('resources/images/logo.png')
        self._logo = QuadDrawable(0, 0, texture.width, texture.height)
        self._logo.anchor = Vector2(texture.width / 2, texture.height / 2)
        self._logo.texture = texture

        self.hint.scale = Vector2(0, 0)

    def update(self, game_speed):
        self._logo.pos = Vector2(self.width / 2, self.height / 2)

    def draw_foreground(self, surface, window_x, window_y):
        super().draw_foreground(surface, window_x, window_y)

        self._logo.draw(surface)
