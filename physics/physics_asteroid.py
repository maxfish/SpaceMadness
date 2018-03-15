from Box2D import b2PolygonShape, b2FixtureDef, b2CircleShape
import random

from mgl2d.math.vector2 import Vector2

class PhysicAsteroid:
    def __init__(self, physicsWorld, x, y):

        self.shape = b2CircleShape
        self.shape.radius = 100
        #self.shape.setLocalPosition(Vector2(x, y))
        self.force_x = random.randint(0, 100) / 100
        self.force_y = random.randint(0, 100) / 100

        self.body = physicsWorld.CreateDynamicBody(
        )

        self.dir = self.body.GetWorldVector(localVector=(self.force_x, self.force_y))

    def update_forces(self):
        pos = self.body.GetWorldPoint(localPoint=(0.0, 2.0))
        self.body.ApplyForce(self.dir * 0.5, pos, True)
        pass
