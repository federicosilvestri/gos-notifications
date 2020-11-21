from gooutsafe import db
import mongoengine as me

from datetime import datetime


class Notification(db.Document):
    """This class represents the model of a Notification.
    """

    # id = db.Column(db.Integer, primary_key=True)
    target_user_id = me.IntField(min_value=0, required=True)
    positive_customer_id = me.IntField(min_value=0, required=True)
    contagion_restaurant_id = me.IntField(min_value=0, required=True)
    contagion_datetime = me.DateTimeField(required=True)
    timestamp = me.DateTimeField(default=datetime.now(), required=True)
    # read = me.BooleanField(default=False, required=True)
