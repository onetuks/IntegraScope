import json
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timezone
import requests

from app.server.sap.log.mpl import MplApiClient
from app.server.sap.oauth2 import OAuth2Client
from app.server.vector_store.chroma_store import get_error_log_store

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("Dashboard")

# --- 1. Artifact Execution Statistics ---
st.header("Today's Artifact Execution Statistics")

@st.cache_data(ttl=300)
def get_todays_mpls():
    # Calculate start and end of today (UTC or local? SAP usually uses UTC, but let's assume we want today in local/server time or UTC)
    # Using UTC for now as per ms_to_tz default
    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now
    
    session = requests.Session()
    oauth_client = OAuth2Client(session=session)
    try:
        token = oauth_client.get_access_token()
        mpl_client = MplApiClient(session=session)
        mpls = mpl_client.get_mpls_by_period(start_of_day, end_of_day, token=token)
        return mpls
    except Exception as e:
        st.error(f"Failed to fetch MPLs: {e}")
        return []

mpls = get_todays_mpls()

if mpls:
    data = []
    for mpl in mpls:
        # Calculate duration in seconds
        duration = (mpl.log_end - mpl.log_start).total_seconds()
        data.append({
            "Status": mpl.status,
            "Artifact": mpl.artifact_id,
            "StartTime": mpl.log_start,
            "Duration": duration
        })
    
    df = pd.DataFrame(data)
    
    # Count by Status
    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    
    # Metric cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_count = len(df)
    completed_count = len(df[df["Status"] == "COMPLETED"])
    escalated_count = len(df[df["Status"] == "ESCALATED"])
    discarded_count = len(df[df["Status"] == "DISCARDED"])
    failed_count = len(df[df["Status"] == "FAILED"])
    
    col1.metric("ALL", total_count)
    col2.metric("COMPLETED", completed_count)
    col3.metric("ESCALATED", escalated_count)
    col4.metric("DISCARDED", discarded_count)
    col5.metric("FAILED", failed_count)
    
    # Bar Chart
    fig = px.bar(status_counts, x="Status", y="Count", title="Execution Counts by Status", color="Status")
    st.plotly_chart(fig, use_container_width=True)

    # --- 2. Performance & Trends ---
    st.markdown("---")
    st.header("Performance & Trends")
    
    col_trend, col_top = st.columns([2, 1])
    
    with col_trend:
        st.subheader("Hourly Execution Trend")
        if not df.empty:
            # Group by Hour and Status
            # Ensure StartTime is datetime
            df['Hour'] = df['StartTime'].dt.floor('h') # 'h' for hour frequency
            hourly_counts = df.groupby(['Hour', 'Status']).size().reset_index(name='Count')
            
            fig_trend = px.line(hourly_counts, x='Hour', y='Count', color='Status', markers=True, 
                                title="Executions Over Time (Hourly)")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No data for trend analysis.")

    with col_top:
        st.subheader("Top Failing Artifacts")
        failed_df = df[df['Status'] == 'FAILED']
        if not failed_df.empty:
            top_failed = failed_df['Artifact'].value_counts().head(5).reset_index()
            top_failed.columns = ['Artifact', 'Failures']
            st.dataframe(top_failed, hide_index=True, use_container_width=True)
        else:
            st.success("No failures recorded today! 🎉")

        st.subheader("Slowest Artifacts (Avg Duration)")
        if not df.empty:
            avg_duration = df.groupby('Artifact')['Duration'].mean().sort_values(ascending=False).head(5).reset_index()
            avg_duration.columns = ['Artifact', 'Avg Duration (s)']
            avg_duration['Avg Duration (s)'] = avg_duration['Avg Duration (s)'].round(2)
            st.dataframe(avg_duration, hide_index=True, use_container_width=True)
        else:
            st.info("No duration data available.")

else:
    st.info("No artifacts executed today.")


# --- 3. Useful Information from Vector DB ---
st.markdown("---")
st.header("Recommended Insights from Knowledge Base")

try:
    store = get_error_log_store()
    
    st.markdown("Recent resolved cases and insights:")
    
    if hasattr(store, "peek_cases"):
        cases = store.peek_cases(limit=5)
        if cases:
            for case in cases:
                artifact_id = case.get('artifact_id', 'Unknown')
                status_code = case.get('status_code', 'N/A')
                exception_msg = case.get('exception', 'No exception details')
                
                with st.expander(f"📌 {artifact_id} (Status: {status_code})"):
                    st.markdown(f"**Error Message:**")
                    st.code(exception_msg, language="text")
                    
                    col_analysis, col_solution = st.columns(2)
                    
                    with col_analysis:
                        st.markdown("### 🔍 Analysis")
                        analysis_json = case.get('analysis_json')
                        if analysis_json:
                            try:
                                analysis_data = json.loads(analysis_json)
                                if isinstance(analysis_data, dict):
                                    for k, v in analysis_data.items():
                                        st.markdown(f"**{k}:** {v}")
                                else:
                                    st.write(analysis_data)
                            except json.JSONDecodeError:
                                st.write(analysis_json)
                        else:
                            st.info("No analysis available.")

                    with col_solution:
                        st.markdown("### 💡 Solution")
                        solution_json = case.get('solution_json')
                        if solution_json:
                            try:
                                solution_data = json.loads(solution_json)
                                if isinstance(solution_data, dict):
                                    for k, v in solution_data.items():
                                        st.markdown(f"**{k}:** {v}")
                                else:
                                    st.write(solution_data)
                            except json.JSONDecodeError:
                                st.write(solution_json)
                        else:
                            st.info("No solution available.")
        else:
            st.info("No recent cases found in Knowledge Base.")
    else:
        st.warning("Vector store capability to list cases is not yet available.")

except Exception as e:
    st.error(f"Error connecting to Vector Store: {e}")
