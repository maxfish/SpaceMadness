from Box2D import b2PolygonShape, b2FixtureDef
from mgl2d.input.game_controller import GameController


class PhysicShip:
    def __init__(self, physicsWorld, x, y):
        w = 5
        h = 10
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
            angularDamping=5,
            linearDamping=0.1,
            shapeFixture=b2FixtureDef(density=2.0),
        )

    def update_forces(self, controller):
        controller.update()
        dir = self.body.GetWorldVector(localVector=(0.0, 1.0))
        pos = self.body.GetWorldPoint(localPoint=(0.0, 2.0))
        intensity = controller.get_axis(GameController.AXIS_TRIGGER_RIGHT) * 200
        self.body.ApplyForce(dir * intensity, pos, True)

        intensity = controller.get_axis(GameController.AXIS_LEFT_X) * 300
        self.body.ApplyTorque(-intensity, True)
