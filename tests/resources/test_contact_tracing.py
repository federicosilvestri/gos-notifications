from tests.resources import ViewTest


class TestContactTracing(ViewTest):

    @classmethod
    def setUp(cls):
        super(TestContactTracing, cls).setUp()
        from gooutsafe.resources import contact_tracing
        cls.ct = contact_tracing

    def test_get_list(self):
        """
        @TODO
        :return:
        """
        pass

    def test_trigger_generation(self):
        """
        @TODO
        :return:
        """
        pass
