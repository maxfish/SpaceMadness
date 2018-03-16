from Box2D import b2ContactListener


class ContactListener(b2ContactListener):

    def handle_contact(self, contact, began):
        if not contact.enabled:
            return

        body_a = contact.fixtureA.body
        body_b = contact.fixtureB.body

        userdata_a = body_a.userData
        userdata_b = body_b.userData

        if self.owner_matches(userdata_a, userdata_b):
            return

        if 'obj' in userdata_a:
            userdata_a['obj'].collide(
                userdata_b.get('obj'),
                body=body_a,
                began=began,
            )
        if 'obj' in userdata_b:
            userdata_b['obj'].collide(
                userdata_a.get('obj'),
                body=body_b,
                began=began,
            )

    def BeginContact(self, contact):
        self.handle_contact(contact, True)

    def EndContact(self, contact):
        self.handle_contact(contact, False)

    def PreSolve(self, contact, *args):
        uda = contact.fixtureA.body.userData
        udb = contact.fixtureB.body.userData

        if self.owner_matches(uda, udb):
            contact.enabled = False

    def owner_matches(self, uda, udb):
        return 'owner' in uda and 'owner' in udb and uda['owner'] == udb['owner']


def calc_intensity(contact) -> float:
    other = contact.fixtureB.body
    speed = other.linearVelocity.length
    mass = other.body.mass
    angle = other.body.angle

    return speed * mass  # how to add the angle?
