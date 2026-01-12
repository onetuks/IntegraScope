from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Dict, Any, Optional

import streamlit as st

from app.client.utils import format_duration


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    try:
        return parsedate_to_datetime(value) if value else None
    except Exception:
        return None


def _format_datetime(value: Optional[str]) -> str:
    dt_value = _parse_datetime(value)
    return dt_value.strftime("%Y-%m-%d %H:%M:%S %Z") if dt_value else "-"


class ArtifactContext:
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        
    def render_component(self):
        with st.container(border=True):
            st.subheader("Artifact Context")

            st.badge(self.data.get("artifact_type"))
            meta_cols = st.columns([1, 1])
            meta_cols[0].text_input(label="Artifact Id",
                                    value=self.data.get("artifact_id",
                                                   "-"),
                                    disabled=False)
            meta_cols[1].text_input(label="Package Id",
                                    value=self.data.get("package_id",
                                                   "-"),
                                    disabled=False)
            meta_cols[0].text_input(label="Message GUID",
                                    value=self.data.get("message_guid",
                                                   "-"),
                                    disabled=False)

            st.divider()

            info_cols = st.columns([6, 1])
            info_cols[0].text_input(label="Exception",
                                    value=self.data.get("exception",
                                                   "-"),
                                    disabled=False)
            info_cols[1].caption("Status Code")
            info_cols[1].container().badge(
                str(self.data.get("status_code", "-")),
                width="stretch", color="red")
            info_cols[1].caption("Duration")
            info_cols[1].badge(
                format_duration(self.data.get("log_start", "-"),
                                self.data.get("log_end", "-")))
            time_cols = info_cols[0].columns([1, 1])
            time_cols[0].caption("Log Start")
            time_cols[0].badge(
                f"{_format_datetime(self.data.get('log_start'))}",
                color="green")
            time_cols[1].caption("Log End")
            time_cols[1].badge(
                f"{_format_datetime(self.data.get('log_end'))}",
                color="green")

            st.markdown("**Error Log**")
            st.code(self.data.get("origin_log", ""), language="bash")