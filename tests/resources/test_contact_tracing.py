from tests.resources import ViewTest


class TestContactTracing(ViewTest):

    @classmethod
    def setUpClass(cls):
        super(TestContactTracing, cls).setUpClass()
        from gooutsafe.resources import contact_tracing
        cls.ct = contact_tracing

    def test_get_list(self):
        rv = self.client.get('/contact_tracing/1')
        assert rv.status_code == 404

    def test_trigger_generation(self):
        #no contact list
        rv = self.client.post('/contact_tracing/1')
        assert rv.status_code == 200

