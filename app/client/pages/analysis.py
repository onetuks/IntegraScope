from typing import Any, Dict, Optional, Tuple

import streamlit as st
from requests import Response

from app.client.api.api_client import post
from app.client.components.analysis_context import AnalysisContext
from app.client.components.overview_context import ArtifactContext
from app.client.components.solution_context import SolutionContext

_ANALYSIS_STATE_DEFAULTS = {
    "data": {},
    "analysis_and_resolve": False,
    "overview_fetched": False,
    "analysis_fetched": False,
    "solution_fetched": False,
}


def _reset_analysis_state() -> None:
    for key, value in _ANALYSIS_STATE_DEFAULTS.items():
        st.session_state[key] = value


def _init_session_state() -> None:
    defaults = {
        "message_guid": None,
        "analysis_last_message_guid": None,
    }
    defaults.update(_ANALYSIS_STATE_DEFAULTS)
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    current_guid = st.session_state.get("message_guid")
    last_guid = st.session_state.get("analysis_last_message_guid")
    if current_guid != last_guid:
        _reset_analysis_state()
        st.session_state["analysis_last_message_guid"] = current_guid


def _fetch_resolve_with_analysis(message_guid_: str) -> Tuple[
    Optional[Dict[str, Any]], Optional[str]]:
    if not message_guid_:
        return None, "Artifact ID가 필요합니다."
    try:
        response: Response = post(
            uri="/api/resolve-with-analysis",
            body={"message_guid": message_guid_},
            timeout=180
        )
        return response.json(), None
    except Exception as exc:
        return None, str(exc)


def _fetch_error_log(message_guid_: str) -> Tuple[
    Optional[Dict[str, Any]], Optional[str]]:
    if not message_guid_:
        return None, "Artifact ID가 필요합니다."
    try:
        response: Response = post(
            uri="/api/error-log",
            body={"message_guid": message_guid_},
            timeout=180
        )
        return response.json(), None
    except Exception as exc:
        return None, str(exc)


def _fetch_analysis(message_guid_: str, data_: Dict[str, Any]) -> Tuple[
    Optional[Dict[str, Any]], Optional[str]]:
    if not message_guid_:
        return None, "Artifact ID가 필요합니다."
    try:
        response: Response = post(
            uri="/api/analysis",
            body={
                "message_guid": message_guid_,
                "artifact_id": data_.get("artifact_id"),
                "artifact_type": data_.get("artifact_type"),
                "package_id": data_.get("package_id"),
                "log_start": data_.get("log_start"),
                "log_end": data_.get("log_end"),
                "log": data_.get("log"),
                "origin_log": data_.get("origin_log"),
                "status_code": data_.get("status_code"),
                "exception": data_.get("exception")
            },
            timeout=180
        )
        return response.json(), None
    except Exception as exc:
        return None, str(exc)


def _fetch_solution(message_guid_: str, data_: Dict[str, Any]) -> Tuple[
    Optional[Dict[str, Any]], Optional[str]
]:
    if not message_guid:
        return None, "Artifact ID가 필요합니다."
    try:
        response: Response = post(
            uri="/api/solutions",
            body={
                "message_guid": message_guid_,
                "artifact_id": data_.get("artifact_id"),
                "artifact_type": data_.get("artifact_type"),
                "package_id": data_.get("package_id"),
                "log_start": data_.get("log_start"),
                "log_end": data_.get("log_end"),
                "log": data_.get("log"),
                "origin_log": data_.get("origin_log"),
                "status_code": data_.get("status_code"),
                "exception": data_.get("exception"),
                "analysis": data_.get("analysis"),
            },
            timeout=180
        )
        return response.json(), None
    except Exception as exc:
        return None, str(exc)


def _current_step() -> str:
    if st.session_state["analysis_and_resolve"]:
        return "all"
    elif (not st.session_state["overview_fetched"]
          and not st.session_state["analysis_fetched"]
          and not st.session_state["solution_fetched"]
    ):
        return "overview"
    elif (st.session_state["overview_fetched"]
          and not st.session_state["analysis_fetched"]
          and not st.session_state["solution_fetched"]
    ):
        return "analysis"
    elif (st.session_state["analysis_fetched"]
          and not st.session_state["solution_fetched"]
    ):
        return "solution"
    return "done"


def _bind_overview_data(overview: Dict[str, Any]):
    st.session_state["overview_fetched"] = True
    data["artifact_id"] = overview.get("artifact_id")
    data["artifact_type"] = overview.get("artifact_type")
    data["package_id"] = overview.get("package_id")
    data["message_guid"] = overview.get("message_guid")
    data["log_start"] = overview.get("log_start")
    data["log_end"] = overview.get("log_end")
    data["log"] = overview.get("log")
    data["origin_log"] = overview.get("origin_log")
    data["status_code"] = overview.get("status_code")
    data["exception"] = overview.get("exception")


def _bind_analysis_data(analysis: Dict[str, Any]):
    st.session_state["analysis_fetched"] = True
    data["analysis"] = analysis


def _bind_solution_data(solution: Dict[str, Any]):
    st.session_state["solution_fetched"] = True
    data["solution"] = solution


def _bind_resolve_with_analysis_data(full_data: Dict[str, Any]):
    st.session_state["analysis_and_resolve"] = True
    _bind_overview_data(full_data)
    data["analysis"] = full_data.get("analysis")
    data["solution"] = full_data.get("solution")


def render_data_fetch():
    fetch_cols = st.columns([3, 1, 1])
    st.session_state["message_guid"] = fetch_cols[0].text_input(
        label="Message Guid",
        value=st.session_state.get(
            "message_guid"),
        placeholder="예) INTEGRA_SCOPE_TEST")
    fetch_cols[1].container(height=10, border=False)
    fetch_clicked = fetch_cols[1].button("Analyze & Solution", type="primary",
                                         use_container_width=True)
    fetch_cols[2].container(height=10, border=False)
    if fetch_cols[2].button("Clear", type="secondary",
                            use_container_width=True):
        st.session_state["data"] = {}
        _reset_analysis_state()
        st.rerun()

    if fetch_clicked:
        with st.spinner("분석 결과를 불러오는중..."):
            _data, _error = _fetch_resolve_with_analysis(message_guid.strip())
        if _data:
            _bind_resolve_with_analysis_data(_data)
            st.success("오류 분석에 성공했습니다")
        else:
            st.error(f"오류 분석 실패: {_error}")


def render_overview():
    def _showable():
        return st.session_state["overview_fetched"]

    if _showable():
        ArtifactContext(data).render_component()
        return

    if _current_step() == "all" or (
            _current_step() == "overview" and st.button("Fetch Error Overview",
                                                        width="stretch")):
        with st.spinner("오류 정보를 불러오는 중"):
            _data, _error = _fetch_error_log(message_guid_=message_guid)
        if _data:
            _bind_overview_data(_data)
            st.success("오류 정보 조회에 성공했습니다")
            ArtifactContext(data).render_component()
        else:
            st.error(f"오류 정보 조회 실패: {_error}")


def render_analysis():
    def _showable():
        return st.session_state["analysis_fetched"]

    if _showable():
        AnalysisContext(data.get("analysis")).render_component()
        return

    if _current_step() == "all" or (_current_step() == "analysis" and st.button(
            "Request Error Analysis",
            width="stretch")):
        with st.spinner("오류 분석하는 중"):
            _data, _error = _fetch_analysis(message_guid_=message_guid,
                                            data_=data)
        if _data:
            analysis = _data.get("analysis")
            _bind_analysis_data(analysis)
            st.success("오류 분석에 성공했습니다")
            AnalysisContext(analysis).render_component()
        else:
            st.error(f"오류 분석 실패: {_error}")


def render_solutions():
    def _showable():
        return st.session_state["solution_fetched"]

    if _showable():
        SolutionContext(data.get("solution")).render_component()
        return

    if _current_step() == "all" or (_current_step() == "solution" and st.button(
            "Request Error Solution",
            width="stretch")):
        with st.spinner("오류 해결책 도출하는 중"):
            _data, _error = _fetch_solution(message_guid_=message_guid,
                                            data_=data)
        if _data:
            solution = _data.get("solution")
            _bind_solution_data(solution)
            st.success("오류 해결책 도출에 성공했습니다")
            SolutionContext(solution).render_component()
        else:
            st.error(f"오류 해결책 도출 실패: {_error}")


st.title("Error Analysis")
st.caption("iFlow 장애 로그를 받아 분석/해결 가이드를 한눈에 확인하세요.")

st.markdown(
    """
    <style>
    .pill {
        display: inline-flex;
        padding: 4px 10px;
        border-radius: 999px;
        color: #f8fafc;
        font-size: 0.85rem;
        font-weight: 600;
    }
    [data-testid="stExpander"] details summary {
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

_init_session_state()
data = st.session_state["data"]
message_guid = st.session_state["message_guid"]
render_data_fetch()

st.divider()

render_overview()
render_analysis()
render_solutions()

if data.get("solution"):
    with st.expander("Raw payload 보기"):
        st.json(data)
