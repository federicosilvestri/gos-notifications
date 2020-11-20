from datetime import datetime

from gooutsafe import db


class Notification(db.Model):
    __tablename__ = 'Notification'

    id = db.Column(db.Integer, primary_key=True)
    target_user_id = db.Column(db.Integer)
    positive_customer_id = db.Column(db.Integer)
    contagion_restaurant_id = db.Column(db.Integer)
    contagion_datetime = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean)

    def __init__(self, target_user_id, positive_customer_id, contagion_restaurant_id, contagion_datetime):
        self.target_user_id = target_user_id
        self.positive_customer_id = positive_customer_id
        self.contagion_restaurant_id = contagion_restaurant_id
        self.contagion_datetime = contagion_datetime
        self.read = False

    def set_target_user_id(self, target_user_id):
        self.target_user_id = target_user_id

    def set_positive_customer_id(self, positive_customer_id):
        self.positive_customer_id = positive_customer_id

    def set_contagion_restaurant_id(self, contagion_restaurant_id):
        self.contagion_restaurant_id = contagion_restaurant_id

    def set_contagion_datetime(self, contagion_datetime):
        self.contagion_datetime = contagion_datetime

    def set_read(self, read):
        self.read = read
