from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

from app.client.api.api_client import get


def parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def format_duration(start: Optional[str], end: Optional[str]) -> str:
    start_dt, end_dt = parse_dt(start), parse_dt(end)
    if not start_dt or not end_dt:
        return "-"
    delta = end_dt - start_dt
    seconds = delta.total_seconds()
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, remainder = divmod(int(seconds), 60)
    return f"{minutes}m {remainder}s"


def fetch_tested(log_start: str, log_end: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    try:
        response = get(f"/api/tested?log_start={log_start}&log_end={log_end}")
        data = response.json()
        return data.get("tested_artifacts", []), None
    except Exception as exc:
        return None, str(exc)


def status_badge(status: str) -> str:
    color = {"COMPLETED": "green", "FAILED": "red"}.get(status.upper(), "gray")
    return f"<span style='padding:2px 8px;border-radius:999px;background:{color};color:white;font-weight:600;'>{status}</span>"


st.title("Tested iFlows")
st.caption("최근 테스트된 iFlow 실행 결과 목록")


def ceil_to_next_hour(dt: datetime) -> datetime:
    base = dt.replace(minute=0, second=0, microsecond=0)
    return base + timedelta(hours=1)


now = datetime.now()
default_end = ceil_to_next_hour(now)
default_start = default_end - timedelta(hours=2)

stored_start = st.session_state.get("tested_start_dt", default_start)
stored_end = st.session_state.get("tested_end_dt", default_end)

col_range = st.columns([1, 1, 0.5])
start_dt = col_range[0].datetime_input("시작 시간", value=stored_start)
end_dt = col_range[1].datetime_input("종료 시간", value=stored_end)
col_range[2].container(height=10, border=False)
refresh = col_range[2].button("조회", type="primary", use_container_width=True)

log_start_param = start_dt.isoformat()
log_end_param = end_dt.isoformat()

if "tested_artifacts" not in st.session_state:
    with st.spinner("테스트 실행 결과를 불러오는 중..."):
        artifacts, error = fetch_tested(log_start_param, log_end_param)
    st.session_state["tested_artifacts"] = artifacts
    st.session_state["tested_error"] = error
    st.session_state["tested_start_dt"] = start_dt
    st.session_state["tested_end_dt"] = end_dt
elif refresh:
    if start_dt >= end_dt:
        st.error("시작 시간이 종료 시간보다 같거나 늦을 수 없습니다.")
        artifacts = st.session_state.get("tested_artifacts", [])
        error = "시간 설정 오류"
    else:
        with st.spinner("테스트 실행 결과를 불러오는 중..."):
            artifacts, error = fetch_tested(log_start_param, log_end_param)
        st.session_state["tested_artifacts"] = artifacts
        st.session_state["tested_error"] = error
        st.session_state["tested_start_dt"] = start_dt
        st.session_state["tested_end_dt"] = end_dt
else:
    artifacts = st.session_state.get("tested_artifacts", [])
    error = st.session_state.get("tested_error")

if error:
    st.error(f"테스트 목록을 불러오지 못했습니다: {error}")
    st.stop()

if not artifacts:
    st.info("표시할 테스트 실행 결과가 없습니다.")
    st.stop()

st.markdown("#### 실행 결과")
header_cols = st.columns([3, 2.5, 2, 2, 1.5, 1.5])
header_cols[0].markdown("**Artifact**")
header_cols[1].markdown("**Package**")
header_cols[2].markdown("**Message GUID**")
header_cols[3].markdown("**Correlation ID**")
header_cols[4].markdown("**Duration**")
header_cols[5].markdown("**Status**")

for item in artifacts:
    cols = st.columns([3, 2.5, 2, 2, 1.5, 1.5])

    artifact_label = item.get("artifact_id", "-")
    if cols[0].button(
        artifact_label,
        key=f"artifact_{item.get('message_guid', artifact_label)}",
        use_container_width=True,
    ):
        st.session_state["artifact_id"] = item.get("artifact_id")
        st.session_state["message_guid"] = item.get("message_guid")
        st.switch_page("pages/analysis.py")

    cols[1].markdown(item.get("package_id", "-"))
    cols[2].code(item.get("message_guid", "-"), language="")
    cols[3].code(item.get("correlation_id", "-"), language="")
    cols[4].markdown(format_duration(item.get("log_start"), item.get("log_end")))
    cols[5].markdown(status_badge(item.get("status", "-")), unsafe_allow_html=True)
