# Plasma Etch Chamber Monitoring & Fault Diagnosis Simulator

An educational software simulation of a plasma etch process chamber that monitors chamber pressure, process-gas flow, RF power, and temperature, detects abnormal conditions using rule-based diagnostics, and demonstrates structured troubleshooting, preventive-maintenance, and shift-reporting workflows.

> **Important disclaimer:** This is an educational simulation, not a real equipment-control system. It does not connect to hardware and does not perform LOTO, ESD, cleanroom, vacuum-system, or semiconductor-equipment maintenance. Use qualified personnel and approved site procedures for real equipment.

## Overview and architecture

The dashboard is deliberately simple:

```
simulator.py  → synthetic time-series readings → app.py charts and metrics
diagnostics.py → deterministic range rules     → app.py alerts and workflow
```

There is no database, API, authentication, ML, or hardware integration. Selecting a fault mode produces a repeatable simulated trend, and the most recent reading is evaluated by deterministic rules.

## Features

- Current readings and Plotly trends for chamber pressure, gas flow, RF power, and chamber temperature
- Fault simulation for normal operation, high chamber pressure, low gas flow, high temperature, and high RF power
- NORMAL / WARNING / CRITICAL equipment status
- Rule-based diagnostic cards with expected ranges, possible causes, and cautious escalation steps
- A simulated training troubleshooting workflow
- Preventive-maintenance training checklist and downloadable shift-summary CSV

## Simulated equipment parameters and detection logic

| Parameter | Expected simulated range |
|---|---:|
| Chamber pressure | 15–25 mTorr |
| Gas flow | 35–50 sccm |
| RF power | 300–400 W |
| Chamber temperature | 50–75 °C |

Any latest reading outside its expected range produces an alert. A modest band outside the range is a **WARNING**; a larger departure is **CRITICAL**. The diagnostics are rule-based and informational only.

## Troubleshooting workflow

1. Verify measurement.
2. Check trend.
3. Check related parameter.
4. Reassess condition.
5. Escalate if condition persists.

This is a simulated training workflow; it never recommends unsupervised equipment repair.

## Relevance to Semiconductor Equipment Engineering

This project demonstrates instrumentation-style parameter monitoring, time-series interpretation, structured troubleshooting, preventive-maintenance thinking, anomaly escalation, and clear technical documentation. It does **not** claim real semiconductor-equipment experience.



## How to run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
