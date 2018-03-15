from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture

from game.stage import Stage
from game.planet import Planet


class StageBackground(Stage):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.quad = QuadDrawable(0, 0, width, height)
        self.quad.texture = Texture.load_from_file('resources/images/bg.png')

        # Init the list of planets
        self.planets = []
        for x in range(0, 10):
            p = Planet(width, height)
            self.planets.append(p)

    def get_width(self):
        return self.width

    def update(self, game_speed):
        pass

    def draw_background(self, surface, window_x, window_y):
        self.quad.draw(surface)

    def draw_foreground(self, surface, window_x, window_y):
        for planet in self.planets:
            draw_planet(planet, surface)


def draw_planet(planet, surface):
    planet.quad.draw(surface)
