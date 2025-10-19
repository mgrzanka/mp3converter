import json
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.config import Config
from src.email_sender import EmailSender

class RabbitMq:
    def __init__(self, email_sender: EmailSender) -> None:
        self.email_sender = email_sender
        self._connect()

    def consume_mp3_messages(self):
        self.channel.basic_consume(
            queue=Config.MP3_QUEUE_NAME,
            on_message_callback=self._callback
        )
        print("Listening for mp3 messages... Press CTR+C to stop.\n")
        self.channel.start_consuming()

    def _callback(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body):
        try:
            message = json.loads(body)

            self.email_sender.send_email(message)

            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Issue while sending notification: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag)

    def _connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=Config.RABBITMQ_HOST,
                port=5672,
                credentials=pika.PlainCredentials(username=Config.RABBITMQ_USER, password=Config.RABBITMQ_PASSWORD)
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue=Config.MP3_QUEUE_NAME,
            durable=True,
            arguments={'x-queue-type': 'quorum'}
        )
