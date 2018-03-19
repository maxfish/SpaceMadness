import random

from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.shader import Shader
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2


class Cloud:
    def __init__(self, width, height, cloud_list):
        start_x = random.randint(0, width)
        start_y = random.randint(0, height)
        cloud_number = random.randint(0, len(cloud_list))

        size = calculate_size(width, height)
        self.pos = Vector2(start_x, start_y)
        self.speed_x = random.randint(-100, 100)
        self.speed_y = random.randint(-100, 100)

        self.quad = None
        create_cloud_quad(self, size, cloud_list, cloud_number)

    def update(self, screen):
        self.pos.x += 0.002 * self.speed_x
        self.pos.y += 0.002 * self.speed_y
        self.quad.pos = self.pos

    def draw(self, screen):
        self.quad.shader.bind()
        self.quad.shader.set_uniform_1f('mul_a', 0.4)
        self.quad.draw(screen)


def calculate_size(width, height):
    percentage = random.randint(0, 100)
    scale = (width + height) / 2
    if percentage < 40:
        size = random.randint(scale * 0.3, scale * 0.5)
    elif percentage < 90:
        size = random.randint(scale * 0.5, scale * 0.7)
    else:
        size = random.randint(scale * 0.7, scale * 0.9)
    return size


def create_cloud_quad(cloud, size, cloud_list, cloud_picked):
    cloud.quad = QuadDrawable(cloud.pos.x, cloud.pos.y, size, size, angle=random.randint(0, 360))
    cloud.quad.texture = Texture.load_from_file('resources/images/clouds/' + cloud_list[cloud_picked - 1])
    cloud.quad.shader = Shader.from_files('resources/shaders/base.vert', 'resources/shaders/rgba.frag')
    cloud.quad.anchor_to_center()
