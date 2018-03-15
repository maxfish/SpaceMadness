from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

from game.stage import Stage
from game.planet import Planet
from game.cloud import Cloud
from os import listdir
from os.path import isfile, join


class StageBackground(Stage):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.quad = QuadDrawable(0, 0, width, height)
        self.quad.texture = Texture.load_from_file('resources/images/bg.png')
        number_of_planets = 15
        self.planets = []
        number_of_clouds_background = 10
        number_of_clouds_foreground = 10

        self.clouds_background = []
        self.clouds_foreground = []


        # Generate the list of planets
        self.generate_planets(number_of_planets, width, height)
        # Generate the list of clouds
        self.generate_clouds_background(number_of_clouds_background, width, height)
        self.generate_clouds_foreground(number_of_clouds_foreground, width, height)


        self.hint = QuadDrawable(100, 800, 1000, 200)
        self.hint.texture = Texture.load_from_file('resources/images/hint.png')

    def get_width(self):
        return self.width

    def update(self, game_speed):
        for planet in self.planets:
            planet.update(game_speed)
        for cloud in self.clouds_foreground:
            cloud.update(game_speed)
        for cloud in self.clouds_background:
            cloud.update(game_speed)

    def draw_background(self, surface, window_x, window_y):
        self.quad.draw(surface)
        for planet in self.planets:
            planet.draw(surface)
        for cloud in self.clouds_background:
            cloud.draw(surface)

        self.hint.draw(surface)

    def draw_foreground(self, surface, window_x, window_y):
        for cloud in self.clouds_foreground:
            cloud.draw(surface)

    def generate_planets(self, number_of_planets, width, height):
        planet_picture_list = [f for f in listdir('resources/images/planets') if
                               isfile(join('resources/images/planets', f))]
        number_per_areas = number_of_planets // 4
        for x in range(0, number_per_areas):
            p = Planet(width/2, height/2, width, height, planet_picture_list)
            self.planets.append(p)
        for x in range(number_per_areas, number_per_areas*2):
            p = Planet(width/2, 0, width, height, planet_picture_list)
            self.planets.append(p)
        for x in range(number_per_areas*2, number_per_areas * 3):
            p = Planet(0, height/2, width, height, planet_picture_list)
            self.planets.append(p)
        for x in range(number_per_areas*3, number_per_areas * 4):
            p = Planet(0, 0, width, height, planet_picture_list)
            self.planets.append(p)

    def generate_clouds_background(self, number_of_clouds, width, height):
        planet_picture_list = [f for f in listdir('resources/images/clouds') if
                               isfile(join('resources/images/clouds', f))]
        for x in range(0, number_of_clouds):
            cloud = Cloud(width, height, planet_picture_list)
            self.clouds_background.append(cloud)

    def generate_clouds_foreground(self, number_of_clouds, width, height):
        planet_picture_list = [f for f in listdir('resources/images/clouds') if
                               isfile(join('resources/images/clouds', f))]
        for x in range(0, number_of_clouds):
            cloud = Cloud(width, height, planet_picture_list)
            self.clouds_foreground.append(cloud)
