from mgl2d.graphics.sprite import Sprite
from mgl2d.math.vector2 import Vector2


class Entity:
    def __init__(self, world, x, y, z=0):
        self._world = world
        self._position = Vector2(x, y)
        self._z = z
        self.should_be_removed = False

    @property
    def position(self):
        return self._position

    def draw(self, screen):
        pass

    def handle_input(self):
        pass

    def update(self, game_speed):
        pass

    class State:
        def __init__(self):
            pass

        def enter(self, old_state):
            return

        def leave(self, new_state):
            return

        def update(self, game_speed):
            return
