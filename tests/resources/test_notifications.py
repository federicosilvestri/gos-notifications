from tests.resources import ViewTest


class TestNotifications(ViewTest):

    @classmethod
    def setUp(cls):
        super(TestNotifications, cls).setUp()
        from gooutsafe.resources import contact_tracing
        cls.ct = contact_tracing

    def test_set_status(self):
        """
        @TODO
        :return:
        """
        pass

    def test_get_by_id(self):
        """
        @TODO
        :return:
        """
        pass

    def test_get_by_user_id(self):
        """
        @TODO
        :return:
        """
        pass
