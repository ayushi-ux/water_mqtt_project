import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from mqtt_app.mqtt.client import get_mqtt_client
from mqtt_app.mqtt.topics import MQTT_TOPIC
from mqtt_app.services.state import LATEST_CALCULATED


def dashboard(request):
    return render(request, "dashboard.html")


@csrf_exempt
def send_input(request):
    data = json.loads(request.body)

    client = get_mqtt_client()  # reuse existing MQTT connection
    client.publish(
        MQTT_TOPIC,
        json.dumps({
            "type": "input",
            "total_height": data["total_height"],
            "total_volume": data["total_volume"],
        })
    )

    return JsonResponse({"status": "sent"})


def get_calculated(request):
    return JsonResponse(LATEST_CALCULATED)



from mqtt_app.services.state import LATEST_INPUT

def get_input(request):
    return JsonResponse(LATEST_INPUT)







# new////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@csrf_exempt
def motor_control(request):
    data = json.loads(request.body)

    client = get_mqtt_client()
    client.publish(
        MQTT_TOPIC,
        json.dumps({
            "type": "motor_command",
            "motor_mode": 1,              # manual
            "motor_status": data["status"]  # 1 = ON, 0 = OFF
        })
    )

    return JsonResponse({"status": "motor command sent"})


@csrf_exempt
def motor_auto(request):
    client = get_mqtt_client()
    client.publish(
        MQTT_TOPIC,
        json.dumps({
            "type": "motor_command",
            "motor_mode": 0  # auto
        })
    )

    return JsonResponse({"status": "auto mode enabled"})


from mqtt_app.services.state import MOTOR_STATE

def get_motor_state(request):
    return JsonResponse(MOTOR_STATE)
