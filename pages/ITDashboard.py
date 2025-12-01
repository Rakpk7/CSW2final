import streamlit as st
import pandas as pd

# use the helper functions from db_helper.py
from db_helper import get_it_incidents_df, insert_it_incident


def show():
    st.title("IT Operations – Service Outage Dashboard")

    # ---------- auth check ----------
    user = st.session_state.get("logged_in_user")
    role = st.session_state.get("role")

    if not user:
        st.warning("Please login from the Login page first.")
        return

    st.caption(f"Logged in as **{user}** (role: `{role}`)")

    # ---------- load data ----------
    df = get_it_incidents_df()

    if df.empty:
        st.error("No IT incidents found in the database.")
        return

    # normalise column name 'type' for UI if needed
    if "type" in df.columns and "incident_type" not in df.columns:
        df = df.rename(columns={"type": "incident_type"})

    # ensure dates are real datetimes
    if "detected_at" in df.columns:
        df["detected_at"] = pd.to_datetime(df["detected_at"], errors="coerce")
    if "resolved_at" in df.columns:
        df["resolved_at"] = pd.to_datetime(df["resolved_at"], errors="coerce")

    # ---------- sidebar filters ----------
    st.sidebar.subheader("IT Incident Filters")

    services = sorted(df["service_name"].dropna().unique().tolist())
    selected_services = st.sidebar.multiselect(
        "Service name", services, default=services
    )

    severities = sorted(df["severity"].dropna().unique().tolist())
    selected_severity = st.sidebar.multiselect(
        "Severity", severities, default=severities
    )

    statuses = sorted(df["status"].dropna().unique().tolist())
    selected_status = st.sidebar.multiselect(
        "Status", statuses, default=statuses
    )

    # apply filters
    filtered = df[
        df["service_name"].isin(selected_services)
        & df["severity"].isin(selected_severity)
        & df["status"].isin(selected_status)
    ]

    # ---------- key metrics ----------
    st.subheader("Key Metrics")
    c1, c2, c3 = st.columns(3)

    total = len(filtered)
    open_inv = int(filtered["status"].isin(["open", "investigating"]).sum())
    resolved = int((filtered["status"] == "resolved").sum())

    c1.metric("Total IT incidents", total)
    c2.metric("Open / Investigating", open_inv)
    c3.metric("Resolved", resolved)

    # ---------- table ----------
    st.subheader("IT Incident Table")
    st.dataframe(filtered, use_container_width=True)

    # ---------- simple charts ----------
    st.subheader("Incidents by Severity")
    if not filtered.empty:
        sev_counts = (
            filtered["severity"].value_counts().rename_axis("severity").to_frame("count")
        )
        st.bar_chart(sev_counts)

    st.subheader("Incidents over Time (Detected)")
    if not filtered.empty and "detected_at" in filtered.columns:
        by_date = (
            filtered.groupby(filtered["detected_at"].dt.date)
            .size()
            .rename("incident_count")
        )
        st.line_chart(by_date)

    # ---------- add new incident ----------
    st.subheader("Add New IT Incident")

    with st.form("new_it_incident", clear_on_submit=True):
        colA, colB = st.columns(2)
        with colA:
            new_service = st.text_input("Service name")
            new_incident_type = st.text_input("Incident type (e.g. outage, latency)")
        with colB:
            new_severity = st.selectbox(
                "Severity", ["low", "medium", "high", "critical"]
            )
            new_status = st.selectbox(
                "Status", ["open", "investigating", "resolved"]
            )
            detected_date = st.date_input("Detected at")
            resolved_date = st.date_input("Resolved at (optional)", value=None)

        submitted = st.form_submit_button("Create IT incident")

    if submitted:
        if not new_service.strip() or not new_incident_type.strip():
            st.error("Please fill in service name and incident type.")
        else:
            insert_it_incident(
                service_name=new_service.strip(),
                incident_type=new_incident_type.strip(),
                severity=new_severity,
                status=new_status,
                detected_at=str(detected_date),
                resolved_at=str(resolved_date) if resolved_date else None,
            )
            st.success("New IT incident added. Click **Rerun** to refresh.")


if __name__ == "__main__":
    show()