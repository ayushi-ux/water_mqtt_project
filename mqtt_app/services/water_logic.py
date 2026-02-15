# def calculate_water_data(total_height, total_volume, distance):
#     water_height = max(total_height - distance, 0)

#     percentage = (water_height / total_height) * 100 if total_height else 0
#     filled_water_volume = (percentage / 100) * total_volume

#     motor_status = 1 if percentage < 20 else 0

#     return {
#         "percentage": round(percentage, 2),
#         "filled_water_volume": round(filled_water_volume, 2),
#         "motor_status": motor_status,
#     }

# def calculate(total_height, total_volume, distance, battery_voltage=0):
#     water_height = max(total_height - distance, 0)


#     percentage = (water_height / total_height) * 100 if total_height else 0
#     filled_volume = (percentage / 100) * total_volume

#     motor_status = 1 if percentage < 20 else 0
#     motor_mode = 0  # auto mode (example)

#     return {
#         "percentage": round(percentage, 2),
#         "filled_water_in_volume": round(filled_volume, 2),
#         "motor_status": motor_status,
#         "motor_mode": motor_mode,
#         "battery_voltage": battery_voltage,
#         "distance": round(distance, 2),
#         "total_height": total_height,
#         "total_volume": total_volume,
#     }


def calculate(
    total_height: float,
    total_volume: float,
    distance: float,
    battery_voltage: float = 0,
):
    """
    Central water management calculation logic.
    This is the SINGLE source of truth for all derived values.
    """

    # Water level calculation
    water_height = max(total_height - distance, 0)

    # Percentage filled
    percentage = (water_height / total_height) * 100 if total_height else 0

    # Filled volume
    filled_water_in_volume = (percentage / 100) * total_volume

    # Motor logic (example rule)
    motor_status = 1 if percentage < 20 else 0
    motor_mode = 0  # 0 = auto, 1 = manual (future use)

    return {
        "percentage": round(percentage, 2),
        "filled_water_in_volume": round(filled_water_in_volume, 2),
        "motor_status": motor_status,
        "motor_mode": motor_mode,
        "battery_voltage": round(battery_voltage, 2),
        "distance": round(distance, 2),
        "total_height": total_height,
        "total_volume": total_volume,
    }
