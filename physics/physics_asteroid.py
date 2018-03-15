from Box2D import b2FixtureDef, b2CircleShape
import random

from mgl2d.math.vector2 import Vector2


class PhysicsAsteroid:
    def __init__(self, asteroid, physicsWorld, center, radius, speed_x, speed_y):
        self.shape = b2CircleShape(radius=radius)
        self.shape.local_position = Vector2(center.x, center.y)

        self.body = physicsWorld.CreateDynamicBody(
            position=(center.x, center.y),
            shapes=self.shape,
            angularDamping=5,
            linearDamping=0.1,
            shapeFixture=b2FixtureDef(density=1.0),
            userData={'type': 'ship', 'obj': asteroid},
        )

        self.dir = self.body.GetWorldVector(localVector=(speed_x, speed_y))


    def update_forces(self):
        pos = self.body.GetWorldPoint(localPoint=(0.0, 1.0))
        self.body.ApplyForce(self.dir * 100, pos, True)

