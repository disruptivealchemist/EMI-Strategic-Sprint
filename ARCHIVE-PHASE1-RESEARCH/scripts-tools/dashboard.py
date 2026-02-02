import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Project Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- Data Loading ---
@st.cache_data
def load_gantt_data():
    df = pd.read_csv("gantt-chart.csv")
    df["Start"] = pd.to_datetime(df["Start"])
    df["Finish"] = pd.to_datetime(df["Finish"])
    return df

@st.cache_data
def load_risk_data():
    with open("risk-management-plan.md", "r") as f:
        lines = f.readlines()
    
    # Find the table in the markdown file
    table_started = False
    header = []
    data = []
    for line in lines:
        if "| Risk ID |" in line:
            header = [h.strip() for h in line.split("|")[1:-1]]
            table_started = True
        elif table_started and "| :---" not in line:
            if line.strip() == "":
                break
            data.append([d.strip() for d in line.split("|")[1:-1]])

    if header and data:
        df = pd.DataFrame(data, columns=header)
        df["Probability (1-5)"] = pd.to_numeric(df["Probability (1-5)"])
        df["Impact (1-5)"] = pd.to_numeric(df["Impact (1-5)"])
        df["Risk Score"] = pd.to_numeric(df["Risk Score"])
        return df
    return pd.DataFrame()

gantt_df = load_gantt_data()
risk_df = load_risk_data()

# --- Dashboard UI ---
st.title("📌 6-Week Branding and Marketing Sprint Dashboard")

# --- Project Summary ---
st.header("Project Summary")

# Calculate overall project dates
project_start = gantt_df["Start"].min()
project_end = gantt_df["Finish"].max()
today = datetime.now()

# Overall project status (simple logic)
project_health = "🟢 Green" # Green
if (project_end - today).days < 14:
    project_health = "🟡 Amber" # Amber
if today > project_end:
    project_health = "🔴 Red" # Red

col1, col2, col3 = st.columns(3)
col1.metric("Project Start Date", project_start.strftime("%Y-%m-%d"))
col2.metric("Project End Date", project_end.strftime("%Y-%m-%d"))
col3.metric("Project Health", project_health)

# --- Interactive Gantt Chart ---
st.header("Project Timeline")

fig = px.timeline(gantt_df, x_start="Start", x_end="Finish", y="Name", color="Resource Names", 
                title="Project Gantt Chart", labels={"Name": "Task"})
fig.update_yaxes(autorange="reversed") # To display tasks from top to bottom
st.plotly_chart(fig, use_container_width=True)

# --- KPIs ---
st.header("Key Performance Indicators (KPIs)")

# Example KPIs (can be made more dynamic)
asset_completion_rate = st.slider("Asset Completion Rate (%)", 0, 100, 10) # Example value
trip_readiness_score = st.selectbox("Trip Readiness Score (1-5)", [1, 2, 3, 4, 5], index=2) # Example value

col1, col2 = st.columns(2)
col1.metric("Asset Completion Rate", f"{asset_completion_rate}%")
col2.metric("Trip Readiness Score", f"{trip_readiness_score}/5")

# --- Live Risk Register ---
st.header("Risk Register")

# Filter by risk owner
risk_owners = ["All"] + list(risk_df["Risk Owner"].unique())
selected_owner = st.selectbox("Filter by Risk Owner", risk_owners)

if selected_owner == "All":
    filtered_risks = risk_df
else:
    filtered_risks = risk_df[risk_df["Risk Owner"] == selected_owner]

st.dataframe(filtered_risks)

# --- Project Documents ---
st.header("Project Documents")
st.markdown("""
*   [Work Breakdown Structure (WBS)](WBS.md)
*   [Project Overview](project-overview.md)
*   [Risk Management Plan](risk-management-plan.md)
*   [Gantt Chart Data](gantt-chart.csv)
""")
