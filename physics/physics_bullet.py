from Box2D import b2PolygonShape


class PhysicsBullet:
    def __init__(self, physics_world, x, y, w, l):
        self.body = physics_world.CreateDynamicBody(
            position=(x, y),
            shapes=b2PolygonShape(box=(w, l)),
        )
