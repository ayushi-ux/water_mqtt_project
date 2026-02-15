import json

from mqtt_app.mqtt import client
from .topics import MQTT_TOPIC
from mqtt_app.services.state import (
    LATEST_INPUT,
    LATEST_SENSOR,
    LATEST_CALCULATED,
    MOTOR_STATE,
)
from mqtt_app.services.water_logic import calculate


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT connected")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to: {MQTT_TOPIC}")
    else:
        print(f"❌ MQTT connection failed | rc={rc}")








def on_message(client, userdata, msg):
    try:
        raw = msg.payload.decode()
        print("📩 Raw Payload:", raw)

        data = json.loads(raw)

        # Make keys lowercase (fix uppercase issue)
        data = {k.lower(): v for k, v in data.items()}

        # Normalize type value also
        if "type" in data and isinstance(data["type"], str):
            data["type"] = data["type"].lower()

        print("📦 Parsed JSON:", data)

    except Exception as e:
        print("❌ JSON Error:", e)
        return



        # 🔥 STOP LOOP HERE
    if data.get("type") == "calculated":
        return
    input_updated = False
    sensor_updated = False

    # ---------- USER INPUT ----------
    if data.get("type") == "input":
        LATEST_INPUT.clear()
        LATEST_INPUT.update({
            "total_height": float(data["total_height"]),
            "total_volume": float(data["total_volume"]),
        })
        input_updated = True

    # ---------- SENSOR DATA ----------
    elif data.get("type") == "sensor":
        LATEST_SENSOR.clear()
        LATEST_SENSOR.update({
            "distance": float(data["distance"]),
            "battery_voltage": float(data.get("battery_voltage", 0)),
        })
        sensor_updated = True

    # ---------- LEGACY ESP32 ----------
    elif "distance" in data:
        LATEST_SENSOR.clear()
        LATEST_SENSOR.update({
            "distance": float(data["distance"]),
            "battery_voltage": float(data.get("battery_voltage", 0)),
        })
        sensor_updated = True

    # ---------- MOTOR COMMAND (MANUAL CONTROL) ----------
    elif data.get("type") == "motor_command":
        MOTOR_STATE["motor_mode"] = data.get("motor_mode", 0)

        if MOTOR_STATE["motor_mode"] == 1:
            MOTOR_STATE["motor_manual_status"] = data.get("motor_status", 0)
        
        print("🟢 Motor command stored:", MOTOR_STATE)
        return

    else:
        return

    # ---------- CALCULATE WHEN STATE IS READY ----------
    if (input_updated or sensor_updated) and LATEST_INPUT and LATEST_SENSOR:
        result = calculate(
            total_height=LATEST_INPUT["total_height"],
            total_volume=LATEST_INPUT["total_volume"],
            distance=LATEST_SENSOR["distance"],
            battery_voltage=LATEST_SENSOR.get("battery_voltage", 0),
        )

        LATEST_CALCULATED.clear()
        LATEST_CALCULATED.update(result)

        client.publish(
            MQTT_TOPIC,
            json.dumps({"type": "calculated", **result})
        )



# def on_message(client, userdata, msg):
#     try:
#         data = json.loads(msg.payload.decode())
#     except Exception:
#         return

#     input_updated = False
#     sensor_updated = False

#     # ---------- USER INPUT ----------
#     if data.get("type") == "input":
#         LATEST_INPUT.clear()
#         LATEST_INPUT.update({
#             "total_height": float(data["total_height"]),
#             "total_volume": float(data["total_volume"]),
#         })
#         input_updated = True

#     # ---------- SENSOR DATA ----------
#     elif data.get("type") == "sensor":
#         LATEST_SENSOR.clear()
#         LATEST_SENSOR.update({
#             "distance": float(data["distance"]),
#             "battery_voltage": float(data.get("battery_voltage", 0)),
#         })
#         sensor_updated = True

#     # ---------- LEGACY ESP32 ----------
#     elif "Distance" in data:
#         LATEST_SENSOR.clear()
#         LATEST_SENSOR.update({
#             "distance": float(data["Distance"]),
#             "battery_voltage": float(data.get("Battery_voltage", 0)),
#         })
#         sensor_updated = True

#     # ---------- MOTOR COMMAND (DEV ECHO) ----------
#     elif data.get("type") == "motor_command":
#         MOTOR_STATE["motor_mode"] = data.get("motor_mode", 0)
#         MOTOR_STATE["motor_manual_status"] = data.get("motor_status", 0)

#         # 🔴 Echo motor state to MQTT
#         client.publish(
#             MQTT_TOPIC,
#             json.dumps({
#                 "type": "motor_state",
#                 "motor_mode": MOTOR_STATE["motor_mode"],
#                 "motor_status": MOTOR_STATE["motor_manual_status"],
#             })
#         )

#         print("🟡 DEV: Motor state echoed to MQTT:", MOTOR_STATE)
#         return

#     else:
#         return

#     # ---------- AUTO CALCULATION ----------
#     if (
#         (input_updated or sensor_updated)
#         and LATEST_INPUT
#         and LATEST_SENSOR
#         and MOTOR_STATE.get("motor_mode", 0) == 0
#     ):
#         result = calculate(
#             total_height=LATEST_INPUT["total_height"],
#             total_volume=LATEST_INPUT["total_volume"],
#             distance=LATEST_SENSOR["distance"],
#             battery_voltage=LATEST_SENSOR.get("battery_voltage", 0),
#         )

#         LATEST_CALCULATED.clear()
#         LATEST_CALCULATED.update(result)

#         client.publish(
#             MQTT_TOPIC,
#             json.dumps({
#                 "type": "calculated",
#                 **result
#             })
#         )



def on_disconnect(client, userdata, rc):
    print("⚠️ MQTT disconnected")
