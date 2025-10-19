import pika
from pika.exceptions import AMQPError
import json
from src.config import Config


class RabbitMq:
    def __init__(self):
        self._connect()

    def publish_message(self, message: object, routing_key: str):
        try:
            self._ensure_connection()
            self.__channel.basic_publish(
                exchange='',
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
            )
        except AMQPError as e:
            self._connect()
            self.__channel.basic_publish(
                exchange='',
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
            )

    def _connect(self):
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=Config.RABBITMQ_HOST,
                port=Config.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD),
            )
        )
        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(
            queue='video',
            durable=True,
            arguments={'x-queue-type': 'quorum'}
        )

    def _ensure_connection(self):
        if self.__connection.is_closed or self.__channel.is_closed:
            self._connect()
