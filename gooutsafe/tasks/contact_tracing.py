from gooutsafe import celery
from gooutsafe import logger
from gooutsafe.comm.reservation_manager import ReservationManager
from gooutsafe.models import ContactTracingList, ContactTracing
from gooutsafe.comm import CommunicationException
from gooutsafe.tasks import TaskFailure


@celery.task
def contact_tracing_computation(positive_id: int):
    """This method allows the health authority to retrieve the list of
       contacts, given a positive user

       Args:
           positive_id (id): univocal id of the user

       Returns:
           Redirects the view to the health authority's home page
    """
    logger.info('Started a computation with positive id=%d' % positive_id)

    # create a new manager and start the communication
    rm = ReservationManager()
    rm.init_communication()

    try:
        pos_reservations = rm.retrieve_by_customer_id(user_id=positive_id)

        for res in pos_reservations:
            contacts = rm.retrieve_all_contact_reservation_by_id(res.id)
            for c in contacts:
                ctracing_list = ContactTracingList(positive_id=positive_id)
                ctracing_list.tracing_list = ContactTracing(contact_id=c.user.id, restaurant_id=c.restaurant_id,
                                                            reservation_id=c.reservation_id)
                ctracing_list.save()
    except CommunicationException as ex:
        logger.error('Cannot complete the task due to CommunicationException')
        logger.error(ex)
        raise TaskFailure(ex)

    # close the communication of manager
    rm.close_communication()
