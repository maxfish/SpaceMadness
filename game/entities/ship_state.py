from config import SHIP_MAX_ENERGY


class ShipState:
    LIVE = 1
    DYING = 2
    DEAD = 3

    MAX_ENERGY = SHIP_MAX_ENERGY

    def __init__(self, ship):
        self.ship = ship
        self.energy = self.MAX_ENERGY
        self.time = 0
        self.last_damage_time = self.time
        self.state_time = self.time
        self.enter(self.LIVE)

    @property
    def time_in_state(self):
        return self.time_since(self.state_time)

    def time_since(self, past_time_ms):
        return self.time - past_time_ms

    @property
    def has_recent_damage(self):
        return self.time_since(self.last_damage_time) <= 40  # ms

    def update(self, time_passed_ms):
        self.time += time_passed_ms

        if self.state == self.DYING:
            self.ship.destroy_ship()
            self.enter(self.DEAD)

    def damage(self, energy):
        if self.state == self.LIVE:
            self.last_damage_time = self.time

            self.energy -= energy
            if self.energy <= 0:
                self.energy = 0
                self.enter(self.DYING)

    def enter(self, state):
        self.state = state
        self.state_time = self.time
