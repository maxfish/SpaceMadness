from Box2D import b2CircleShape
from Box2D import b2FixtureDef


class PhysicsShield:
    def __init__(self, shield, physicsWorld, center, radius):
        self.shape = b2CircleShape(radius=radius)
        self.body = physicsWorld.CreateDynamicBody(
            position=(center.x, center.y),
            shapes=self.shape,
            angularDamping=5,
            linearDamping=0.1,
            shapeFixture=b2FixtureDef(density=2.0, isSensor=True),
            userData={'type': 'shield', 'obj': shield, 'owner': id(shield._ship)},
        )
