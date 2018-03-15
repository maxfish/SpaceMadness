from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.shader import Shader

from mgl2d.math.vector2 import Vector2

class Laser:
    def __init__(self, x, y, length, angle):
        self.quadb = QuadDrawable(x, y, 36, 100)
        self.quadb.texture = Texture.load_from_file('resources/images/burst_b.png')
        self.quadm = QuadDrawable(x+36, y, 100, 100)
        self.quadm.texture = Texture.load_from_file('resources/images/burst_m.png')
        self.quade = QuadDrawable(x+136, y, 64, 100)
        self.quade.texture = Texture.load_from_file('resources/images/burst_e.png')

    def update(self, screen):
        pass

    def draw(self, screen):
        self.quad.draw(screen)
