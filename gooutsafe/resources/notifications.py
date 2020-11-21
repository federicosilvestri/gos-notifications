from flask import jsonify
from connexion import NoContent
from datetime import date
from gooutsafe.models.notification import Notification


def get_by_user_id(user_id: int):
    """
    Given the user id, this function searches inside database the notifications and returns it.

    :param user_id: user ID
    :return: json response
    """
    
    notifications = Notification.objects(target_user_id=user_id)

    if len(notifications) == 0:
        return NoContent, 404

    return jsonify(notifications), 200
