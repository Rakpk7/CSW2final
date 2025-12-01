from db_helper import insert_cyber_incident
import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3

DATA_DIR = Path("data1")
DB_FILE = DATA_DIR / "cw2.db"


def load_incidents() -> pd.DataFrame:
    """
    Load cybersecurity incidents data from SQLite into a pandas DataFrame.

    This function is reused by the dashboard and can easily be extended for
    other domains (e.g. data science, IT operations).
    """
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    conn.close()

    # Original CSV used column name 'type' – normalise to 'incident_type'
    if "type" in df.columns and "incident_type" not in df.columns:
        df = df.rename(columns={"type": "incident_type"})

    # Ensure reported_at is treated as a datetime column
    if not df.empty:
        df["reported_at"] = pd.to_datetime(df["reported_at"], errors="coerce")

    return df


def show():
    """Render the cybersecurity incident analytics dashboard."""
    st.title("Cybersecurity – Incident Dashboard")

    user = st.session_state.get("logged_in_user")
    role = st.session_state.get("role")

    # Enforce authentication
    if not user:
        st.warning("Please log in from the Login page before viewing this dashboard.")
        return

    st.caption(f"Logged in as **{user}** (role: `{role}`)")

    # ---------- Load data ----------
    df = load_incidents()

    if df.empty:
        st.error("No incidents found in the database.")
        return

    # ---------- Sidebar filters ----------
    st.sidebar.subheader("Incident Filters")

    severities = sorted(df["severity"].dropna().unique().tolist())
    selected_severity = st.sidebar.multiselect(
        "Severity", severities, default=severities
    )

    statuses = sorted(df["status"].dropna().unique().tolist())
    selected_status = st.sidebar.multiselect(
        "Status", statuses, default=statuses
    )

    types = sorted(df["incident_type"].dropna().unique().tolist())
    selected_type = st.sidebar.multiselect(
        "Incident Type", types, default=types
    )

    min_date = df["reported_at"].min().date()
    max_date = df["reported_at"].max().date()
    date_range = st.sidebar.date_input(
        "Reported Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(date_range, tuple):
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    # Apply filters to DataFrame
    filtered = df[
        df["severity"].isin(selected_severity)
        & df["status"].isin(selected_status)
        & df["incident_type"].isin(selected_type)
        & (df["reported_at"].dt.date >= start_date)
        & (df["reported_at"].dt.date <= end_date)
    ]

    # ---------- Key metrics ----------
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Incidents", len(filtered))
    col2.metric(
        "Open / Investigating",
        int(filtered["status"].isin(["open", "investigating"]).sum()),
    )
    col3.metric(
        "High / Critical",
        int(filtered["severity"].isin(["high", "critical"]).sum()),
    )

    # ---------- Data table ----------
    st.subheader("Incident Table")
    st.dataframe(filtered, use_container_width=True)

    # ---------- Visual analytics ----------
    st.subheader("Incidents by Severity")
    if not filtered.empty:
        st.bar_chart(filtered["severity"].value_counts())

    st.subheader("Incidents over Time")
    if not filtered.empty:
        st.line_chart(
            filtered.groupby(filtered["reported_at"].dt.date)
            .size()
            .rename("incident_count")
        )

    # ---------- Create new incident ----------
    st.subheader("Add New Incident")

    with st.form("new_incident_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            new_type = st.text_input(
                "Incident type (e.g. phishing, malware, ransomware)"
            )
            new_severity = st.selectbox(
                "Severity", ["low", "medium", "high", "critical"]
            )
        with col_b:
            new_status = st.selectbox(
                "Status", ["open", "investigating", "resolved"]
            )
            new_date = st.date_input("Reported date")

        submitted = st.form_submit_button("Create incident")

    if submitted:
        if not new_type.strip():
            st.error("Please enter an incident type.")
        else:
            # Persist new record into cyber_incidents table
            insert_cyber_incident(
                domain="cybersecurity",
                incident_type=new_type.strip(),
                severity=new_severity,
                status=new_status,
                reported_at=str(new_date),
            )
            st.success(
                "New incident added. Use the Rerun button to refresh the dashboard."
            )


if __name__ == "__main__":
    show()