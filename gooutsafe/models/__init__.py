"""
Here you need to import all classes
to be managed by ORM
"""
from .notification import Notification
from .contact_tracing import ContactTracingList, ContactTracing

__all__ = ['Notification', 'ContactTracingList', 'ContactTracing']
