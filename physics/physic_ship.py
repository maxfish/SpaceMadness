from Box2D import b2PolygonShape


class PhysicShip:
    def __init__(self, physicsWorld, x, y):
        w = 20
        h = 50
        self.shape = b2PolygonShape(vertices=[
            (0, h * 0.5),
            (-w * 0.5, h * 0.5 - w * 0.5),
            (-w * 0.5, -h * 0.5 + w * 0.3),
            (-w * 0.25, -h * 0.5),
            (w * 0.25, -h * 0.5),
            (w * 0.5, -h * 0.5 + w * 0.3),
            (w * 0.5, h * 0.5 - w * 0.5),
        ])

        self.body = physicsWorld.CreateDynamicBody(
            position=(x, y),
            shapes=self.shape,
        )
