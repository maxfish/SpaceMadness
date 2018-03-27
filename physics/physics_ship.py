from Box2D import b2PolygonShape, b2FixtureDef
from mgl2d.input.game_controller import GameController

from physic_config import PhysicConfig

PROPULSION_INTENSITY = 120
LATERAL_PROPULSION_INTENSITY = 60
SIDE_THRUST_MAX_TORQUE = 180
BOOST_IMPULSE = 2


class PhysicsShip:
    def __init__(self, ship, physicsWorld, x, y, angle=0):
        config_body = PhysicConfig.bodies['ship']
        config_fixture = config_body['fixtures'][0]
        f = (1 / PhysicConfig.ptm_ratio) * 0.67
        self.shapes = [b2PolygonShape(vertices=self.scale(polygon, f)) for polygon in config_fixture['polygon']]
        self.body = physicsWorld.CreateDynamicBody(
            position=(x, y),
            angle=angle,
            shapes=self.shapes,
            angularDamping=config_body['angular_damping'],
            linearDamping=config_body['linear_damping'],
            shapeFixture=b2FixtureDef(density=config_fixture['density']),
            userData={'type': 'ship', 'obj': ship, 'owner': id(ship)},
        )

    def scale(self, vertices, factor):
        nv = []
        for v in vertices:
            nv.append((v[0] * factor, v[1] * factor))
        return nv

    def update_forces(self, controller):
        if controller is None:
            return

        pos = self.body.GetWorldPoint(localPoint=(0.0, 0.0))
        direction = self.body.GetWorldVector(localVector=(1.0, 0.0))
        value = controller.get_axis(GameController.AXIS_RIGHT_X) or 0.0
        intensity = value * LATERAL_PROPULSION_INTENSITY
        self.body.ApplyForce(direction * intensity, pos, True)

        pos = self.body.GetWorldPoint(localPoint=(0.0, 2.0))
        direction = self.body.GetWorldVector(localVector=(0.0, -1.0))

        value = controller.get_axis(GameController.AXIS_TRIGGER_RIGHT) or 0.0
        intensity = value * PROPULSION_INTENSITY
        self.body.ApplyForce(direction * intensity, pos, True)

        value = controller.get_axis(GameController.AXIS_LEFT_X) or 0.0
        intensity = value * SIDE_THRUST_MAX_TORQUE
        self.body.ApplyTorque(intensity, True)

        if controller.is_button_down(GameController.BUTTON_A):
            intensity = BOOST_IMPULSE
            self.body.ApplyLinearImpulse(direction * intensity, pos, True)
