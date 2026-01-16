import streamlit as st

from app.client.components.fetch_option import TestedFetch
from app.client.components.tested_list import render_list
from app.client.exception.SessionStateError import SessionStateInfo, \
    SessionStateError, SessionStateWarning
from app.client.pages import fetch_tested


def _init_session_state() -> None:
    defaults = {
        "tested_artifacts": [],
        "tested_error": None,
        "tested_fetch": TestedFetch(),
        "tested_has_run": False,
        "tested_page": 0,
        "tested_page_size": 20,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _validate_error_state():
    error_ = st.session_state["tested_error"]
    if error_:
        raise SessionStateError(f"테스트 목록을 불러오지 못했습니다: {error_}")


def _validate_tested_artifact():
    artifacts_ = st.session_state["tested_artifacts"]
    if not artifacts_ and st.session_state["tested_page"] == 0:
        raise SessionStateInfo("표시할 테스트 실행 결과가 없습니다.")


def load_data(reset_page=False):
    tested_fetch = st.session_state["tested_fetch"]
    try:
        tested_fetch.validate_time()
        
        if reset_page:
            st.session_state["tested_page"] = 0
            
        page = st.session_state["tested_page"]
        page_size = st.session_state["tested_page_size"]
        skip = page * page_size

        with st.spinner("테스트 실행 결과를 불러오는 중..."):
            artifacts, error = fetch_tested(
                tested_fetch.stored_start,
                tested_fetch.stored_end,
                tested_fetch.status,
                skip=skip,
                top=page_size
            )

        st.session_state["tested_artifacts"] = artifacts or []
        st.session_state["tested_error"] = error
        st.session_state["tested_has_run"] = True
    except ValueError as e:
        st.session_state["tested_artifacts"] = []
        st.session_state["tested_error"] = str(e)
        st.session_state["tested_has_run"] = True


st.title("Tested Artifacts")
st.caption("최근 테스트된 Artifact 실행 결과 목록")
_init_session_state()
tested_fetch = st.session_state["tested_fetch"]
fetch_button = tested_fetch.render_component()

if fetch_button:
    load_data(reset_page=True)

if st.session_state["tested_has_run"]:
    try:
        _validate_error_state()
        _validate_tested_artifact()
        
        render_list(st.session_state["tested_artifacts"])
        
        # Pagination Controls
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if st.session_state["tested_page"] > 0:
                if st.button("이전 페이지", width="stretch"):
                    st.session_state["tested_page"] -= 1
                    load_data()
                    st.rerun()
        
        with col_page:
            st.markdown(f"<div style='text-align: center'>Page {st.session_state['tested_page'] + 1}</div>", unsafe_allow_html=True)
            
        with col_next:
            # If we received a full page, there might be more
            if len(st.session_state["tested_artifacts"]) == st.session_state["tested_page_size"]:
                if st.button("다음 페이지", width="stretch"):
                    st.session_state["tested_page"] += 1
                    load_data()
                    st.rerun()

    except SessionStateWarning as e:
        st.warning(str(e))
    except SessionStateError as e:
        st.error(str(e))
        st.stop()
    except SessionStateInfo as e:
        st.info(str(e))
        st.stop()
