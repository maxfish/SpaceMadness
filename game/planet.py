from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.shader import Shader

from mgl2d.math.vector2 import Vector2

import random


class Planet:

    def __init__(self, width, height, planet_list):
        start_x = width/2 + random.randint(-width/2, width/2)
        start_y = height/2 + random.randint(-height/2, height/2)
        planet_number = random.randint(0, len(planet_list))
        size = calculate_size(width, height)
        self.pos = Vector2(start_x, start_y)
        self.speed_x = random.randint(-100, 100)
        self.speed_y = random.randint(-100, 100)

        create_planet_quad(self, size, planet_list, planet_number)

    def update(self, screen):
        self.pos.x += 0.00005*self.speed_x
        self.pos.y += 0.00005*self.speed_y
        self.speed_x += random.randint(-20, 20)
        self.speed_y += random.randint(-20, 20)
        self.quad.pos = self.pos

    def draw(self, screen):
        self.quad.draw(screen)


def calculate_size(width, height):
    percentage = random.randint(0, 100)
    scale = (width+height) / 2
    if percentage < 40:
        size = random.randint(scale * 0.075, scale * 0.15)
    elif percentage < 90:
        size = random.randint(scale * 0.15, scale * 0.25)
    else:
        size = random.randint(scale * 0.25, scale * 0.35)
    return size


def create_planet_quad(planet, size, planet_list, planet_picked):
    planet.quad = QuadDrawable(planet.pos.x, planet.pos.y, size, size)
    planet.quad.texture = Texture.load_from_file('resources/images/planets/' + planet_list[planet_picked - 1])
    planet.quad.shader = Shader.from_files('resources/shaders/base.vert', 'resources/shaders/base.frag')