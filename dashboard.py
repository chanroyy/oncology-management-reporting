
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Oncology Management Reporting",
    page_icon="📊",
    layout="wide"
)

st.title("Oncology Management Reporting Dashboard")
st.caption(
    "Synthetic appointment data | "
    "Educational reporting prototype"
)

@st.cache_data
def load_data():
    with sqlite3.connect("oncology_reporting.db") as conn:
        return pd.read_sql_query(
            "SELECT * FROM appointments", conn
        )

try:
    df = load_data()
except Exception as error:
    st.error(f"Could not load database: {error}")
    st.stop()

if df.empty:
    st.warning("No appointment records found.")
    st.stop()

df["appointment_date"] = pd.to_datetime(
    df["appointment_date"]
)

departments = sorted(df["department"].unique())

selected = st.sidebar.multiselect(
    "Filter by oncology department",
    departments,
    default=departments
)

filtered = df[df["department"].isin(selected)].copy()

st.sidebar.info(
    "All records are fictional. "
    "Not intended for clinical use."
)

if filtered.empty:
    st.warning("Select at least one department.")
    st.stop()

total = len(filtered)
completed = (filtered["status"] == "Completed").sum()
cancelled = (filtered["status"] == "Cancelled").sum()
no_show = (filtered["status"] == "No-show").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Appointments", f"{total:,}")
col2.metric("Completed", f"{completed:,}")
col3.metric("Cancellation Rate", f"{cancelled / total:.1%}")
col4.metric("No-show Rate", f"{no_show / total:.1%}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Appointments by Department")
    dept_counts = (
        filtered.groupby("department")
        .size()
        .sort_values(ascending=False)
    )
    st.bar_chart(dept_counts)

with right:
    st.subheader("Appointment Status")
    status_counts = filtered["status"].value_counts()
    st.bar_chart(status_counts)

st.subheader("Monthly Appointment Trends")

filtered["month"] = (
    filtered["appointment_date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

monthly = (
    filtered.groupby(["month", "status"])
    .size()
    .unstack(fill_value=0)
    .sort_index()
)

st.line_chart(monthly)

st.subheader("Appointment Records")
st.dataframe(
    filtered.sort_values(
        "appointment_date",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Download Filtered Report (CSV)",
    data=filtered.to_csv(index=False),
    file_name="oncology_management_report.csv",
    mime="text/csv"
)

st.caption(
    "Prototype built with Python, SQLite, pandas "
    "and Streamlit. All data is synthetic."
)
