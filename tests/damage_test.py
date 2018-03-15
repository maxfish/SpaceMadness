import pytest

from game import damage


def test_damage():
    force = 10.0
    absorber = 10.0

    dmg = damage.Damage(absorber=absorber)
    dmg.hit(force)

    expected = 1.0 - ((force * 0.001) * ((100.0 - absorber) / 100.0))
    assert dmg.health == pytest.approx(expected)


def test_damage_destroyed():
    dmg = damage.Damage(absorber=0.0)
    dmg.hit(1000.0)
    assert dmg.health == 0.0
