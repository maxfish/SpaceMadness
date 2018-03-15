from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from game.entity import Entity
from mgl2d.math.vector2 import Vector2
from os import listdir
from os.path import isfile, join


import random


class Planet:

    def __init__(self, width, height, planet_list):
        start_x = random.randint(0, width)
        start_y = random.randint(0, height)
        planet_number = random.randint(0, len(planet_list))

        size = 0
        area_size = random.randint(0, 100)
        if area_size < 20:
            size = random.randint(50, 150)
        elif area_size < 80:
            size = random.randint(150, 500)
        else:
            size = random.randint(500, 1000)


        self.pos = Vector2(start_x, start_y)
        self.speed_x = random.randint(-100, 100)
        self.speed_y = random.randint(-100, 100)
        self.quad = QuadDrawable(self.pos.x, self.pos.y, size, size)

        self.quad.texture = Texture.load_from_file('resources/images/planets/' + planet_list[planet_number - 1])

    def update(self, screen):
        self.pos.x += 0.0001*self.speed_x
        self.pos.y += 0.0001*self.speed_y
        self.speed_x += random.randint(-20, 20)
        self.speed_y += random.randint(-20, 20)
        self.quad.pos = self.pos

    def draw(self, screen):
        self.quad.draw(screen)

