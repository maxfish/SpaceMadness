from mgl2d.graphics.sprite import Sprite
from mgl2d.math.vector2 import Vector2


class Entity:
    def __init__(self, world, frames_store, x, y, z=0):
        self._world = world
        self._sprite = Sprite(frames_store)
        self._position = Vector2(x, y)
        self._z = z
        self.should_be_removed = False

    @property
    def position(self):
        return self._position

    @property
    def sprite(self):
        return self._sprite

    def draw(self, screen):
        self._sprite.x = self.position.x + self._world.window_x
        self._sprite.y = self.position.y + self._z + self._world.window_y
        self._sprite.draw(screen)

    def handle_input(self):
        pass

    def update(self, game_speed):
        self._sprite.x = self._position.x
        self._sprite.y = self._position.y
        self._sprite.update(game_speed)

    class State:
        def __init__(self):
            pass

        def enter(self, old_state):
            return

        def leave(self, new_state):
            return

        def update(self, game_speed):
            return
