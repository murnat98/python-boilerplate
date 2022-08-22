from devices_hub.mqtt.subscribers import Subscriber


class Topic:
    def __init__(self, topic: str, subscriber: Subscriber):
        self.topic = topic
        self.subscriber = subscriber
