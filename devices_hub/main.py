from zeroconf import ServiceBrowser, Zeroconf

from devices_hub.mqtt_connection import env, mqtt_connection
from devices_hub.zeroconf_lib.listeners import SonoffDeviceListener

if __name__ == '__main__':
    zeroconf = Zeroconf()
    ServiceBrowser(zeroconf, env('SONOFF_SERVICE_BROWSER_TYPE'), SonoffDeviceListener())

    mqtt_connection.loop()
