from gooutsafe import celery
from gooutsafe import logger
from gooutsafe.models import ContactTracingList, ContactTracing


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

    pos_reservations = ReservationManager.retrieve_by_customer_id(user_id=positive_id)
    cust_contacts = []
    restaurant_contacts = []
    date_contacts = []

    for res in pos_reservations:
        contacts = ReservationManager.retrieve_all_contact_reservation_by_id(res.id)
        for c in contacts:
            cust = CustomerManager.retrieve_by_id(c.user_id)
            cust_contacts.append(cust)
            restaurant_contacts.append(RestaurantManager.retrieve_by_id(c.restaurant_id).name)
            date_contacts.append(c.start_time.date())


