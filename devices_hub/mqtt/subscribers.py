import json
from typing import Optional


class Subscriber:
    def __init__(self):
        self.message = None

    @classmethod
    def as_subscriber(cls):
        return cls()

    def convert_message(self, message: Optional[bytes]):
        return message

    def subscribe(self, message: Optional[bytes]):
        self.message = self.convert_message(message)
        self.handle()

    def handle(self):
        raise NotImplementedError


class JsonSubscriber(Subscriber):
    def convert_message(self, message: Optional[bytes]):
        if message is not None:
            return json.loads(message.decode('utf-8'))
        else:
            return {}
