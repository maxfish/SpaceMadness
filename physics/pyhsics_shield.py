from Box2D import b2CircleShape
from Box2D import b2FixtureDef


class PhysicShield:

    def __init__(self, physicsWorld, center, radius):
        self.shape = b2CircleShape(radius=10.0)
        self.body = physicsWorld.CreateDynamicBody(
            position=(center.x, center.y),
            shapes=self.shape,
            angularDamping=5,
            linearDamping=0.1,
            shapeFixture=b2FixtureDef(density=2.0, isSensor=True),
        )
