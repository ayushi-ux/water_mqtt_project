# from django.apps import AppConfig


# class MqttAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'mqtt_app'

# from django.apps import AppConfig
# import threading

# class MqttAppConfig(AppConfig):
#     name = "mqtt_app"

#     def ready(self):
#         from .mqtt.client import create_mqtt_client

#         def run():
#             client = create_mqtt_client()
#             client.loop_forever()

#         threading.Thread(target=run, daemon=True).start()

from django.apps import AppConfig

class MqttAppConfig(AppConfig):
    name = "mqtt_app"

    def ready(self):
        from .mqtt.client import get_mqtt_client
        get_mqtt_client()
