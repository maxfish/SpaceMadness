import math
from game.entity import Entity
from game.laser import Laser
from mgl2d.graphics.texture import Texture
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2
from game.shield_state import ShieldState


SHIP_SCALE = Vector2(109, 156)

INERTIA = True


# copied from game.py
GAME_FPS = 50
GAME_FRAME_MS = 1000 / GAME_FPS


class Shield(Entity):
    def __init__(self, ship):
        super().__init__(ship._world, 0, 0)

        self._ship = ship
        self._position = self._ship.position
        self._angle = 0

        # self._rad1 = ship._dim.x / 1.8
        self._rad1 = ship._dim.y / 2.9
        self._rad2 = ship._dim.y / 2.9
        self._angle = 0
        self._angle_speed = 1

        self._quad = QuadDrawable(0, 0, 0, 0)
        self._quad.scale = SHIP_SCALE
        self._quad.texture = Texture.load_from_file('resources/images/shield_arc.png')
        self._quad.anchor = Vector2(109/2, 156/2)

        self._charge = 0
        self.shield_state = ShieldState(self)
        self.update(0, (0.0, 0.0, 0.0))


    def calc_angle(self, x, y):
        if INERTIA:
            mag = math.sqrt(x*x+y*y)
            self._angle_speed = max(1, self._angle_speed * mag)

            if mag > 0.001:
                theta = math.degrees(math.atan2(y, x))
                self._angle_speed = min(self._angle_speed * 1.01, 6)
            else:
                return self._angle

            delta = theta - self._angle
            delta = (delta + 180) % 360 - 180
            step = delta * self._angle_speed / 8.0
            return self._angle + step
        else:
            return math.degrees(math.atan2(y, x))

    def update(self, game_speed, input_values):
        x, y, trigger = input_values
        if input_values == (0.0, 0.0, 0.0):
            # If the shields aren't being used, don't display them
            self._quad.scale = Vector2(0, 0)
        else:
            self._quad.scale = SHIP_SCALE
            self.update_angle_position(x, y)
            self.update_charge(trigger)

        self.shield_state.advance_time(
            time_passed_ms=(game_speed * GAME_FRAME_MS),
        )


    def update_angle_position(self, x, y):
        self._angle = self.calc_angle(x, y)

        pos = Vector2(
            math.cos(math.radians(self._angle)),
            math.sin(math.radians(self._angle)),
        )
        # pos = Vector2(
        #     pos.x * math.cos(math.radians(self._ship._angle)) - \
        #     pos.y * math.sin(math.radians(self._ship._angle)),
        #     pos.x * math.sin(math.radians(self._ship._angle)) + \
        #     pos.y * math.cos(math.radians(self._ship._angle)),
        # )

        self._position = \
            self._ship._position + \
            Vector2(pos.x * self._rad1, pos.y * self._rad2)

        self._quad.pos = self._position
        # self._quad.angle = self._angle + self._ship._angle
        self._quad.angle = self._angle

    def update_charge(self, trigger):
        if trigger > 0:
            self._charge += trigger
        else:
            self._charge -= 0.4
            if self._charge < 0:
                self._charge = 0

        if self._charge >= 50:
            self._charge = 0
            self._world.entities.append(
                Laser(self.position.x, self.position.y, 1000, self._angle),
            )

        self._quad.scale = Vector2(
            SHIP_SCALE.x * (1.0 + 2*self._charge/55.0),
            SHIP_SCALE.y * (1.0 - self._charge/55.0),
        )

    def draw(self, screen):
        if self.shield_state.is_healthy:
            self._quad.draw(screen)

    def collide(self, other, began):
        self.shield_state.damage(energy=10.0)
