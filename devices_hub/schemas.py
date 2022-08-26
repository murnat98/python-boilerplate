from schema import Or, Schema

from devices_hub.consts import SwitcherEnum

sonoff_control_schema = Schema({'device_id': str, 'switch': Or(*SwitcherEnum.list())})
tasmota_switch_schema = Schema({'client': str, 'switch': Or(*SwitcherEnum.list())})
