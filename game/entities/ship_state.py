class ShipState:
    LIVE = 1
    DYING = 2
    DEAD = 3

    MAX_ENERGY = 1000.0
    DYING_TIME_MS = 2000

    def __init__(self, ship):
        self.ship = ship
        self.energy = self.MAX_ENERGY
        self.time = 0
        self.state_time = self.time
        self.enter(self.LIVE)

    @property
    def time_in_state(self):
        return self.time_since(self.state_time)

    def time_since(self, past_time_ms):
        return self.time - past_time_ms

    def update(self, time_passed_ms):
        self.time += time_passed_ms

        if self.state == self.DYING:
            if self.time_in_state >= self.DYING_TIME_MS:
                self.enter(self.DEAD)

    def damage(self, energy):
        if self.state == self.LIVE:
            self.energy -= energy
            if self.energy <= 0:
                self.energy = 0
                self.enter(self.DYING)

    def enter(self, state):
        self.state = state
        self.state_time = self.time
