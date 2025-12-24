from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st
from requests import Response

from app.client.api.api_client import post
from app.client.utils.utils import format_duration


def fetch_analysis(message_guid: str) -> Tuple[
    Optional[Dict[str, Any]], Optional[str]]:
    if not message_guid:
        return None, "Artifact ID가 필요합니다."
    try:
        response: Response = post(
            uri="/api/analysis",
            body={"message_guid": message_guid},
            timeout=180
        )
        return response.json(), None
    except Exception as exc:
        return None, str(exc)


def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    try:
        return parsedate_to_datetime(value) if value else None
    except Exception:
        return None


def format_datetime(value: Optional[str]) -> str:
    dt_value = parse_datetime(value)
    return dt_value.strftime("%Y-%m-%d %H:%M:%S %Z") if dt_value else "-"


def render_overview(payload: Dict[str, Any]):
    with st.container(border=True):
        st.subheader("Artifact Context")

        st.badge(payload.get("artifact_type"))
        meta_cols = st.columns([1, 1])
        meta_cols[0].text_input(label="Artifact Id",
                                value=payload.get("artifact_id", "-"),
                                disabled=False)
        meta_cols[1].text_input(label="Package Id",
                                value=payload.get("package_id", "-"),
                                disabled=False)
        meta_cols[0].text_input(label="Message GUID",
                                value=payload.get("message_guid", "-"),
                                disabled=False)

        st.divider()

        info_cols = st.columns([6, 1])
        info_cols[0].text_input(label="Exception",
                                value=payload.get("exception", "-"),
                                disabled=False)
        info_cols[1].caption("Status Code")
        info_cols[1].container().badge(str(payload.get("status_code", "-")),
                                       width="stretch", color="red")
        info_cols[1].caption("Duration")
        info_cols[1].badge(format_duration(payload.get("log_start", "-"),
                                           payload.get("log_end", "-")))
        time_cols = info_cols[0].columns([1, 1])
        time_cols[0].caption("Log Start")
        time_cols[0].badge(f"{format_datetime(payload.get('log_start'))}",
                           color="green")
        time_cols[1].caption("Log End")
        time_cols[1].badge(f"{format_datetime(payload.get('log_end'))}",
                           color="green")

        st.markdown("**Error Log**")
        st.code(payload.get("origin_log", ""), language="bash")


def render_analysis(analysis: Dict[str, Any]):
    with st.container(border=True):
        st.subheader("Analysis")
        st.markdown("**Summary**")
        st.markdown(f"{analysis.get('summary', '-')}")

        classification = analysis.get("classification") or {}
        class_cols = st.columns([1, 1])
        if classification.get("category"):
            for category in classification.get("category"):
                class_cols[0].badge(category, color="orange")
        else:
            class_cols[0].badge("-", color="orange")
        # class_cols[0].badge(classification.get("category", "-"), color="orange")
        class_cols[1].markdown("**Confidence**")
        class_cols[1].badge(f"{classification.get('confidence') * 100:.0f}%",
                            color="blue")

        st.markdown("**Top Causes**")
        top_causes: List[Dict[str, Any]] = analysis.get("top_causes") or []
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
        for question in analysis.get("question_for_user", []):
            st.write(f"- {question}")

        st.markdown("**Additional data needed**")
        for item in analysis.get("additional_data_needed", []):
            with st.container(border=True):
                st.markdown(f"**{item.get('data', '-')}**")
                st.write(f"이유: {item.get('reason', '-')}")
                st.write(f"확보 방법: {item.get('how', '-')}")


def render_solutions(solution: Dict[str, Any]):
    with st.container(border=True):
        st.subheader("Solutions")
        solutions: List[Dict[str, Any]] = solution.get("solutions") or []
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


def render_data_fetch() -> Dict[str, Any]:
    _payload: Dict[str, Any] = {}

    fetch_cols = st.columns([3, 1])
    message_guid = fetch_cols[0].text_input(label="Message Guid",
                                            value=st.session_state.get(
                                                "message_guid"),
                                            placeholder="예) INTEGRA_SCOPE_TEST")
    fetch_cols[1].container(height=10, border=False)
    fetch_clicked = fetch_cols[1].button("Analyze & Solution", type="primary",
                                         use_container_width=True)

    if fetch_clicked:
        with st.spinner("분석 결과를 불러오는중..."):
            data, error = fetch_analysis(message_guid.strip())
        if data:
            _payload = data
            st.success("오류 분석에 성공했습니다")
        else:
            st.error(f"오류 분석 실패: {error}")

    st.divider()

    if not _payload:
        st.info("분석 데이터를 불러와 주세요.")
        st.stop()

    return _payload


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

payload: Dict[str, Any] = render_data_fetch()
render_overview(payload)
render_analysis(payload.get("analysis") or {})
render_solutions(payload.get("solution") or {})

with st.expander("Raw payload 보기"):
    st.json(payload)
