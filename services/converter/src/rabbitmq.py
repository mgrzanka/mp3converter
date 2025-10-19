import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from pika.exceptions import AMQPError
import json
from src.config import Config
from src.mongo import Mongo
from src.converter import Converter


class RabbitMQ:
    def __init__(self, mongo: Mongo, converter: Converter) -> None:
        self.mongo = mongo
        self.converter = converter
        self._connect()

    def consume_video_messages(self):
        self.channel.basic_consume(
            queue=Config.VIDEOS_QUEUE_NAME,
            on_message_callback=self._consume_callback
        )
        print("Waiting for messages... To stop press CRL+C\n")
        self.channel.start_consuming()

    def publish_mp3_message(self, mp3_fid: str, video_fid: str, email: str):
        message = {
            "video_fid": video_fid,
            "mp3_fid": mp3_fid,
            "email": email
        }
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key='mp3',
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
            )
        except AMQPError as e:
            self._connect()
            self.channel.basic_publish(
                exchange='',
                routing_key='mp3',
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)
            )
        except Exception as e:
            print(f"Error in publishing mp3 to queue: {e}")
            self.mongo.delete_mp3(mp3_fid)
            raise e

    def _consume_callback(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body):
        try:
            message = json.loads(body)

            audio = self.converter.convert(message)
            mp3_fid = self.mongo.put_mp3(audio)
            self.publish_mp3_message(mp3_fid, message["video_fid"], message["email"])

            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Issue in conversion: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag)

    def _connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=Config.RABBITMQ_HOST,
            port=5672,
            credentials=pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD),
            heartbeat=60
        ))
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue='mp3',
            durable=True,
            arguments={'x-queue-type': 'quorum'}
        )
        self.channel.queue_declare(
            queue=Config.VIDEOS_QUEUE_NAME,
            durable=True,
            arguments={'x-queue-type': 'quorum'}
        )

    def _ensure_connection(self):
        if self.connection.is_closed or self.channel.is_closed:
            self._connect()
