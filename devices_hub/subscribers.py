import json

import requests
from urllib3.exceptions import RequestError

from devices_hub.mqtt.subscribers import JsonSubscriber
from devices_hub.schemas import sonoff_control_schema
from devices_hub.zeroconf_lib.listeners import SonoffDeviceListener


class SonoffControlSubscriber(JsonSubscriber):
    schema = sonoff_control_schema

    def handle(self):
        device_id = self.message['device_id']
        devices = SonoffDeviceListener.devices
        address = devices[device_id].device_address
        data = {'device_id': device_id, 'data': {'switch': self.message['switch']}}
        try:
            requests.post(
                f'http://{address.host}:{address.port}/zeroconf/switch',
                data=json.dumps(data),
            )
        except RequestError:
            pass
