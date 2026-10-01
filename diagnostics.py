"""Deterministic training diagnostics; no equipment commands are issued."""

from simulator import PARAMETERS


DETAILS = {
    "pressure": {
        "high": ("HIGH CHAMBER PRESSURE", ["Possible vacuum leak", "Pump performance issue", "Valve issue", "Sensor fault"]),
        "low": ("LOW CHAMBER PRESSURE", ["Gas delivery issue", "Valve response issue", "Sensor fault"]),
    },
    "gas_flow": {
        "high": ("HIGH GAS FLOW", ["Flow-controller setting issue", "Valve issue", "Sensor fault"]),
        "low": ("LOW GAS FLOW", ["Gas supply restriction", "Flow-controller issue", "Valve issue", "Sensor fault"]),
    },
    "rf_power": {
        "high": ("HIGH RF POWER", ["Setpoint issue", "RF matching issue", "Sensor fault"]),
        "low": ("LOW RF POWER", ["Power delivery issue", "RF matching issue", "Sensor fault"]),
    },
    "temperature": {
        "high": ("HIGH CHAMBER TEMPERATURE", ["Cooling performance issue", "Process load change", "Temperature sensor fault"]),
        "low": ("LOW CHAMBER TEMPERATURE", ["Heating performance issue", "Setpoint issue", "Temperature sensor fault"]),
    },
}

STEPS = [
    "Verify the sensor reading.",
    "Review the recent parameter trend.",
    "Check related parameter readings.",
    "Reassess the condition after verification.",
    "If the abnormal condition persists, escalate to a qualified engineer.",
]


def severity(value: float, low: float, high: float) -> str:
    """Classify an out-of-range value using a modest warning band."""
    if low <= value <= high:
        return "NORMAL"
    span = high - low
    if value < low - 0.25 * span or value > high + 0.25 * span:
        return "CRITICAL"
    return "WARNING"


def diagnose(current: dict) -> list[dict]:
    """Return diagnostic cards for readings outside their expected ranges."""
    alerts = []
    for key, config in PARAMETERS.items():
        value = float(current[key])
        low, high = config["range"]
        level = severity(value, low, high)
        if level == "NORMAL":
            continue
        direction = "high" if value > high else "low"
        title, causes = DETAILS[key][direction]
        alerts.append({
            "parameter": config["label"],
            "value": value,
            "unit": config["unit"],
            "expected": f"{low:g}–{high:g} {config['unit']}",
            "severity": level,
            "title": title,
            "causes": causes,
            "steps": STEPS,
        })
    return alerts


def overall_status(alerts: list[dict]) -> str:
    if any(alert["severity"] == "CRITICAL" for alert in alerts):
        return "CRITICAL"
    if alerts:
        return "WARNING"
    return "NORMAL"
