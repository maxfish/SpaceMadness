from abc import ABC


class TurretState():

    fire_time_ms = 250
    ammo_clip_size = 40
    reload_time_ms = 5000

    def __init__(self):
        self._current_time_ms = 0
        self._state = TurretIdle(self)

        self.last_shot_time_ms = self._current_time_ms - 1000000  # last fired in some imaginary past
        self.cur_loaded_ammo = self.ammo_clip_size

    def fire(self):
        self._state = self._state.fire()

    def hold_fire(self):
        self._state = self._state.hold_fire()

    def advance_time(self, time_passed_ms):
        self._current_time_ms += time_passed_ms
        self._state = self._state.advanced_time()


class _TurretState(ABC):
    """State Machine interface"""

    def __init__(self, sm):
        self.sm = sm
        self._state_init_time = self._current_time_ms
        self._entered()

    def fire(self):
        return self

    def hold_fire(self):
        return self

    def advanced_time(self):
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


class TurretIdle(_TurretState):

    def fire(self):
        return TurretFiring(self.sm)


class TurretFiring(_TurretState):

    def advanced_time(self):
        if self.sm.cur_loaded_ammo == 0:
            return TurretReloading(self.sm)

        if self._time_since(self.sm.last_shot_time_ms) >= self.sm.fire_time_ms:
            self._fire_bullet()

        return self

    def hold_fire(self):
        return TurretIdle(self.sm)

    def _fire_bullet(self):
        self.sm.last_shot_time_ms = self._current_time_ms
        print("_fire_bullet")


class TurretReloading(_TurretState):

    def advanced_time(self):
        if self._time_in_state >= self.sm.reload_time_ms:
            self._finish_reloading()
            return TurretIdle(self.sm)

    def _finish_reloading():
        self.sm.cur_loaded_ammo = self.sm.ammo_clip_size
        print("_finish_reloading")
