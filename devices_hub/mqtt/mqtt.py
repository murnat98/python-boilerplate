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

    def __init__(self, host: str, port: int, username: str, password: str, topics: List[Topic]):
        self._restart_seconds = self._INITIAL_RESTART_SECONDS
        self.host = host
        self.port = port

        self.topics = {topic.topic: topic.subscriber for topic in topics}

        self.paho_mqtt_client = client.Client()
        self.paho_mqtt_client.username_pw_set(username, password)
        self.paho_mqtt_client.on_message = self.on_message
        self.paho_mqtt_client.on_connect = self.on_connect
        self.paho_mqtt_client.on_disconnect = self.on_disconnect
        self.connect()

    def connect(self):
        try:
            self.paho_mqtt_client.connect(self.host, self.port)
        except ConnectionRefusedError:
            logger.error(
                f'Unable to connect to mosquitto broker at {self.host}:{self.port}. '
                f'Trying in {self._restart_seconds} seconds...'
            )
            sleep(self._restart_seconds)
            if self._restart_seconds < self._MAX_RESTART_SECONDS:
                self._restart_seconds += 5
            self.connect()
        else:
            self._restart_seconds = self._INITIAL_RESTART_SECONDS
            logger.info(f'Successfully connected to broker at {self.host}:{self.port}')

    def on_connect(self, client_data, userdata, flags, rc):
        if rc != 0:
            logger.error(f'Error to connect to mosquitto broker with error {rc} at {self.host}:{self.port}')
            self.paho_mqtt_client.reconnect()
        else:
            for topic in self.topics.keys():
                self.paho_mqtt_client.subscribe(topic)
                logger.info(f'Subscribe to topic {topic}')

    def on_disconnect(self, client_data, userdata, flags):
        logger.error(f'Mosquitto broker disconnected from {self.host}:{self.port}')
        self.connect()

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

    def publish(self, topic, payload):
        self.paho_mqtt_client.publish(topic, payload)

    def loop(self):
        self.paho_mqtt_client.loop_forever()
