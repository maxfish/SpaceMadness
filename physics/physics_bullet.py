from Box2D import b2PolygonShape


class PhysicsBullet:
    def __init__(self, bullet, physics_world, x, y, w, l):
        self.body = physics_world.CreateDynamicBody(
            position=(x, y),
            shapes=b2PolygonShape(box=(w, l)),
            userData={'type': 'bullet', 'obj': bullet},
        )
