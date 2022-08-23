import json

import requests
from requests import exceptions
from urllib3.exceptions import RequestError

from devices_hub.logger import get_logger
from devices_hub.mqtt.subscribers import JsonSubscriber
from devices_hub.schemas import sonoff_control_schema
from devices_hub.zeroconf_lib.listeners import SonoffDeviceListener

logger = get_logger(__name__)


class SonoffControlSubscriber(JsonSubscriber):
    schema = sonoff_control_schema

    def handle(self):
        device_id = self.message['device_id']
        device_info = SonoffDeviceListener.get_device(device_id)
        if device_info is None:
            logger.error(f'Device {device_id} not found')
            return

        address = device_info.device_address
        data = {'device_id': device_id, 'data': {'switch': self.message['switch']}}
        try:
            request = requests.post(
                f'http://{address.host}:{address.port}/zeroconf/switch',
                data=json.dumps(data),
            )
        except (RequestError, exceptions.ConnectionError):
            logger.error(f'Request error on {address} with data {data}')
        else:
            logger.info(f'Response from {address} - {request.status_code} {request.json()}')
