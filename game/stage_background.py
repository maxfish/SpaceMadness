from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture

from game.stage import Stage
from game.planet import Planet
from os import listdir
from os.path import isfile, join


class StageBackground(Stage):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.quad = QuadDrawable(0, 0, width, height)
        self.quad.texture = Texture.load_from_file('resources/images/bg.png')

        # Get all the planets pictures
        planet_picture_list = [f for f in listdir('resources/images/planets') if
                               isfile(join('resources/images/planets', f))]

        # Init the list of planets
        self.planets = []
        for x in range(0, 10):
            p = Planet(width, height, planet_picture_list)
            self.planets.append(p)

    def get_width(self):
        return self.width

    def update(self, game_speed):
        for planet in self.planets:
            planet.update(game_speed)

    def draw_background(self, surface, window_x, window_y):
        self.quad.draw(surface)
        for planet in self.planets:
            planet.draw(surface)

    def draw_foreground(self, surface, window_x, window_y):
        pass
