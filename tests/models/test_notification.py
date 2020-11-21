import random
import unittest
from faker import Faker
from . import ModelTest


class TestNotification(ModelTest):

    @classmethod
    def setUpClass(cls):
        super(TestNotification, cls).setUpClass()
        from gooutsafe.models import notification
        cls.notif = notification
        cls.faker = Faker()

    @classmethod
    def _random_id(cls):
        return cls.faker.random.number({'min': 1, 'max': 10})

    @classmethod
    def generate_random_notification(cls, target_user_id=None):
        if target_user_id is None:
            target_user_id = cls._random_id()

        positive_customer_id = cls._random_id()
        contagion_restaurant_id = cls._random_id()
        contagion_datetime = cls.faker.date_time()
        notification = cls.notif.Notification(target_user_id.id, positive_customer_id.id, contagion_restaurant_id.id,
                                              contagion_datetime)

        return notification, (target_user_id, positive_customer_id, contagion_restaurant_id, contagion_datetime)

    @classmethod
    def assertEqualNotifications(cls, n1, n2):
        cls.assertEqual(n1.target_user_id, n2.target_user_id)
        cls.assertEqual(n1.positive_customer_id, n2.positive_customer_id)
        cls.assertEqual(n1.contagion_restaurant_id, n2.contagion_restaurant_id)
        cls.assertEqual(n1.contagion_datetime, n2.contagion_datetime)

    def test_init(self):
        notif, (target_user_id, positive_customer_id, contagion_restaurant_id,
                contagion_datetime) = self.generate_random_notification()

        notif_dict = dict(
            target_user_id=target_user_id,
            positive_customer_id=positive_customer_id,
            contagion_restaurant_id=contagion_restaurant_id,
            contagion_datetime=contagion_datetime
        )

        self.assertEqualNotifications(notif_dict, notif)

    def test_set_target_user_id(self):
        _id = self._random_id()
        n, _ = self.generate_random_notification(_id)

        self.assertEqualNotifications(n.target_user_id, _id)
        n.set_target_user_id()

    def set_positive_customer_id(self, positive_customer_id):
        self.positive_customer_id = positive_customer_id

    def set_contagion_restaurant_id(self, contagion_restaurant_id):
        self.contagion_restaurant_id = contagion_restaurant_id

    def set_contagion_datetime(self, contagion_datetime):
        self.contagion_datetime = contagion_datetime

    def set_read(self, read):
        self.read = read
