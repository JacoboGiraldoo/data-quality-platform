# core/validators/status_calculator.py

def calculate_status(percentage: float, green_threshold: float, yellow_threshold: float) -> str:
    if percentage <= green_threshold:
        return "green"
    elif percentage <= yellow_threshold:
        return "yellow"
    return "red"