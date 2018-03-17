import math

from Box2D import b2PolygonShape, b2FixtureDef
from mgl2d.input.game_controller import GameController

PROPULSION_INTENSITY = 360
SIDE_THRUST_INTENSITY = 5100


class PhysicsShip:
    def __init__(self, ship, physicsWorld, x, y, angle=0):
        w = 5
        h = 10
        self.shape = b2PolygonShape(vertices=[
            (0, -(h * 0.5)),
            (-w * 0.5, -(h * 0.5 - w * 0.5)),
            (-w * 0.5, -(-h * 0.5 + w * 0.3)),
            (-w * 0.25, -(-h * 0.5)),
            (w * 0.25, -(-h * 0.5)),
            (w * 0.5, -(-h * 0.5 + w * 0.3)),
            (w * 0.5, -(h * 0.5 - w * 0.5)),
        ])

        self.body = physicsWorld.CreateDynamicBody(
            position=(x, y),
            angle=math.radians(angle - 180),
            shapes=self.shape,
            angularDamping=4,
            linearDamping=0.1,
            shapeFixture=b2FixtureDef(density=2.0),
            userData={'type': 'ship', 'obj': ship, 'owner': id(ship)},
        )

    def update_forces(self, controller):
        if controller is None:
            return

        direction = self.body.GetWorldVector(localVector=(0.0, 1.0))
        pos = self.body.GetWorldPoint(localPoint=(0.0, 2.0))

        value = controller.get_axis(GameController.AXIS_TRIGGER_RIGHT) or 0.0
        intensity = value * PROPULSION_INTENSITY
        self.body.ApplyForce(direction * intensity, pos, True)

        value = controller.get_axis(GameController.AXIS_LEFT_X) or 0.0
        intensity = value * SIDE_THRUST_INTENSITY
        self.body.ApplyTorque(intensity, True)

        if controller.is_button_down(GameController.BUTTON_A):
            intensity = 50
            self.body.ApplyLinearImpulse(direction * intensity, pos, True)
