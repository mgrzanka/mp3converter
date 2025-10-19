import sys, os
from src.mongo import Mongo
from src.rabbitmq import RabbitMQ
from src.converter import Converter


if __name__ == '__main__':
    mongo = Mongo()
    converter = Converter(mongo)
    rabbitMQ = RabbitMQ(mongo, converter)
    try:
        rabbitMQ.consume_video_messages()
    except KeyboardInterrupt:
        print("Stopping service at user's request...\n")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception as e:
        print(f"Stopping converter service because of exception: {e}\n")
