"""Plasma Etch Chamber Monitoring & Fault Diagnosis Simulator."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from diagnostics import diagnose, overall_status
from simulator import FAULTS, PARAMETERS, generate_readings


st.set_page_config(page_title="Plasma Etch Chamber Monitor | Training", page_icon="⚙️", layout="wide")
st.markdown("""
<style>
    .block-container {max-width: 1250px; padding-top: 2rem;}
    .status {padding: 1rem 1.25rem; border-radius: .55rem; font-weight: 700; letter-spacing: .08em;}
    .normal {background: #e6f4ea; color: #137333; border-left: 5px solid #34a853;}
    .warning {background: #fef7e0; color: #8a5a00; border-left: 5px solid #fbbc04;}
    .critical {background: #fce8e6; color: #b3261e; border-left: 5px solid #ea4335;}
    .disclaimer {color: #56616f; font-size: .93rem;}
</style>
""", unsafe_allow_html=True)

st.title("Plasma Etch Chamber Monitoring & Fault Diagnosis Simulator")
st.markdown("<p class='disclaimer'>Educational training simulation only. It does not control real semiconductor equipment or replace qualified engineering, safety, LOTO, ESD, cleanroom, vacuum-system, or maintenance procedures.</p>", unsafe_allow_html=True)

if "fault_mode" not in st.session_state:
    st.session_state.fault_mode = "Normal operation"

readings = generate_readings(st.session_state.fault_mode)
latest = readings.iloc[-1].to_dict()
alerts = diagnose(latest)
status = overall_status(alerts)

st.subheader("Equipment status")
status_class = status.lower()
st.markdown(f"<div class='status {status_class}'>{status}</div>", unsafe_allow_html=True)

st.subheader("Current parameters")
metric_columns = st.columns(4)
for column, (key, config) in zip(metric_columns, PARAMETERS.items()):
    low, high = config["range"]
    value = latest[key]
    is_abnormal = not low <= value <= high
    column.metric(config["label"], f"{value:.1f} {config['unit']}", "Out of range" if is_abnormal else "Within expected range", delta_color="inverse" if is_abnormal else "normal")

st.subheader("Parameter trends")
for row in [("pressure", "gas_flow"), ("rf_power", "temperature")]:
    chart_columns = st.columns(2)
    for column, key in zip(chart_columns, row):
        config = PARAMETERS[key]
        low, high = config["range"]
        chart = go.Figure()
        chart.add_trace(go.Scatter(x=readings["timestamp"], y=readings[key], mode="lines", name=config["label"], line=dict(color="#1769aa", width=2)))
        chart.add_hrect(y0=low, y1=high, fillcolor="#34a853", opacity=0.10, line_width=0, annotation_text="Expected range", annotation_position="top left")
        chart.update_layout(title=config["label"], height=270, margin=dict(l=15, r=15, t=45, b=15), showlegend=False, yaxis_title=config["unit"], xaxis_title="Time", template="plotly_white")
        column.plotly_chart(chart, use_container_width=True)

st.subheader("Fault simulation")
st.radio("Operating condition", list(FAULTS), key="fault_mode", horizontal=True)
st.caption("Select a mode to inject a simulated condition into the latest readings.")

st.subheader("Diagnostic alert")
if not alerts:
    st.success("No abnormal conditions detected. All current readings are within their simulated expected ranges.")
else:
    for alert in alerts:
        method = st.error if alert["severity"] == "CRITICAL" else st.warning
        method(f"{alert['title']} — {alert['severity']}")
        left, right = st.columns([1, 2])
        left.markdown(f"**Current:** {alert['value']:.1f} {alert['unit']}  \\n+**Expected:** {alert['expected']}")
        right.markdown("**Possible causes**\n\n" + "\n".join(f"- {cause}" for cause in alert["causes"]))
        st.markdown("**Recommended diagnostic steps**\n\n" + "\n".join(f"{number}. {step}" for number, step in enumerate(alert["steps"], 1)))

st.subheader("Troubleshooting workflow")
st.info("Simulated training workflow — use qualified personnel and approved site procedures for any real equipment condition.")
workflow = ["Verify measurement", "Check trend", "Check related parameter", "Reassess condition", "Escalate if condition persists"]
flow_columns = st.columns(5)
for number, (column, step) in enumerate(zip(flow_columns, workflow), 1):
    column.markdown(f"**Step {number}**  \n{step}")

st.subheader("Preventive-maintenance checklist")
checklist = [
    "Verify equipment is in a safe state", "Verify sensor readings", "Inspect electrical connections",
    "Check pressure stability", "Check gas-flow stability", "Record measurements", "Complete maintenance log",
]
checked = []
for index, item in enumerate(checklist):
    checked.append(st.checkbox(item, key=f"pm_{index}"))
pm_complete = all(checked)
if pm_complete:
    st.success("Training PM checklist completed — engineer verification required.")
else:
    st.caption(f"{sum(checked)} of {len(checklist)} training items complete.")

st.subheader("Shift summary")
st.caption("Equipment: Plasma Etch Chamber A — Simulation")
summary = pd.DataFrame([{
    "equipment_name": "Plasma Etch Chamber A — Simulation", "shift_duration": "100 minutes",
    "average_pressure_mTorr": round(readings["pressure"].mean(), 2),
    "average_gas_flow_sccm": round(readings["gas_flow"].mean(), 2),
    "average_rf_power_W": round(readings["rf_power"].mean(), 2),
    "average_temperature_C": round(readings["temperature"].mean(), 2),
    "abnormal_events": len(alerts), "pm_checklist_complete": "Yes" if pm_complete else "No",
}])
st.dataframe(summary, use_container_width=True, hide_index=True)
st.download_button("Download shift summary (CSV)", summary.to_csv(index=False).encode("utf-8"), "simulated_shift_summary.csv", "text/csv")
