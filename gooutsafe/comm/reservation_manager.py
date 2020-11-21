import pika
import uuid
import json


class ReservationManager:

    def __init__(self):
        from gooutsafe.comm import amqp_connection, conf
        self.amqp_connection = amqp_connection
        self.channel = None
        self.result_queue = None
        self.callback_queue = None
        self.worker_queue = conf['RESERVATION_WORKER_QUEUE_NAME']
        self.response = None
        # This only a correlation ID
        self.corr_id = None

    def init_communication(self) -> None:
        self.channel = self.amqp_connection.channel()
        """
        Declare a queue that is exclusive and not durable. Typically used
        only for pushing results by remote procedure.
        """
        self.result_queue = self.channel.queue_declare(
            queue='',
            exclusive=True,
            durable=False
        )
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
        # waiting the response inside our queue
        while self.response is None:
            self.amqp_connection.process_data_events()

        # decoding response
        try:
            response = json.loads(self.response)
            return response
        except ValueError:
            raise RuntimeError('The response from reservation worker is not in json format response=%s' % self.response)

        return None

    def close_communication(self) -> None:
        self.channel.basic_cancel('ReservationManagerConsumer')

    def retrieve_by_customer_id(self, customer_id: int):
        return self.__send_receive_message(
            message=dict(func='retrieve_by_customer_id', customer_id=customer_id)
        )

    def retrieve_all_contact_reservation_by_id(self, customer_id: int):
        return self.__send_receive_message(
            message=dict(func='retrieve_all_contact_reservation_by_id', customer_id=customer_id)
        )
