import paho.mqtt.client as mqtt
from django.conf import settings
from .callbacks import on_connect, on_message, on_disconnect

_mqtt_client = None

def get_mqtt_client():
    global _mqtt_client

    if _mqtt_client is None:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        client.connect(
            settings.MQTT_BROKER,
            settings.MQTT_PORT,
            settings.MQTT_KEEPALIVE
        )

        client.loop_start()
        _mqtt_client = client

    return _mqtt_client
