from abc import ABC


class TurretState():
    fire_time_ms = 100
    ammo_clip_size = 20
    reload_time_ms = 1000
    recently_fired_ms = fire_time_ms

    def __init__(self, turret):
        self.turret = turret
        self._current_time_ms = 0
        self._state = TurretIdle(self)

        self.last_shot_time_ms = self._current_time_ms - self.fire_time_ms
        self.cur_loaded_ammo = self.ammo_clip_size

    def _time_since(self, past_time_ms):
        return self._current_time_ms - past_time_ms

    def _set_state(self, state=None):
        if state:
            self._state = state
        return self._state

    def fire(self):
        self._set_state(
            self._state.fire(),
        )

    def hold_fire(self):
        self._set_state(
            self._state.hold_fire(),
        )

    @property
    def has_recently_fired(self):
        return self._time_since(self.last_shot_time_ms) <= self.recently_fired_ms

    @property
    def is_reloading(self):
        return isinstance(self._state, TurretReloading)

    def advance_time(self, time_passed_ms):
        self._current_time_ms += time_passed_ms
        self._set_state(
            self._state.advanced_time(),
        )


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
        # print(self.__class__.__name__)
        pass

    @property
    def _current_time_ms(self):
        return self.sm._current_time_ms

    @property
    def _time_in_state(self):
        return self._time_since(self._state_init_time)

    def _time_since(self, past_time_ms):
        return self._current_time_ms - past_time_ms


class TurretIdle(_TurretState):
    def __init__(self, sm):
        super().__init__(sm)

    def fire(self):
        return TurretFiring(self.sm)


class TurretFiring(_TurretState):
    def __init__(self, sm):
        super().__init__(sm)

    def advanced_time(self):
        if self.sm.cur_loaded_ammo == 0:
            return TurretReloading(self.sm)

        if self._time_since(self.sm.last_shot_time_ms) >= self.sm.fire_time_ms:
            self._fire_bullet()

        return self

    def hold_fire(self):
        return TurretIdle(self.sm)

    def _fire_bullet(self):
        assert self.sm.cur_loaded_ammo > 0

        self.sm.last_shot_time_ms = self._current_time_ms
        self.sm.cur_loaded_ammo -= 1
        self.sm.turret.fire_bullet()
        # print("_fire_bullet")


class TurretReloading(_TurretState):
    def __init__(self, sm):
        super().__init__(sm)

    def advanced_time(self):
        if self._time_in_state >= self.sm.reload_time_ms:
            self._finish_reloading()
            return TurretIdle(self.sm)

    def _finish_reloading(self):
        self.sm.cur_loaded_ammo = self.sm.ammo_clip_size
