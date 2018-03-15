from Box2D import b2ContactListener


class ContactListener(b2ContactListener):

    def handle_contact(self, contact, began):
        if not contact.enabled:
            return

        fixture_a = contact.fixtureA
        fixture_b = contact.fixtureB

        body_a, body_b = fixture_a.body, fixture_b.body
        ud_a, ud_b = body_a.userData, body_b.userData

        if self.owner_matches(ud_a, ud_b):
            return

        for ud in (ud_a, ud_b):
            if ud is None:
                print('Does not have userdata. Whatever...')
            if ud['type'] == 'ship':
                print('Collision with ship %r' % ud['obj'])
            if ud['type'] == 'bullet':
                print('Collision with bullet %r' % ud['obj'])
            if ud['type'] == 'shield':
                print('Collision with shield %r' % ud['obj'])

        if 'obj' in ud_a:
            ud_a['obj'].collide(ud_b['obj'], began)
        if 'obj' in ud_b:
            ud_b['obj'].collide(ud_a['obj'], began)

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
