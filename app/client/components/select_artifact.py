from typing import List, Optional

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from app.client.api.api_client import get


def _fetch_artifact_list(package_id: str) -> List[str]:
    try:
        response = get(f"/api/artifacts?package_id={package_id}")
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        return []


def reset_results() -> None:
    st.session_state["searched_artifacts"] = []
    st.session_state["searched_error"] = None


def load_artifacts(package_id: Optional[str]) -> None:
    if not package_id:
        st.session_state["artifact_list"] = []
        st.session_state["selected_artifact"] = None
        reset_results()
        return

    with st.spinner("Artifact 목록을 불러오는 중..."):
        artifacts = _fetch_artifact_list(package_id)

    st.session_state["artifact_list"] = artifacts
    st.session_state["selected_artifact"] = artifacts[0] if artifacts else None
    reset_results()


def render_artifact_select_box(cols: list[DeltaGenerator]):
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