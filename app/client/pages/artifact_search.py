import streamlit as st

from app.client.components.select_artifact import render_artifact_select_box
from app.client.components.select_package import render_package_select_box
from app.client.components.tested_artifact import TestedArtifact
from app.client.components.tested_fetch import TestedFetch
from app.client.pages import fetch_tested


def init_session_state() -> None:
    defaults = {
        "searched_artifacts": [],
        "searched_error": None,
        "searched_has_fetched": False,
        "package_list": [],
        "artifact_list": [],
        "selected_package": None,
        "selected_artifact": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_list(artifacts):
    if not artifacts:
        return

    title_cols = st.columns([5, 1])
    title_cols[0].markdown("#### Tested Flow List")
    header_cols = st.columns([4, 3, 1])
    header_cols[0].markdown("**Package / Artifact**")
    header_cols[1].markdown("**Message / Correlation**")
    header_cols[2].markdown("**Status / Duration**")

    for item in artifacts:
        TestedArtifact(item).render_artifact()


st.title("Artifact Search")
st.caption("검색한 Artifact 테스트 실행 결과 목록")

init_session_state()
cols = st.columns([1.25, 1.25, 0.5])
render_package_select_box(cols)
render_artifact_select_box(cols)



if "searched_fetch" not in st.session_state:
    searched_fetch = TestedFetch()
    st.session_state["searched_fetch"] = searched_fetch
else:
    searched_fetch = st.session_state["searched_fetch"]
fetch_button = searched_fetch.render_component()

if fetch_button:
    if searched_fetch.stored_start >= searched_fetch.stored_end:
        st.error("시작 시간이 종료 시간보다 같거나 늦을 수 없습니다.")
        st.session_state["searched_artifacts"] = []
        st.session_state["searched_error"] = "시간 설정 오류"
        st.session_state["searched_has_fetched"] = False
    elif not st.session_state["selected_artifact"]:
        st.warning("Artifact를 선택해주세요.")
    else:
        with st.spinner("테스트 실행 결과를 불러오는 중..."):
            artifacts, error = fetch_tested(
                searched_fetch.stored_start,
                searched_fetch.stored_end,
                searched_fetch.status,
                artifact_id=st.session_state["selected_artifact"])

        st.session_state["searched_artifacts"] = artifacts or []
        st.session_state["searched_error"] = error
        st.session_state["searched_has_fetched"] = error is None

artifacts = st.session_state["searched_artifacts"]
error = st.session_state["searched_error"]
has_fetched = st.session_state["searched_has_fetched"]

if error:
    st.error(f"테스트 목록을 불러오지 못했습니다: {error}")
    st.stop()

if not artifacts:
    if not has_fetched:
        st.info("조건을 선택 후 조회해주세요.")
        st.stop()
    st.info("표시할 테스트 실행 결과가 없습니다.")
    st.stop()

render_list(artifacts)
