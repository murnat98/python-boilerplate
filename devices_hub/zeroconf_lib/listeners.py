from dataclasses import dataclass
from typing import Optional, Dict

from zeroconf import ServiceListener, Zeroconf, ServiceInfo

from devices_hub.logger import get_logger
from devices_hub.zeroconf_lib.errors import ZeroconfError

logger = get_logger(__name__)


@dataclass
class Address:
    host: str
    port: int


class DeviceInfo:
    def __init__(self, service_info: ServiceInfo):
        self.service_info = service_info

    def __str__(self) -> str:
        return self.service_info.__str__()

    @property
    def device_id(self) -> Optional[str]:
        try:
            device_id = self.service_info.properties[b'id']
        except KeyError:
            raise ZeroconfError(f'Cannot find device id from service info {self.service_info}')
        return device_id.decode('utf-8')

    @property
    def device_address(self) -> Address:
        try:
            host_bytes: bytes = self.service_info.addresses[0]
            port: int = self.service_info.port
        except KeyError:
            raise ZeroconfError(f'Cannot find ip address or port of device {self.service_info}')

        if len(host_bytes) != 4:
            raise ZeroconfError(f'ip address more than 4 symbols {host_bytes}')

        host = f'{host_bytes[0]}.{host_bytes[1]}.{host_bytes[2]}.{host_bytes[3]}'
        return Address(host, port)


class SonoffDeviceListener(ServiceListener):
    devices: Dict[str, DeviceInfo] = {}

    def update_service(self, zc: Zeroconf, type_: str, name: str):
        self.add_update_device(zc, type_, name)

    def remove_service(self, zc: Zeroconf, type_: str, name: str):
        info = self.get_info(zc, type_, name)
        device_id = info.device_id
        try:
            del self.devices[device_id]
        except KeyError:
            raise ZeroconfError(f'Device {device_id} cannot find in {self.devices}')

    def add_service(self, zc: Zeroconf, type_: str, name: str):
        self.add_update_device(zc, type_, name)

    def add_update_device(self, zc: Zeroconf, type_: str, name: str):
        info = self.get_info(zc, type_, name)
        device_id = info.device_id
        self.devices[device_id] = info

    def get_info(self, zc: Zeroconf, type_: str, name: str) -> DeviceInfo:
        return DeviceInfo(zc.get_service_info(type_, name))
