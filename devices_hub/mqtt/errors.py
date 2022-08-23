from devices_hub.errors import LoggerError


class MQTTError(LoggerError):
    logger = 'mqtt'


class ValidationError(Exception):
    pass
