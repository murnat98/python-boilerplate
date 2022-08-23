import json
from typing import Optional

from schema import Schema, SchemaError

from devices_hub.mqtt.errors import MQTTError, ValidationError


class Subscriber:
    schema = None

    def __init__(self):
        self.message = None

    @classmethod
    def as_subscriber(cls):
        return cls()

    def get_schema(self):
        if self.schema is not None and not isinstance(self.schema, Schema):
            raise MQTTError('Only Schema (https://pypi.org/project/schema/) instances supported for schemas')
        return self.schema

    def convert_message(self, message: Optional[bytes]):
        schema = self.get_schema()
        if schema is not None:
            try:
                return schema.validate(message)
            except SchemaError as e:
                raise ValidationError(e)
        else:
            return message

    def subscribe(self, message: Optional[bytes]):
        self.message = self.convert_message(message)
        self.handle()

    def handle(self):
        raise NotImplementedError


class JsonSubscriber(Subscriber):
    def convert_message(self, message: Optional[bytes]):
        if message is not None:
            json_message = json.loads(message.decode('utf-8'))
            return super().convert_message(json_message)
        else:
            return {}
