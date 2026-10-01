"""Synthetic chamber readings for the training dashboard."""

import numpy as np
import pandas as pd


PARAMETERS = {
    "pressure": {"label": "Chamber pressure", "unit": "mTorr", "range": (15.0, 25.0)},
    "gas_flow": {"label": "Gas flow", "unit": "sccm", "range": (35.0, 50.0)},
    "rf_power": {"label": "RF power", "unit": "W", "range": (300.0, 400.0)},
    "temperature": {"label": "Chamber temperature", "unit": "°C", "range": (50.0, 75.0)},
}

FAULTS = {
    "Normal operation": None,
    "High chamber pressure": "pressure",
    "Low gas flow": "gas_flow",
    "High temperature": "temperature",
    "High RF power": "rf_power",
}


def generate_readings(fault_mode: str = "Normal operation", count: int = 100) -> pd.DataFrame:
    """Return a repeatable, realistic-looking simulated shift history.

    The selected training fault ramps in during the final 20 readings so both
    the trend and the current metric clearly communicate the condition.
    """
    rng = np.random.default_rng(42)
    time = pd.date_range(end=pd.Timestamp.now().floor("min"), periods=count, freq="min")
    phase = np.linspace(0, 3 * np.pi, count)

    data = {
        "timestamp": time,
        "pressure": 20 + 0.7 * np.sin(phase) + rng.normal(0, 0.35, count),
        "gas_flow": 42.5 + 1.0 * np.sin(phase + 0.5) + rng.normal(0, 0.45, count),
        "rf_power": 350 + 7 * np.sin(phase + 1.2) + rng.normal(0, 3.0, count),
        "temperature": 62 + 1.4 * np.sin(phase + 0.8) + rng.normal(0, 0.5, count),
    }
    readings = pd.DataFrame(data)
    ramp = np.linspace(0, 1, min(20, count))
    affected = FAULTS.get(fault_mode)
    if affected == "pressure":
        readings.loc[readings.index[-len(ramp):], "pressure"] += 12 * ramp
    elif affected == "gas_flow":
        readings.loc[readings.index[-len(ramp):], "gas_flow"] -= 14 * ramp
    elif affected == "temperature":
        readings.loc[readings.index[-len(ramp):], "temperature"] += 22 * ramp
    elif affected == "rf_power":
        readings.loc[readings.index[-len(ramp):], "rf_power"] += 95 * ramp
    return readings.round(2)
