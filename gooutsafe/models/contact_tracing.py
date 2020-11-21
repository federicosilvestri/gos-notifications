from gooutsafe import db
import mongoengine as me


class ContactTracing(me.EmbeddedDocument):
    """This class represents the fact that a user is traced because it has been in contact
    with a positive user.
    """

    contact_id = me.IntField(min_value=0)
    restaurant_id = me.IntField(min_value=0)
    reservation_id = me.IntField(min_value=0)


class ContactTracingList(db.Document):
    """This class describes a contact tracing list, hence it is a list of ContactTracing object, identified
    by a positive user ID.
    """

    positive_id = me.IntField(min_value=0, primary=True)
    tracing_list = me.ListField(me.EmbeddedDocumentField(ContactTracing))

