from gooutsafe import app
from gooutsafe.comm import CommunicationException
import pika
import uuid
import json


class ReservationManager:
    """
    This class represents the communication manager for Reservation.
    """

    # Timeout for communication
    COMMUNICATION_TIMEOUT_SECONDS = 5
    # how many time should I retry?
    RETRY_TIMES = 5
    # how long I have to wait before retry?
    RETRY_TIMEOUT_SECONDS = 10

    def __init__(self):
        """
        Create a new reservation manager. It will connect to message broker.
        """
        from gooutsafe.comm import conf

        # creating the connection parameters
        self.connection = None
        self.url_parameters = pika.URLParameters(conf['RABBIT_MQ_URL'])
        self.channel = None
        self.result_queue = None
        self.callback_queue = None
        self.worker_queue = conf['RESERVATION_WORKER_QUEUE_NAME']

        # Response message
        self.response = None
        # Correlation ID
        self.corr_id = None
        self.started = False

    def init_communication(self) -> None:
        if self.started:
            # checking the initializations
            return
        self.started = True

        self.connection = pika.BlockingConnection(self.url_parameters)
        self.channel = self.connection.channel()
        """
        Declare a queue that is exclusive and not durable. Typically used
        only for pushing results by remote procedure.
        """
        self.result_queue = self.channel.queue_declare(
            queue='',
            exclusive=True,
            durable=False
        )

        # retrieve the queue name
        self.callback_queue = self.result_queue.method.queue

        # setting the consuming
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
            consumer_tag='ReservationManagerConsumer'
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def wait_response(self) -> None:
        """
        This function simply processes data from queue and it returns
        when the response is available.
        :return: None
        """
        from datetime import datetime
        from datetime import timedelta
        from time import sleep

        timeout_delta = timedelta(seconds=self.COMMUNICATION_TIMEOUT_SECONDS)
        start_time = datetime.now()
        retry = 1

        while self.response is None:
            # executing data processing
            self.connection.process_data_events()

            # check for timeout
            delta = datetime.now() - start_time
            if delta > timeout_delta:
                if retry > self.RETRY_TIMES:
                    # exception!
                    raise CommunicationException(
                        'The timeout has been triggered, no response from remote service.'
                        ' Please check the reservations microservice.')
                else:
                    app.logger.warning('Service is not responding! Waiting %s seconds, attempt=%d/%d' % (
                        self.RETRY_TIMEOUT_SECONDS, retry, self.RETRY_TIMES)
                                       )
                    # wait
                    sleep(self.RETRY_TIMEOUT_SECONDS)
                    # initialize parameters
                    start_time = datetime.now()
                    retry += 1

    def __send_receive_message(self, message):
        # cleaning the response
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # publishing the job
        self.channel.basic_publish(
            exchange='',
            routing_key=self.worker_queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message)
        )

        self.wait_response()

        # decoding response
        try:
            response = json.loads(self.response)
            return response
        except ValueError:
            msg = 'The response from reservation worker is not in json format response=%s' % self.response
            app.logger.error(msg)
            raise CommunicationException(msg)

    def close_communication(self) -> None:
        if not self.started:
            # we do not want to close None objects :D
            return

        self.started = False
        self.channel.basic_cancel('ReservationManagerConsumer')
        self.connection.close()

    def retrieve_by_customer_id(self, user_id: int):
        return self.__send_receive_message(
            message=dict(func='retrieve_by_customer_id', customer_id=user_id)
        )

    def retrieve_all_contact_reservation_by_id(self, user_id: int):
        return self.__send_receive_message(
            message=dict(func='retrieve_all_contact_reservation_by_id', customer_id=user_id)
        )

    @staticmethod
    def retrieve_all_contact_reservation_by_id_static(user_id: int):
        m = ReservationManager()
        m.init_communication()
        result = m.retrieve_all_contact_reservation_by_id(user_id)
        m.close_communication()
        return result

    @classmethod
    def retrieve_by_customer_id_in_future(cls, customer_id):
        m = ReservationManager()
        m.init_communication()
        ret = m.__send_receive_message(
            message=dict(func='retrieve_by_customer_id_in_future', customer_id=customer_id)
        )
        m.close_communication()

        return ret

    @classmethod
    def retrieve_by_customer_id_in_last_14_days(cls, customer_id):
        m = ReservationManager()
        m.init_communication()
        ret = m.__send_receive_message(
            message=dict(func='retrieve_by_customer_id_in_last_14_days', customer_id=customer_id)
        )
        m.close_communication()

        return ret
