from time import sleep
from typing import List

from paho.mqtt import client

from devices_hub.logger import get_logger
from devices_hub.mqtt.errors import MQTTError, ValidationError
from devices_hub.mqtt.topics import Topic

logger = get_logger(__name__)


class MQTT:
    _INITIAL_RESTART_SECONDS = 5
    _MAX_RESTART_SECONDS = 60

    def __init__(self, host: str, port: int, topics: List[Topic]):
        self._restart_seconds = self._INITIAL_RESTART_SECONDS
        self.topics = {topic.topic: topic.subscriber for topic in topics}

        self.paho_mqtt_client = client.Client()
        self.paho_mqtt_client.on_message = self.on_message
        self.paho_mqtt_client.on_connect = self.on_connect
        self.connect(host, port)

    def connect(self, host: str, port: int):
        try:
            self.paho_mqtt_client.connect(host, port)
        except ConnectionRefusedError:
            logger.error(
                f'Unable to connect to mosquitto broker at {host}:{port}. Trying in {self._restart_seconds} seconds...'
            )
            sleep(self._restart_seconds)
            if self._restart_seconds < self._MAX_RESTART_SECONDS:
                self._restart_seconds += 5
            self.connect(host, port)
        else:
            logger.info(f'Successfully connected to broker at {host}:{port}')

    def on_connect(self, client_data, userdata, flags, rc):
        if rc != 0:
            self.paho_mqtt_client.reconnect()
        else:
            for topic in self.topics.keys():
                self.paho_mqtt_client.subscribe(topic)

    def on_message(self, client_data, userdata, message):
        logger.info(f'New message to {message.topic} - {message.payload}')
        try:
            subscriber = self.topics[message.topic]
        except KeyError:
            raise MQTTError(f'{message.topic} not found in topics {self.topics}')
        try:
            subscriber.subscribe(message.payload)
        except ValidationError:
            logger.error(f'Message incorrect format: {message.payload}')

    def loop(self):
        self.paho_mqtt_client.loop_forever()
