from typing import List, Optional

import streamlit as st

from app.client.api.api_client import get
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


def reset_results() -> None:
    st.session_state["searched_artifacts"] = []
    st.session_state["searched_error"] = None
    st.session_state["searched_has_fetched"] = False


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


def fetch_package_list() -> List[str]:
    try:
        response = get("/api/packages")
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return []


def fetch_artifact_list(package_id: str) -> List[str]:
    try:
        response = get(f"/api/artifacts?package_id={package_id}")
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return []


def load_packages(force: bool = False) -> None:
    """Fetch packages once on first load or when refresh is requested."""
    if not force and st.session_state["package_list"]:
        return

    with st.spinner("패키지 목록을 불러오는 중..."):
        packages = fetch_package_list()

    st.session_state["package_list"] = packages
    st.session_state["selected_package"] = packages[0] if packages else None
    st.session_state["artifact_list"] = []
    st.session_state["selected_artifact"] = None
    reset_results()
    if st.session_state["selected_package"]:
        load_artifacts(st.session_state["selected_package"])


def load_artifacts(package_id: Optional[str]) -> None:
    if not package_id:
        st.session_state["artifact_list"] = []
        st.session_state["selected_artifact"] = None
        reset_results()
        return

    with st.spinner("Artifact 목록을 불러오는 중..."):
        artifacts = fetch_artifact_list(package_id)

    st.session_state["artifact_list"] = artifacts
    st.session_state["selected_artifact"] = artifacts[0] if artifacts else None
    reset_results()


load_packages()

cols = st.columns([1.25, 1.25, 0.5])
cols[2].container(height=10, border=False)
if cols[2].button("패키지 목록 새로고침", width="stretch"):
    load_packages(force=True)

if not st.session_state["package_list"]:
    st.info("패키지 목록이 없습니다. 새로고침을 눌러 재조회해주세요.")
    st.stop()

selected_pkg = st.session_state["selected_package"]
pkg_index = 0
if selected_pkg in st.session_state["package_list"]:
    pkg_index = st.session_state["package_list"].index(selected_pkg)
package_id = cols[0].selectbox(
    label="Package Id",
    options=st.session_state["package_list"],
    index=pkg_index,
)

if package_id != st.session_state["selected_package"]:
    st.session_state["selected_package"] = package_id
    load_artifacts(package_id)

artifact_options = st.session_state["artifact_list"]
if artifact_options:
    art_index = 0
    if st.session_state["selected_artifact"] in artifact_options:
        art_index = artifact_options.index(
            st.session_state["selected_artifact"])
    previous_artifact = st.session_state["selected_artifact"]
    artifact_id = cols[1].selectbox(
        label="Artifact Id",
        options=artifact_options,
        index=art_index,
    )
    if artifact_id != previous_artifact:
        reset_results()
    st.session_state["selected_artifact"] = artifact_id
else:
    st.info("선택한 패키지의 Artifact가 없습니다.")

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
