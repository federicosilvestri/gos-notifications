from gooutsafe import celery
from gooutsafe import logger
from gooutsafe.models import ContactTracingList, ContactTracing


@celery.task
def contact_tracing_computation(positive_id: int):
    logger.info('Started a computation with positive id=%d' % positive_id)
    pass
