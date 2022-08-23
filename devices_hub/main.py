from environs import Env
from mqtt.mqtt import MQTT

from devices_hub.topics import topics

env = Env()
env.read_env()

if __name__ == '__main__':
    mqtt = MQTT(env('BROKER_HOST'), env.int('BROKER_PORT'), topics)
    mqtt.loop()
