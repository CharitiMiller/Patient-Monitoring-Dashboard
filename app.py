import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Clinical Patient Monitoring Dashboard", layout="wide")

# -----------------------------
# Hospital-style custom theme
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0b1420;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #e8f1f8;
}
p, div, label, span {
    color: #d6e2ea;
}
.metric-card {
    background-color: #132235;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #23384f;
    box-shadow: 0 2px 10px rgba(0,0,0,0.25);
}
.alert-high {
    background-color: #5c1f24;
    border-left: 6px solid #ff4b4b;
}
.alert-medium {
    background-color: #5a4316;
    border-left: 6px solid #ffb347;
}
.alert-low {
    background-color: #183b2b;
    border-left: 6px solid #45d483;
}
.section-box {
    background-color: #111c2b;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #223449;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title and header
# -----------------------------
st.title("Clinical Patient Monitoring Dashboard")
st.markdown("### Central Telemetry Risk Overview")
st.caption("Simulated patient vital sign monitoring with triage-style risk prioritization.")

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Monitoring Controls")
num_patients = st.sidebar.slider("Number of Patients", 10, 100, 50, 5)
random_seed = st.sidebar.number_input("Random Seed", 1, 9999, 42)
show_only_flagged = st.sidebar.checkbox("Show only Moderate/High Risk patients", False)

random.seed(random_seed)

# -----------------------------
# Simulated patient data
# -----------------------------
data = {
    "Patient ID": [f"P{str(i).zfill(3)}" for i in range(1, num_patients + 1)],
    "Heart Rate": [random.randint(55, 130) for _ in range(num_patients)],
    "Systolic BP": [random.randint(90, 180) for _ in range(num_patients)],
    "Oxygen Level": [random.randint(88, 100) for _ in range(num_patients)],
    "Respiratory Rate": [random.randint(10, 30) for _ in range(num_patients)],
}

df = pd.DataFrame(data)

# -----------------------------
# Alert flags
# -----------------------------
df["High Heart Rate"] = df["Heart Rate"] > 100
df["Low Heart Rate"] = df["Heart Rate"] < 60
df["High BP"] = df["Systolic BP"] > 140
df["Low Oxygen"] = df["Oxygen Level"] < 95
df["High Respiratory Rate"] = df["Respiratory Rate"] > 20

# -----------------------------
# Risk scoring
# -----------------------------
def calculate_risk(row):
    score = 0
    if row["Heart Rate"] > 100 or row["Heart Rate"] < 60:
        score += 2
    if row["Systolic BP"] > 140:
        score += 2
    if row["Oxygen Level"] < 95:
        score += 3
    if row["Respiratory Rate"] > 20:
        score += 1
    return score

def classify_risk(score):
    if score >= 5:
        return "High Risk"
    elif score >= 3:
        return "Moderate Risk"
    return "Low Risk"

df["Risk Score"] = df.apply(calculate_risk, axis=1)
df["Risk Level"] = df["Risk Score"].apply(classify_risk)

if show_only_flagged:
    filtered_df = df[df["Risk Level"] != "Low Risk"].copy()
else:
    filtered_df = df.copy()

# -----------------------------
# Summary values
# -----------------------------
avg_hr = round(df["Heart Rate"].mean(), 1)
avg_bp = round(df["Systolic BP"].mean(), 1)
avg_o2 = round(df["Oxygen Level"].mean(), 1)
flagged_count = int((df["Risk Level"] != "Low Risk").sum())
high_count = int((df["Risk Level"] == "High Risk").sum())
moderate_count = int((df["Risk Level"] == "Moderate Risk").sum())

# -----------------------------
# Metric cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div class='metric-card'><h4>Average Heart Rate</h4><h2>{avg_hr}</h2></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='metric-card'><h4>Average Systolic BP</h4><h2>{avg_bp}</h2></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='metric-card'><h4>Average Oxygen Level</h4><h2>{avg_o2}</h2></div>", unsafe_allow_html=True)

with col4:
    alert_class = "alert-high" if high_count > 0 else "alert-medium" if moderate_count > 0 else "alert-low"
    st.markdown(f"""
    <div class='metric-card {alert_class}'>
        <h4>Flagged Patients</h4>
        <h2>{flagged_count}</h2>
        <p>High: {high_count} | Moderate: {moderate_count}</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# 🚨 ALERT BANNER (NEW)
# -----------------------------
if high_count > 0:
    st.error(f"🚨 ALERT: {high_count} High-Risk Patients Require Immediate Attention")
elif moderate_count > 0:
    st.warning(f"⚠️ {moderate_count} Moderate-Risk Patients Under Observation")
else:
    st.success("✅ All Patients Stable")

# -----------------------------
# Priority Queue
# -----------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Priority Review Queue")

priority_df = df[df["Risk Level"] != "Low Risk"].sort_values(
    by=["Risk Score", "Oxygen Level"], ascending=[False, True]
)

if priority_df.empty:
    st.success("No patients currently require escalation.")
else:
    st.dataframe(priority_df, width="stretch")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Full Table
# -----------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Patient Data Table")

st.dataframe(filtered_df, width="stretch")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Charts
# -----------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Clinical Trend Charts")

fig1, ax1 = plt.subplots()
ax1.bar(df["Patient ID"], df["Heart Rate"])
plt.xticks(rotation=90)
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.plot(df["Patient ID"], df["Oxygen Level"])
plt.xticks(rotation=90)
st.pyplot(fig2)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Top 5
# -----------------------------
st.subheader("Top 5 Highest Risk Patients")

top_risk = df.sort_values(by="Risk Score", ascending=False).head(5)
st.dataframe(top_risk, width="stretch")