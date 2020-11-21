"""
This package contains all the classes
that manage the communications with other microservices.
"""
import os
from gooutsafe import logger
import pika

__REQUIRED_CONFIG_KEYS = ['RABBIT_MQ_HOST', 'RABBIT_MQ_PORT',
                          'RABBIT_MQ_VHOST', 'RESERVATION_WORKER_QUEUE_NAME']

amqp_connection: pika.BlockingConnection
conf = dict
disabled: bool


def init_rabbit_mq():
    """
    Initialize Rabbit MQ Connection
    :return: None
    """
    global amqp_connection
    global conf

    # loading configuration
    conf = dict()
    for key in __REQUIRED_CONFIG_KEYS:
        value = os.getenv(key, None)

        if value is None:
            raise RuntimeError('Cannot find the environment variable %s for Rabbit MQ Configuration' % key)

        conf[key] = value

    # Getting parameters
    url = 'amqp://%s:%s/%s' % (conf['RABBIT_MQ_HOST'], conf['RABBIT_MQ_PORT'], conf['RABBIT_MQ_VHOST'])
    parameters = pika.connection.URLParameters(url)

    # Creating connection to Rabbit Broker
    amqp_connection = pika.BlockingConnection(parameters=parameters)
    logger.info('AMQP Connection initialized!')
