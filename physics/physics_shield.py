from Box2D import b2CircleShape
from Box2D import b2FixtureDef

from game.ship import Ship


class PhysicShield:
    def __init__(self, physicsWorld, center, radius):
        self.shape = b2CircleShape(radius=radius)
        self.body = physicsWorld.CreateDynamicBody(
            position=(center.x, center.y),
            shapes=self.shape,
            angularDamping=5,
            linearDamping=0.1,
            shapeFixture=b2FixtureDef(density=2.0, isSensor=True),
        )

        self.body.contactListener = self

    def handle_contact(self, contact, began):
        fixture_a = contact.fixtureA
        fixture_b = contact.fixtureB

        body_a, body_b = fixture_a.body, fixture_b.body
        ud_a, ud_b = body_a.userData, body_b.userData

        for ud in (ud_a, ud_b):
            if ud is None:
                continue

            if isinstance(ud, object):
                print("!!!!!!!")
                break

    def BeginContact(self, contact):
        self.handle_contact(contact, True)

    def EndContact(self, contact):
        self.handle_contact(contact, False)
