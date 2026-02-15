from django.urls import path
from .views import dashboard, get_motor_state, motor_auto, motor_control, send_input, get_calculated,get_input

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("send-input/", send_input),
    path("calculated/", get_calculated),
    path("input/", get_input),
    path("motor-control/", motor_control),
    path("motor-auto/", motor_auto),
    path("motor-state/", get_motor_state),
]
