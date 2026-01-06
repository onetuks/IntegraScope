import streamlit as st

from app.client.components.fetch_option import TestedFetch
from app.client.components.select_artifact import render_artifact_select_box
from app.client.components.select_package import render_package_select_box
from app.client.components.tested_list import render_list
from app.client.exception.SessionStateError import SessionStateWarning, \
    SessionStateError, SessionStateInfo
from app.client.pages import fetch_tested


def _init_session_state() -> None:
    defaults = {
        "searched_artifacts": [],
        "searched_error": None,
        "searched_fetch": TestedFetch(),
        "package_list": [],
        "artifact_list": [],
        "selected_package": None,
        "selected_artifact": None,
        "searched_has_run": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _validate_selected_artifact():
    if not st.session_state["selected_artifact"] or st.session_state[
        "selected_artifact"] is None:
        raise SessionStateWarning("Artifact를 선택해주세요.")


def _validate_error_state():
    error_ = st.session_state["searched_error"]
    if error_:
        raise SessionStateError(f"테스트 목록을 불러오지 못했습니다: {error_}")


def _validate_searched_artifact():
    artifacts_ = st.session_state["searched_artifacts"]
    if not artifacts_:
        raise SessionStateInfo("표시할 테스트 실행 결과가 없습니다.")


st.title("Artifact Search")
st.caption("검색한 Artifact 테스트 실행 결과 목록")

_init_session_state()
cols = st.columns([1.25, 1.25, 0.5])
render_package_select_box(cols)
render_artifact_select_box(cols)
searched_fetch = st.session_state["searched_fetch"]
fetch_button = searched_fetch.render_component()

if fetch_button:
    try:
        searched_fetch.validate_time()
        _validate_selected_artifact()

        with st.spinner("테스트 실행 결과를 불러오는 중..."):
            artifacts, error = fetch_tested(
                searched_fetch.stored_start,
                searched_fetch.stored_end,
                searched_fetch.status,
                artifact_id=st.session_state["selected_artifact"])

        st.session_state["searched_artifacts"] = artifacts or []
        st.session_state["searched_error"] = error
        st.session_state["searched_has_run"] = True
    except SessionStateWarning as e:
        st.warning(str(e))
    except ValueError as e:
        st.session_state["searched_artifacts"] = []
        st.session_state["searched_error"] = str(e)
        st.session_state["searched_has_run"] = True

if st.session_state["searched_has_run"]:
    try:
        _validate_error_state()
        _validate_searched_artifact()
        render_list(st.session_state["searched_artifacts"])
    except SessionStateError as e:
        st.error(str(e))
        st.stop()
    except SessionStateInfo as e:
        st.info(str(e))
        st.stop()
