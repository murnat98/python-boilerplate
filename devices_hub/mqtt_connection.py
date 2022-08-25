from environs import Env

from devices_hub.mqtt.mqtt import MQTT
from devices_hub.topics import topics

env = Env()
env.read_env()
mqtt_connection = MQTT(
    env('BROKER_HOST'), env.int('BROKER_PORT'), env('BROKER_USERNAME'), env('BROKER_PASSWORD'), topics
)
