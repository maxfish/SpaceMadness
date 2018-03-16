from Box2D import b2FixtureDef, b2CircleShape
import random

from mgl2d.math.vector2 import Vector2


class PhysicsAsteroid:
    def __init__(self, asteroid, physicsWorld, center, radius, speed, torque):
        self.shape = b2CircleShape(radius=radius)
        self.shape.local_position = Vector2(center.x, center.y)

        self.speed = speed
        self.body = physicsWorld.CreateDynamicBody(
            position=(center.x, center.y),
            shapes=self.shape,
            angularDamping=0,
            linearDamping=0,
            shapeFixture=b2FixtureDef(density=3.0),
            userData={'type': 'ship', 'obj': asteroid},
        )

        self.body.ApplyLinearImpulse(tuple(speed.to_list()), (0, 0), True)
        self.body.angularVelocity = torque

    def update_forces(self):
        pass
