from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture

from game.stage import Stage


class Stage1(Stage):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.quad = QuadDrawable(0, 0, width, height)
        self.quad.texture = Texture.load_from_file('resources/images/bg.png')

    def get_width(self):
        return self.width

    def update(self, game_speed):
        pass

    def draw_background(self, surface, window_x, window_y):
        self.quad.draw(surface)

    def draw_foreground(self, surface, window_x, window_y):
        pass
