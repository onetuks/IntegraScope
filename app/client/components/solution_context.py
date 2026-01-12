from typing import Dict, Any, List

import streamlit as st


class SolutionContext:

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def render_component(self):
        with st.container(border=True):
            st.subheader("Solutions")
            solutions: List[Dict[str, Any]] = self.data.get("solutions") or []
            if not solutions:
                st.info("제안된 해결책이 없습니다.")
                return
            for idx, plan in enumerate(solutions, start=1):
                with st.container(border=True):
                    st.markdown(f"**{idx}. {plan.get('fix_plan', '-')}**")
                    check_list = plan.get("check_list") or []
                    for checklist in check_list:
                        st.markdown(f"- **{checklist.get('target', '-')}**")
                        for point in checklist.get("check_points") or []:
                            st.write(f"  • {point}")
                        if checklist.get("expected"):
                            st.caption(f"  기대 결과: {checklist['expected']}")

                    if plan.get("prove_senario"):
                        st.markdown("**검증 시나리오**")
                        st.write(plan["prove_senario"])

                    if plan.get("prevention"):
                        st.markdown("**예방 가이드**")
                        st.write(plan["prevention"])

                    extra_data = plan.get("additional_data_needed") or []
                    if extra_data:
                        st.markdown("**추가 필요 데이터**")
                        for item in extra_data:
                            st.write(
                                f"- {item.get('data', '-')}: {item.get('reason', '-')}")
                            st.caption(f"  확보 방법: {item.get('how', '-')}")