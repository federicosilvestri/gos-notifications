from faker import Faker
from . import ModelTest


class TestNotification(ModelTest):

    @classmethod
    def setUpClass(cls):
        super(TestNotification, cls).setUpClass()
        from gooutsafe.models import notification
        cls.notif = notification
        cls.faker = Faker()

    def test_init(self):
        self.notif.Notification()
