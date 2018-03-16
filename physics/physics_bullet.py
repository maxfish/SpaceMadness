from Box2D import b2CircleShape
from Box2D import b2FixtureDef
from Box2D import b2PolygonShape


class PhysicsBullet:
    def __init__(self, bullet, physics_world, x, y, r, owner):
        self.body = physics_world.CreateDynamicBody(
            position=(x, y),
            shapes=b2CircleShape(radius=r),
            shapeFixture=b2FixtureDef(density=0.1, isSensor=True),
            angularDamping=0,
            linearDamping=0,
            userData={'type': 'bullet', 'obj': bullet, 'owner': owner},
        )
