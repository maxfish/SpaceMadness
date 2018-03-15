from Box2D import b2PolygonShape


class PhysicsGun:
    def __init__(self, gun, physics_world, x, y, w, l):
        self.body = physics_world.CreateDynamicBody(
            position=(x, y),
            angularDamping=4,
            linearDamping=0.1,
            shapes=b2PolygonShape(box=(w, l)),
            userData={'type': 'gun', obj: gun},
        )
