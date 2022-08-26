from devices_hub.mqtt.topics import Topic
from devices_hub.subscribers import SonoffSwitchSubscriber, TasmotaSwitchSubscriber

topics = [
    Topic('sonoff/switch', SonoffSwitchSubscriber.as_subscriber()),
    Topic('tasmota/switch', TasmotaSwitchSubscriber.as_subscriber()),
]
