from Box2D import b2CircleShape
from Box2D import b2FixtureDef


class PhysicsShield:
    def __init__(self, shield, physicsShip, physicsWorld, center, radius):
        self.shape = b2CircleShape(radius=radius)
        self.body = physicsWorld.CreateDynamicBody(
            position=(0, 0),
            shapes=self.shape,
            angularDamping=0,
            linearDamping=0,
            shapeFixture=b2FixtureDef(density=0.1, isSensor=True),
            userData={'type': 'shield', 'obj': shield, 'owner': id(shield._ship)},
        )
