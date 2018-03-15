from game.shield import Shield
from game.ship import Ship

INTRO_DEBUG = 0
DEBUG = 0


# noinspection PyAttributeOutsideInit
class World:
    SCENE_NONE = 0
    SCENE_TITLE = 1
    SCENE_GAME = 2
    SCENE_GAME_OVER = 4

    def __init__(self, bounds, debug=0):
        self.scene = self.SCENE_TITLE

        self.bounds = bounds
        self.debug = debug

        self.window_x = 0
        self.window_y = 0

        self.stage = None

        ship = Ship(self, 1000, 500)
        shield = Shield(ship)

        self.players = [
            ship
        ]
        self.entities = [
            ship, shield
        ]

        # self.item_frames = FramesStore()
        # self.item_frames.load('resources/sprites/items', 'sprites.json')

    def set_stage(self, stage):
        self.stage = stage

    def restart_game(self):
        # This is not enough, you need to re-init players
        self.init(self.bounds, self.stage, self.debug)

    def begin(self):
        self.scene = self.SCENE_GAME
        # for character in self.characters:
        #     character.begin()

    def update(self, game_speed):
        self.stage.update(game_speed)

        # for i in self.items:
        #     i.update(game_speed)
        for e in self.entities:
            e.update(game_speed)

    def draw(self, screen):
        self.stage.draw_background(screen, self.window_x, self.window_y)

        # TODO: Draw objects
        for e in self.entities:
            e.draw(screen)

        self.stage.draw_foreground(screen, self.window_x, self.window_y)

    def game_over(self):
        self.scene = self.SCENE_GAME_OVER
