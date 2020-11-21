from . import ModelTest


class TestContactTracing(ModelTest):

    @classmethod
    def setUpClass(cls):
        super(TestContactTracing, cls).setUpClass()
        from gooutsafe.models import contact_tracing
        cls.ct = contact_tracing

    def test_init(self):
        self.ct.ContactTracingList()
        self.ct.ContactTracing()

