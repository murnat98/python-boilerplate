from environs import Env
from mqtt.mqtt import MQTT
from zeroconf import ServiceBrowser, Zeroconf

from devices_hub.topics import topics
from devices_hub.zeroconf_lib.listeners import SonoffDeviceListener

env = Env()
env.read_env()

if __name__ == '__main__':
    zeroconf = Zeroconf()
    ServiceBrowser(zeroconf, env('SONOFF_SERVICE_BROWSER_TYPE'), SonoffDeviceListener())

    mqtt = MQTT(env('BROKER_HOST'), env.int('BROKER_PORT'), topics)
    mqtt.loop()
