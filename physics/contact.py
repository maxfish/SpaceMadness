from Box2D import b2ContactListener


class ContactListener(b2ContactListener):

    def handle_contact(self, contact, began):
        fixture_a = contact.fixtureA
        fixture_b = contact.fixtureB

        body_a, body_b = fixture_a.body, fixture_b.body
        ud_a, ud_b = body_a.userData, body_b.userData

        for ud in (ud_a, ud_b):
            if ud is None:
                print('Does not have userdata. Whatever...')
            if ud['type'] == 'ship':
                print('Collision with ship %r' % ud['obj'])
            elif ud['type'] == 'bullet':
                print('Collision with bullet %r' % ud['obj'])
            if ud['type'] == 'shield':
                print('Collision with shield %r' % ud['obj'])

        if hasattr(ud_a['obj']):
            ud_a['obj'].collide(ud_b['obj'], began)
        if hasattr(ud_a['obj']):
            ud_b['obj'].collide(ud_a['obj'], began)

    def BeginContact(self, contact):
        self.handle_contact(contact, True)

    def EndContact(self, contact):
        self.handle_contact(contact, False)
