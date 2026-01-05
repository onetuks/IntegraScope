from typing import List, Any

import streamlit as st

from app.client.components.tested_artifact import TestedArtifact


def render_list(artifacts: List[Any]):
    if not artifacts:
        return

    st.success(f"{len(artifacts)}건의 테스트가 조회되었습니다.")

    title_cols = st.columns([5, 1])
    title_cols[0].markdown("#### Tested Flow List")
    header_cols = st.columns([4, 3, 1])
    header_cols[0].markdown("**Package / Artifact**")
    header_cols[1].markdown("**Message / Correlation**")
    header_cols[2].markdown("**Status / Duration**")

    for item in artifacts:
        TestedArtifact(item).render_artifact()