from typing import List

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from app.client.api.api_client import get
from app.client.components.select_artifact import load_artifacts, reset_results


def _fetch_package_list() -> List[str]:
    try:
        response = get("/api/packages")
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return []


def load_packages(force: bool = False) -> None:
    """Fetch packages once on first load or when refresh is requested."""
    if not force and st.session_state["package_list"]:
        return

    with st.spinner("패키지 목록을 불러오는 중..."):
        packages = _fetch_package_list()

    st.session_state["package_list"] = packages
    st.session_state["selected_package"] = packages[0] if packages else None
    st.session_state["artifact_list"] = []
    st.session_state["selected_artifact"] = None
    reset_results()
    if st.session_state["selected_package"]:
        load_artifacts(st.session_state["selected_package"])


def render_package_select_box(cols: list[DeltaGenerator]):
    load_packages()

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
