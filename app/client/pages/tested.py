from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

from app.client.api.api_client import get
from app.client.utils.utils import format_duration, get_default_time_period


def fetch_tested(log_start: str, log_end: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    try:
        response = get(f"/api/tested?log_start={log_start}&log_end={log_end}")
        data = response.json()
        return data.get("tested_artifacts", []), None
    except Exception as exc:
        return None, str(exc)


default_start, default_end = get_default_time_period()

stored_start = st.session_state.get("tested_start_dt", default_start)
stored_end = st.session_state.get("tested_end_dt", default_end)


def render_time_period():
    global artifacts

    col_range = st.columns([1, 1, 0.5])
    start_dt = col_range[0].datetime_input("Log Start", value=stored_start)
    end_dt = col_range[1].datetime_input("Log End", value=stored_end)
    col_range[2].container(height=10, border=False)
    refresh = col_range[2].button("Fetch", type="primary", use_container_width=True)

    log_start_param = start_dt.isoformat()
    log_end_param = end_dt.isoformat()

    if refresh:
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
        if "tested_artifacts" not in st.session_state:
            st.info("시간 설정 후 조회해주세요.")
            st.stop()
        st.info("표시할 테스트 실행 결과가 없습니다.")
        st.stop()


def render_tested_list():
    st.markdown("#### Tested Flow List")

    header_cols = st.columns([4, 3, 1])
    header_cols[0].markdown("**Package / Artifact**")
    header_cols[1].markdown("**Message / Correlation**")
    header_cols[2].markdown("**Status / Duration**")

    seen_guids = set()
    for idx, item in enumerate(artifacts):
        msg_guid = item.get("message_guid")
        if msg_guid in seen_guids:
            continue
        seen_guids.add(msg_guid)

        row_key = msg_guid or f"row_{idx}_{item.get('artifact_id', 'artifact')}"
        container = st.container(border=True)
        cols = container.columns([4, 3, 1])

        cols[0].text_input(
            label="Package Id",
            value=item.get("package_id", "-"),
            key=f"{row_key}_package",
            disabled=True,
        )
        cols[0].text_input(
            label="Artifact Id",
            value=item.get("artifact_id", "-"),
            key=f"{row_key}_artifact",
            disabled=True,
        )

        cols[1].text_input(
            label="Message GUID",
            value=msg_guid or "-",
            key=f"{row_key}_message_guid",
            disabled=True,
        )
        cols[1].text_input(
            label="Correlation Id",
            value=item.get("correlation_id", "-"),
            key=f"{row_key}_correlation",
            disabled=True,
        )

        status_color = (
            "red"
            if item.get("status", "-") == "FAILED"
            else "green"
            if item.get("status") == "COMPLETED"
            else "orange"
        )
        cols[2].badge(item.get("status", "-"), color=status_color)
        cols[2].caption(format_duration(item.get("log_start"), item.get("log_end")))
        cols[2].caption(item.get("log_start").replace("T", " ")[:-8])
        if cols[2].button(
                label="Analyze",
                use_container_width=True,
                type="primary",
                key=f"analyze_btn_{row_key}",
        ):
            st.session_state["message_guid"] = msg_guid
            st.switch_page("pages/analysis.py")


st.title("Tested iFlows")
st.caption("최근 테스트된 iFlow 실행 결과 목록")

artifacts = list()
render_time_period()
render_tested_list()
