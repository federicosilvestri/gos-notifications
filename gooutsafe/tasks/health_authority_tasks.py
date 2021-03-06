from gooutsafe import celery
from gooutsafe.models.notification import Notification
from gooutsafe.comm.reservation_manager import ReservationManager
from gooutsafe.comm import CommunicationException
from gooutsafe.tasks import TaskFailure


def notify_restaurant_owners_about_positive_past_customer(customer_id):
    notify_restaurant_owners_about_positive_past_customer_task.delay(customer_id)


@celery.task
def notify_restaurant_owners_about_positive_past_customer_task(customer_id):
    from gooutsafe.rao.restaurant_manager import RestaurantManager
    try:
        reservations = ReservationManager.retrieve_by_customer_id_in_last_14_days(customer_id)

        for reservation in reservations:
            owner_id = RestaurantManager.get_owner_id_by_restaurant_id(reservation['restaurant_id'])
            notification = Notification(
                target_user_id=owner_id,
                positive_customer_id=customer_id,
                contagion_restaurant_id=reservation['restaurant_id'],
                contagion_datetime=reservation['start_time']
            )
            notification.save()
    except CommunicationException as ex:
        raise TaskFailure(ex)


def notify_restaurant_owners_about_positive_booked_customer(customer_id):
    notify_restaurant_owners_about_positive_booked_customer_task.delay(customer_id)


@celery.task
def notify_restaurant_owners_about_positive_booked_customer_task(customer_id):
    from gooutsafe.rao.restaurant_manager import RestaurantManager

    try:
        reservations = ReservationManager.retrieve_by_customer_id_in_future(customer_id)

        for reservation in reservations:
            owner_id = RestaurantManager.get_owner_id_by_restaurant_id(reservation['restaurant_id'])

            notification = Notification(
                target_user_id=owner_id,
                positive_customer_id=customer_id,
                contagion_restaurant_id=reservation['restaurant_id'],
                contagion_datetime=reservation['start_time']
            )

            notification.save()
    except CommunicationException as ex:
        raise TaskFailure(ex)


def notify_customers_about_positive_contact(customer_id):
    notify_customers_about_positive_contact_task.delay(customer_id)


@celery.task
def notify_customers_about_positive_contact_task(customer_id):
    try:
        reservations = ReservationManager.retrieve_by_customer_id_in_last_14_days(customer_id)

        for reservation in reservations:
            contact_reservations = ReservationManager.retrieve_all_contact_reservation_by_id_static(
                reservation['id'])

            for contact_reservation in contact_reservations:
                notification = Notification(
                    target_user_id=contact_reservation['user_id'],
                    positive_customer_id=customer_id,
                    contagion_restaurant_id=contact_reservation['restaurant_id'],
                    contagion_datetime=reservation['start_time']
                )
                notification.save()
    except CommunicationException as ex:
        raise TaskFailure(ex)
