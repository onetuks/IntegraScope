from datetime import datetime
from typing import Any

import streamlit as st

from app.client.utils.utils import format_duration


class TestedArtifact:
    """Tested Artifact Info Card Component"""

    def __init__(self, item: Any):
        self._item = item

    def render_artifact(self):
        msg_guid = self._item.get("message_guid")
        wrapper = st.container(border=True)
        cols = wrapper.columns([4, 3, 1])

        cols[0].text_input(
            label="Package Id",
            value=self._item.get("package_id", "-"),
            key=f"{msg_guid}_package",
        )
        cols[0].text_input(
            label="Artifact Id",
            value=self._item.get("artifact_id", "-"),
            key=f"{msg_guid}_artifact",
        )

        cols[1].text_input(
            label="Message GUID",
            value=msg_guid or "-",
            key=f"{msg_guid}_message_guid",
        )
        cols[1].text_input(
            label="Correlation Id",
            value=self._item.get("correlation_id", "-"),
            key=f"{msg_guid}_correlation",
        )

        status_color = (
            "red"
            if self._item.get("status", "-") == "FAILED"
            else "green"
            if self._item.get("status") == "COMPLETED"
            else "orange"
        )
        cols[2].badge(self._item.get("status", "-"), color=status_color)
        cols[2].caption(format_duration(self._item.get("log_start"),
                                        self._item.get("log_end")))
        dt = datetime.strptime(self._item.get("log_start"),
                               "%Y-%m-%dT%H:%M:%S.%fZ")
        cols[2].caption(datetime.strftime(dt, "%Y-%m-%d %H:%M:%S"))
        if cols[2].button(
                label="Analyze",
                use_container_width=True,
                type="primary",
                key=f"analyze_btn_{msg_guid}",
                disabled=self._item.get("status") not in ("FAILED", "ESCALATED")
        ):
            st.session_state["message_guid"] = msg_guid
            st.switch_page("pages/analysis.py")
