import streamlit as st

from app.client.ui import hide_sidebar_nav, render_sidebar_nav
from app.common import IFLOWS

hide_sidebar_nav()
render_sidebar_nav("Test Execution")

st.title("Test Execution")

# Keep current selections in session state so they persist across reruns.
selected_artifacts = set(st.session_state.get("selected_iflow_artifacts", []))

header_cols = st.columns([1.5, 3, 3, 3, 3, 1.5])
headers = ["Queue", "Artifact", "Package", "Sender", "Receiver", "Test"]
for col, header in zip(header_cols, headers):
    col.markdown(f"**{header}**")

for flow in IFLOWS:
    cols = st.columns([1.5, 3, 3, 3, 3, 1.5])
    cols[1].write(flow.artifact)
    cols[2].write(flow.package)
    cols[3].write(flow.sender)
    cols[4].write(flow.receiver)
    cols[5].write(flow.test_result)
    checked = cols[0].checkbox(
        "Queue",
        key=f"queue_{flow.artifact}",
        value=flow.artifact in selected_artifacts,
        label_visibility="collapsed",
    )
    if checked:
        selected_artifacts.add(flow.artifact)
    else:
        selected_artifacts.discard(flow.artifact)

# Persist updated selections
st.session_state["selected_iflow_artifacts"] = list(selected_artifacts)

queued_flows = [flow for flow in IFLOWS if flow.artifact in selected_artifacts]

st.divider()
test_col, reset_col, _ = st.columns([1, 1, 6])

test_clicked = test_col.button("Test", type="primary", use_container_width=True)
reset_clicked = reset_col.button("초기화", type="secondary",
                                 use_container_width=True)

if test_clicked:
    if not queued_flows:
        st.warning("하나 이상의 iFlow를 선택해 주세요.")
    else:
        st.session_state["test_queue"] = [flow.model_dump()
                                          for flow in queued_flows]
        st.switch_page("pages/error_analysis.py")

if reset_clicked:
    selected_artifacts.clear()
    st.session_state["selected_iflow_artifacts"] = []
    st.session_state.pop("test_queue", None)
    for flow in IFLOWS:
        st.session_state.pop(f"queue_{flow.artifact}", None)
    st.rerun()
