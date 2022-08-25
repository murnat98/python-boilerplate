from devices_hub.mqtt.topics import Topic
from devices_hub.subscribers import SonoffControlSubscriber, TasmotaSwitchSubscriber

topics = [
    Topic('sonoff/switch', SonoffControlSubscriber.as_subscriber()),
    Topic('tasmota/switch', TasmotaSwitchSubscriber.as_subscriber()),
]
