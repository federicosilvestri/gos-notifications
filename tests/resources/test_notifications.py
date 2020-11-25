from tests.resources import ViewTest


class TestNotifications(ViewTest):

    @classmethod
    def setUpClass(cls):
        super(TestNotifications, cls).setUpClass()
        from gooutsafe.resources import contact_tracing
        cls.ct = contact_tracing

    def test_get_by_user_id(self):
        #no notifications
        rv = self.client.get('/notifications')
        assert rv.status_code == 404
