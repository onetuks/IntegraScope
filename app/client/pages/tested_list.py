from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

from app.client.api.api_client import get
from app.client.components.tested_artifact import TestedArtifact
from app.client.components.time_period import TestedFetch, TestStatus


def fetch_tested(log_start: datetime, log_end: datetime, status: TestStatus) -> \
        Tuple[
            Optional[List[Dict[str, Any]]], Optional[str]]:
    try:
        response = get(f"/api/tested"
                       f"?status={status}"
                       f"&log_start={log_start.isoformat()}"
                       f"&log_end={log_end.isoformat()}")
        data = response.json()
        return data.get("tested_artifacts", []), None
    except Exception as exc:
        return None, str(exc)

def render_list():
    if not st.session_state["tested_artifacts"]:
        return

    title_cols = st.columns([5, 1])
    title_cols[0].markdown("#### Tested Flow List")
    header_cols = st.columns([4, 3, 1])
    header_cols[0].markdown("**Package / Artifact**")
    header_cols[1].markdown("**Message / Correlation**")
    header_cols[2].markdown("**Status / Duration**")

    for idx, item in enumerate(st.session_state["tested_artifacts"]):
        TestedArtifact(item).render_artifact()


st.title("Tested iFlows")
st.caption("최근 테스트된 iFlow 실행 결과 목록")

if "tested_artifacts" not in st.session_state:
    st.session_state["tested_artifacts"] = []
if "tested_error" not in st.session_state:
    st.session_state["tested_error"] = None

if "tested_fetch" not in st.session_state:
    tested_fetch = TestedFetch()
    st.session_state["tested_fetch"] = tested_fetch
else:
    tested_fetch = st.session_state["tested_fetch"]
fetch_button = tested_fetch.render_component()

render_list()

if fetch_button:
    if tested_fetch.stored_start >= tested_fetch.stored_end:
        st.error("시작 시간이 종료 시간보다 같거나 늦을 수 없습니다.")
        st.session_state["tested_artifacts"] = []
        st.session_state["tested_error"] = "시간 설정 오류"
    else:
        with st.spinner("테스트 실행 결과를 불러오는 중..."):
            st.session_state["tested_artifacts"], st.session_state["tested_error"] = fetch_tested(
                tested_fetch.stored_start,
                tested_fetch.stored_end,
                tested_fetch.status)

        render_list()

else:
    st.session_state["tested_artifacts"] = []
    st.session_state["tested_error"] = None

if st.session_state["tested_error"]:
    st.error(f"테스트 목록을 불러오지 못했습니다: {st.session_state['tested_error']}")
    st.stop()

if not st.session_state["tested_artifacts"]:
    st.info("표시할 테스트 실행 결과가 없습니다.")
    st.stop()
