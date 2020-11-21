from gooutsafe import db
import mongoengine as me


class ContactTracing(me.EmbeddedDocument):
    """This class represents the fact that a user is traced because it has been in contact
    with a positive user.
    """

    contact_id = me.IntField(min_value=0)
    restaurant_id = me.IntField(min_value=0)
    reservation_id = me.IntField(min_value=0)

    def __init__(self, contact_id: int, restaurant_id: int, reservation_id: int):
        """
        Create a new instance of ContactTracing.

        :param contact_id: the ID of user
        :param restaurant_id: the restaurant ID
        :param reservation_id: the reservation ID
        """
        super(ContactTracing, self).__init__(
            contact_id=contact_id,
            restaurant_id=restaurant_id,
            reservation_id=reservation_id
        )




class ContactTracingList(db.Document):
    """This class describes a contact tracing list, hence it is a list of ContactTracing object, identified
    by a positive user ID.
    """

    positive_id = me.IntField(min_value=0)
    tracing_list = me.ListField(me.EmbeddedDocumentField(ContactTracing))

    def __init__(self, positive_id: int):
        super(ContactTracingList, self).__init__(
            positive_id=positive_id,
            tracing_list=[]
        )