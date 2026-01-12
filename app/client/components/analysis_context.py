from typing import List, Dict, Any

import streamlit as st


class AnalysisContext:

    def __init__(self, analysis):
        self.analysis = analysis

    def render_component(self):
        with st.container(border=True):
            st.subheader("Analysis")
            st.markdown("**Summary**")
            st.markdown(f"{self.analysis.get('summary', '-')}")

            classification = self.analysis.get("classification") or {}
            class_cols = st.columns([1, 1])
            if classification.get("category"):
                for category in classification.get("category", []):
                    class_cols[0].badge(category, color="orange")
            else:
                class_cols[0].badge("-", color="orange")
            # class_cols[0].badge(classification.get("category", "-"), color="orange")
            class_cols[1].markdown("**Confidence**")
            class_cols[1].badge(f"{classification.get('confidence', 0.0) * 100:.0f}%",
                                color="blue")

            st.markdown("**Top Causes**")
            top_causes: List[Dict[str, Any]] = self.analysis.get("top_causes") or []
            if not top_causes:
                st.info("원인 후보가 아직 없습니다.")
            for cause in top_causes:
                with st.expander(cause.get("hypothesis", "원인"), expanded=False):
                    cols = st.columns(2)
                    evidence = cause.get("evidence") or []
                    if evidence:
                        cols[0].markdown("**Evidence**")
                        for item in evidence:
                            cols[0].write(f"- {item}")
                    verification = cause.get("how_to_verify") or []
                    if verification:
                        cols[1].markdown("**How to verify**")
                        for item in verification:
                            cols[1].write(f"- {item}")

            st.markdown("**Questions for you**")
            for question in self.analysis.get("question_for_user", []):
                st.write(f"- {question}")

            st.markdown("**Additional data needed**")
            for item in self.analysis.get("additional_data_needed", []):
                with st.container(border=True):
                    st.markdown(f"**{item.get('data', '-')}**")
                    st.write(f"이유: {item.get('reason', '-')}")
                    st.write(f"확보 방법: {item.get('how', '-')}")