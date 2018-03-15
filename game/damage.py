from typing import Any

class Damage:

    def __init__(self, absorber: float) -> None:
        """
        absorber is a percentage of how much the force is absorbed
        """
        self.health = 1.0
        if absorber < 0.0 or absorber > 100.0:
            raise ValueError('Provide a value between 0.0 and 100.0')
        self.absorber = (100.0 - absorber) / 100.0

    def hit(self, force: float) -> None:
        damage = (force * 0.001) * self.absorber
        self.health = max(0.0, self.health - damage)
