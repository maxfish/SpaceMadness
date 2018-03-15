from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
import random


class Planet:

    def __init__(self, width, height):
        self.x_start = random.randint(0, width)
        self.y_start = random.randint(0, height)
        self.size = random.randint(100, 400)
        self.quad = QuadDrawable(self.x_start, self.y_start, self.size, self.size)
        self.speed = 1
        self.quad.texture = Texture.load_from_file('resources/images/planets/exoplanet.png')

