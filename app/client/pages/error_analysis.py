import streamlit as st

from app.client.ui import hide_sidebar_nav, render_sidebar_nav

hide_sidebar_nav()
render_sidebar_nav("Error Analysis")

st.title("Error Analysis")

queue = st.session_state.get("test_queue", [])

if not queue:
    st.info("No iFlows queued for testing yet. Select flows on the Test Automation page and click Test.")
else:
    st.subheader("Queued iFlows")
    header_cols = st.columns([3, 3, 3, 3])
    headers = ["Artifact", "Package", "Sender", "Receiver"]
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")

    for flow in queue:
        cols = st.columns([3, 3, 3, 3])
        cols[0].write(flow.get("artifact", ""))
        cols[1].write(flow.get("package", ""))
        cols[2].write(flow.get("sender", ""))
        cols[3].write(flow.get("receiver", ""))
