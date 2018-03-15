from abc import ABC


class ShipState():

    max_energy = 100.0

    def __init__(self, ship):
        self.ship = ship
        self._current_time_ms = 0
        self._state = ShipHealthy(self)

        self.cur_energy = self.max_energy

    def _set_state(self, state=None):
        if state:
            self._state = state
        return self._state

    def damage(self, energy):
        self._set_state(
            self._state.damage(energy),
        )

    def advance_time(self, time_passed_ms):
        self._current_time_ms += time_passed_ms
        self._set_state(
            self._state.advanced_time(time_passed_ms),
        )

    @property
    def is_healthy(self):
        return isinstance(self._state, ShipHealthy)


class _ShipState(ABC):
    """State Machine interface"""

    def __init__(self, sm):
        self.sm = sm
        self._state_init_time = self._current_time_ms
        self._entered()

    def damage(self, energy):
        return self

    def advanced_time(self, time_passed_ms):
        return self

    def _entered(self):
        print(self.__class__.__name__)

    @property
    def _current_time_ms(self):
        return self.sm._current_time_ms

    @property
    def _time_in_state(self):
        return self._time_since(self._state_init_time)

    def _time_since(self, past_time_ms):
        return self._current_time_ms - past_time_ms


class ShipHealthy(_ShipState):

    def damage(self, energy):
        self.sm.cur_energy = max(
            0,
            self.sm.cur_energy - energy
        )
        if self.sm.cur_energy == 0:
            return ShipDestroyed(self.sm)


class ShipDestroyed(_ShipState):
    pass
