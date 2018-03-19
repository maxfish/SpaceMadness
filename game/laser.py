from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture

from mgl2d.math.vector2 import Vector2


class Laser:
    def __init__(self, x, y, length, angle):
        # self.quadb = QuadDrawable(x, y, 36/8, 100/8, angle)
        # self.quadb.texture = Texture.load_from_file('resources/images/burst_b.png')
        self.quadm = QuadDrawable(x + 36 / 8, y, length, 100 / 8, angle)
        self.quadm.texture = Texture.load_from_file('resources/images/burst_m.png')
        # self.quade = QuadDrawable(x+36/8+100-4, y, 64/8, 100/8, angle)
        # self.quade.texture = Texture.load_from_file('resources/images/burst_e.png')
        self.should_be_removed = False

    def update(self, screen):
        self.quadm.size = Vector2(self.quadm.scale.x, self.quadm.scale.y * 0.9)
        if self.quadm.scale.x < 0.01:
            self.should_be_removed = True
            self.quadm.size = Vector2(0, 0)

    def draw(self, screen):
        # self.quadb.draw(screen)
        self.quadm.draw(screen)
        # self.quade.draw(screen)
