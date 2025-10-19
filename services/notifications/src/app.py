import sys, os
from src.rabbitmq import RabbitMq
from src.email_sender import EmailSender


if __name__ == '__main__':
    email_sender = EmailSender()
    rabbitmq = RabbitMq(email_sender)
    try:
        rabbitmq.consume_mp3_messages()
    except KeyboardInterrupt as e:
        print("Stopping notification service on user's request...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception as e:
        print(f"Stopping notification service because of exception: {e}\n")
