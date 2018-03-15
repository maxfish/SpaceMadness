from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture

from game.stage import Stage
from game.entity import Entity

class Turret(Entity):

    def __init__(self, world, x, y, z=0):
        self.x = x
        self.y = y
        self.turret_quad = QuadDrawable(self.x, self.y, 13, 46)
        self.turret_quad.texture = Texture.load_from_file('resources/images/guns/minigun_right.png')

    def fire(self):
        print("FIRE!")

    def draw(self, screen):
        self.turret_quad.draw(screen)

    def update(self, game_speed):
        old_angle = self.turret_quad.angle
        self.turret_quad.angle = old_angle + 1


class TurretStage(Stage):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.quad = QuadDrawable(0, 0, width, height)
        self.quad.texture = Texture.load_from_file('resources/images/bg.png')
        self.turret = Turret(None, 100, 100)


    def get_width(self):
        return self.width

    def update(self, game_speed):
        self.turret.update(game_speed)

    def draw_background(self, surface, window_x, window_y):
        self.quad.draw(surface)

    def draw_foreground(self, surface, window_x, window_y):
        self.turret.draw(surface)
