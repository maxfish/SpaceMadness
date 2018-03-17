from abc import ABC

from config import SHIELD_MAX_ENERGY


class ShieldState():
    max_energy = SHIELD_MAX_ENERGY
    recharge_per_s = 2.0  # energy recharged per s on healthy shield
    restore_time_s = 20  # seconds to restore damaged shield
    restore_energy = 50.0  # how much energy shields have when restored

    def __init__(self, shield):
        self.shield = shield
        self._current_time_ms = 0
        self._state = ShieldHealthy(self)

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
        return isinstance(self._state, ShieldHealthy)


class _ShieldState(ABC):
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
        pass

    @property
    def _current_time_ms(self):
        return self.sm._current_time_ms

    @property
    def _time_in_state(self):
        return self._time_since(self._state_init_time)

    def _time_since(self, past_time_ms):
        return self._current_time_ms - past_time_ms


class ShieldHealthy(_ShieldState):
    def damage(self, energy):
        self.sm.cur_energy = max(
            0,
            self.sm.cur_energy - energy
        )
        if self.sm.cur_energy == 0:
            return ShieldRestoring(self.sm)

    def advanced_time(self, time_passed_ms):
        time_passed_s = time_passed_ms / 1000
        self.sm.cur_energy = min(
            self.sm.max_energy,
            self.sm.cur_energy + (time_passed_s * self.sm.recharge_per_s)
        )


class ShieldRestoring(_ShieldState):
    def advanced_time(self, time_passed_ms):
        restore_time_ms = self.sm.restore_time_s * 1000
        if self._time_in_state >= restore_time_ms:
            self._restore_shield()
            return ShieldHealthy(self.sm)

    def _restore_shield(self):
        self.sm.cur_energy = self.sm.restore_energy
