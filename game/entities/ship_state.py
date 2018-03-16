class ShipState:
    LIVE = 1
    DYING = 2
    DEAD = 3

    MAX_ENERGY = 100000000000000.0

    def __init__(self, ship):
        self.ship = ship
        self.energy = self.MAX_ENERGY
        self.time = 0
        self.enter(self.LIVE)

    def update(self, game_speed):
        self.time += game_speed

        if self.state == self.DYING:
            if self.state_time + 1 < self.time:
                self.enter(self.DEAD)

    def damage(self, energy):
        self.energy -= energy
        print(self.energy)

        if self.energy <= 0:
            self.energy = 0
            self.enter(self.DYING)

    def enter(self, state):
        self.state = state
        self.state_time = self.time
