from Box2D import b2PolygonShape, b2CircleShape


class PhysicsBullet:
    def __init__(self, bullet, physics_world, x, y, r):
        self.body = physics_world.CreateDynamicBody(
            position=(x, y),
            shapes=b2CircleShape(radius=r),
            angularDamping=0,
            linearDamping=0,
            userData={'type': 'bullet', 'obj': bullet},
        )
