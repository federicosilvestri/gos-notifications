from flask import jsonify
from connexion import NoContent
from gooutsafe.models.contact_tracing import ContactTracingList
from gooutsafe.tasks.contact_tracing import contact_tracing_computation


def trigger_generation(positive_id: int):
    """
    Given the contact user id, this function triggers the task that generates
    the contact tracing list.

    :param positive_id: user ID
    :return: None
    """
    contact_tracing_computation.delay(positive_id=positive_id)

    return NoContent, 200


def get_list(positive_id: int):
    """
    Given the contact user id, this function searches inside database the contact tracing list and returns it.

    :param positive_id: user ID
    :return: json response
    """

    ctl = ContactTracingList.objects(positive_id=positive_id).first()

    if ctl is None:
        return NoContent, 404

    return jsonify(ctl), 200
