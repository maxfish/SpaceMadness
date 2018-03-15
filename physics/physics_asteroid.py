from Box2D import b2PolygonShape, b2FixtureDef, b2CircleShape
import random

from mgl2d.math.vector2 import Vector2

class PhysicsAsteroid:
    def __init__(self, asteroid, physicsWorld, x, y):

        self.shape = b2CircleShape()
        self.shape.radius = 200
        self.shape.local_position = Vector2(x, y)
        self.force_x = random.randint(0, 100) / 100
        self.force_y = random.randint(0, 100) / 100

        self.body = physicsWorld.CreateDynamicBody(
            position=(x, y),
            shapes=self.shape,
            angularDamping=1,
            linearDamping=1,
            shapeFixture=b2FixtureDef(density=1.0),
        )
        self.force_x = random.randint(0, 100) / 100
        self.force_y = random.randint(0, 100) / 100

        """w=5
        h=5

        self.shape = b2PolygonShape(vertices=[
            (0, -(h * 0.5)),
            (-w * 0.5, -(h * 0.5 - w * 0.5)),
            (-w * 0.5, -(-h * 0.5 + w * 0.3)),
            (-w * 0.25, -(-h * 0.5)),
            (w * 0.25, -(-h * 0.5)),
            (w * 0.5, -(-h * 0.5 + w * 0.3)),
            (w * 0.5, -(h * 0.5 - w * 0.5)),
        ])

        self.body = physicsWorld.CreateDynamicBody(
            position=(x, y),
            shapes=self.shape,
            angularDamping=4,
            linearDamping=0.1,
            shapeFixture=b2FixtureDef(density=2.0),
            userData={'type': 'ship', 'obj': asteroid},
        )"""

        self.dir = self.body.GetWorldVector(localVector=(self.force_x, self.force_y))

    def update_forces(self):
        pos = self.body.GetWorldPoint(localPoint=(0.0, 1.0))
        self.body.ApplyForce(self.dir * 1, pos, True)

