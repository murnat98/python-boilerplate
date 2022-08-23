from devices_hub.mqtt.subscribers import JsonSubscriber
from devices_hub.schemas import sonoff_control_schema


class SonoffControlSubscriber(JsonSubscriber):
    schema = sonoff_control_schema

    def handle(self):
        print(self.message)
