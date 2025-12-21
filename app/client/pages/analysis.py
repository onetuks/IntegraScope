import json
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any, Dict, List, Optional, Tuple
import streamlit as st
from requests import Response

from app.client.api.api_client import post

# EXAMPLE_ANALYSIS: Dict[str, Any] = {
#     "artifact_id": "INTEGRA_SCOPE_TEST",
#     "artifact_type": "INTEGRATION_FLOW",
#     "package_id": "TEST10192",
#     "message_guid": "AGlB9IyPbfLAFZWFtlMprIJf8JYp",
#     "log_start": "Wed, 17 Dec 2025 00:08:44 +0000",
#     "log_end": "Wed, 17 Dec 2025 00:08:46 +0000",
#     "log": (
#         "com.sap.it.rt.adapter.http.api.exception.HttpResponseException: "
#         "An internal server error occured: HTTP operation failed invoking <URL> "
#         "with statusCode: 404."
#     ),
#     "status_code": 404,
#     "exception": "com.sap.it.rt.adapter.http.api.exception.HttpResponseException",
#     "analysis": {
#         "summary": (
#             "외부 시스템(Receiver) 호출 시 요청한 리소스를 찾을 수 없어 "
#             "HTTP 404 Not Found 응답이 발생했습니다."
#         ),
#         "classification": {
#             "category": "ADAPTER_CONFIG",
#             "confidence": 0.9,
#         },
#         "top_causes": [
#             {
#                 "hypothesis": "Receiver 어댑터에 설정된 엔드포인트 URL 또는 자원 경로(Resource Path)가 잘못됨",
#                 "evidence": [
#                     "statusCode: 404",
#                     "HTTP operation failed invoking <URL>",
#                 ],
#                 "how_to_verify": [
#                     "Integration Flow의 HTTP/OData/SOAP 어댑터 설정에서 'Address' 필드의 URL 오탈자 확인",
#                     "호출하려는 외부 시스템의 API 가이드를 참조하여 Resource Path가 정확한지 대조",
#                     "Postman 등 외부 도구를 사용하여 동일한 URL로 직접 호출 시도",
#                 ],
#             },
#             {
#                 "hypothesis": "Content Modifier 또는 Script를 통해 동적으로 생성된 URL/쿼리 파라미터 오류",
#                 "evidence": [
#                     "invoking <URL> with statusCode: 404",
#                 ],
#                 "how_to_verify": [
#                     "CamelHttpUri, CamelHttpPath, CamelHttpQuery 헤더가 런타임에 어떻게 변경되는지 Trace 모드에서 확인",
#                     "URL에 포함된 동적 변수(Property/Header)에 공백이나 특수문자가 포함되어 인코딩 문제가 발생하는지 확인",
#                     "스크립트 내에서 URL을 구성하는 로직이 유효한 값을 반환하는지 검증",
#                 ],
#             },
#             {
#                 "hypothesis": "SAP Cloud Connector를 통한 온프레미스 연결 시 'Resources' 권한 설정 누락",
#                 "evidence": [
#                     "statusCode: 404",
#                 ],
#                 "how_to_verify": [
#                     "Proxy Type이 'On-Premise'인 경우, Cloud Connector의 'Access Control' 탭 확인",
#                     "해당 URL 경로(Path)가 'Path and all sub-paths'로 허용되어 있는지 확인",
#                     "Cloud Connector 내에 정의된 Virtual Host와 Port가 Integration Suite의 어댑터 설정과 일치하는지 확인",
#                 ],
#             },
#         ],
#         "question_for_user": [
#             "실패한 시점의 정확한 대상 URL(마스킹 처리됨)은 무엇입니까?",
#             "최근에 대상 시스템(Receiver)의 API 구조나 엔드포인트 변경이 있었습니까?",
#             "Cloud Connector를 사용 중인 환경입니까?",
#         ],
#         "additional_data_needed": [
#             {
#                 "data": "Message Processing Log (Trace mode)",
#                 "reason": "런타임에 결정된 최종 URL과 헤더 값을 확인하여 동적 경로 생성 오류를 판별하기 위함",
#                 "how": "Monitoring > Manage Integration Content > 해당 iFlow 선택 > Log Level을 Trace로 변경 후 재실행",
#             },
#             {
#                 "data": "HTTP Response Body",
#                 "reason": "404 응답과 함께 대상 시스템에서 반환한 구체적인 에러 메시지가 있을 수 있음",
#                 "how": "Trace 모드에서 Receiver 어댑터 직후의 메시지 페이로드를 확인",
#             },
#         ],
#     },
#     "solution": {
#         "solutions": [
#             {
#                 "fix_plan": "호출 URL 경로 및 리소스 가용성 즉시 점검",
#                 "check_list": [
#                     {
#                         "target": "HTTP/OData Receiver Adapter 설정",
#                         "check_points": [
#                             "Address 필드에 입력된 URL 끝에 불필요한 슬래시(/)나 공백이 있는지 확인",
#                             "동적 헤더(CamelHttpPath, CamelHttpQuery)를 사용하여 경로를 생성하는 경우, 런타임에 값이 올바르게 생성되는지 확인",
#                         ],
#                         "expected": "Target 시스템의 API 명세서와 일치하는 URL 경로가 설정되어 있어야 함",
#                     },
#                     {
#                         "target": "Target 시스템(엔드포인트) 상태",
#                         "check_points": [
#                             "Postman이나 cURL을 사용하여 동일한 URL로 요청을 보냈을 때 404 응답이 발생하는지 확인",
#                             "대상 서버의 API 서비스가 활성화되어 있는지 및 배포 상태 확인",
#                         ],
#                         "expected": "외부 도구에서 정상 호출 시 iFlow의 동적 경로 생성 로직 문제로 판단 가능",
#                     },
#                 ],
#                 "prove_senario": (
#                     "iFlow를 Trace 모드로 변경한 후 다시 실행하여, Message Content의 'Log' 탭에서 "
#                     "실제 호출된 'CamelHttpAddress' 및 'CamelHttpPath'의 전체 문자열을 추출하여 "
#                     "브라우저나 테스트 도구에서 직접 호출해 봄."
#                 ),
#                 "prevention": (
#                     "1. 운영/개발 환경별 URL을 Externalized Parameters로 관리하여 환경 설정 오류 방지. "
#                     "2. URL 생성 로직 직전에 Groovy Script를 통해 최종 URL을 로그에 기록하도록 구현. "
#                     "3. Exception Subprocess를 추가하여 404 발생 시 상세 에러 메시지를 메일이나 모니터링 시스템으로 전송."
#                 ),
#                 "additional_data_needed": [
#                     {
#                         "data": "전체 호출 URL (Full Target URL)",
#                         "reason": "404 에러는 경로가 잘못된 것이므로 실제 어떤 주소로 요청이 나갔는지 알아야 오타나 누락된 경로를 식별할 수 있음",
#                         "how": "CPI 모니터링의 Trace 모드 활성화 후 HTTP Adapter 호출 직전의 Header/Property 확인",
#                     }
#                 ],
#             }
#         ]
#     },
# }


def fetch_analysis(artifact_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if not artifact_id:
        return None, "Artifact ID가 필요합니다."
    try:
        response: Response = post(
            uri="/api/analysis",
            body={"artifact_id": artifact_id},
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


def format_duration(start: Optional[str], end: Optional[str]) -> str:
    start_dt, end_dt = parse_datetime(start), parse_datetime(end)
    if not start_dt or not end_dt:
        return "-"
    delta = end_dt - start_dt
    seconds = delta.total_seconds()
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, remainder = divmod(int(seconds), 60)
    return f"{minutes}m {remainder}s"


def render_overview(payload: Dict[str, Any]):
    with st.container(border=True):
        st.subheader("Artifact Context")

        st.badge(payload.get("artifact_type"))
        meta_cols = st.columns([1, 1])
        meta_cols[0].text_input(label="Artifact Id", value=payload.get("artifact_id", "-"), disabled=False)
        meta_cols[1].text_input(label="Package Id", value=payload.get("package_id", "-"), disabled=False)
        meta_cols[0].text_input(label="Message GUID", value=payload.get("message_guid", "-"), disabled=False)

        st.divider()

        info_cols = st.columns([6, 1])
        info_cols[0].text_input(label="Exception", value=payload.get("exception", "-"), disabled=False)
        info_cols[1].caption("Status Code")
        info_cols[1].container().badge(str(payload.get("status_code", "-")), width="stretch", color="red")
        info_cols[1].caption("Duration")
        info_cols[1].badge(format_duration(payload.get("log_start", "-"), payload.get("log_end", "-")))
        time_cols = info_cols[0].columns([1, 1])
        time_cols[0].caption("Log Start")
        time_cols[0].badge(f"{format_datetime(payload.get('log_start'))}", color="green")
        time_cols[1].caption("Log End")
        time_cols[1].badge(f"{format_datetime(payload.get('log_end'))}", color="green")

        st.markdown("**Error Log**")
        st.code(payload.get("origin_log", ""), language="bash")


def render_analysis(analysis: Dict[str, Any]):
    with st.container(border=True):
        st.subheader("Analysis")
        st.markdown("**Summary**")
        st.markdown(f"{analysis.get('summary', '-')}")

        classification = analysis.get("classification") or {}
        class_cols = st.columns([1, 1])
        class_cols[0].markdown("**Classification**")
        class_cols[0].badge(classification.get("category", "-"), color="orange")
        class_cols[1].markdown("**Confidence**")
        class_cols[1].badge(f"{classification.get('confidence') * 100:.0f}%", color="blue")

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
                        st.write(f"- {item.get('data', '-')}: {item.get('reason', '-')}")
                        st.caption(f"  확보 방법: {item.get('how', '-')}")


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

payload: Dict[str, Any] = st.session_state.get("analysis_data", EXAMPLE_ANALYSIS)

incoming_artifact_id = st.session_state.get("artifact_id")
prefetched_for = st.session_state.get("_analysis_prefetched_artifact")

if incoming_artifact_id:
    artifact_from_state = str(incoming_artifact_id).strip()
    if artifact_from_state and artifact_from_state != prefetched_for:
        data, error = fetch_analysis(artifact_from_state)
        st.session_state["_analysis_prefetched_artifact"] = artifact_from_state
        if data:
            st.session_state["analysis_data"] = data
            payload = data
            st.success(f"전달된 artifact_id '{artifact_from_state}' 로 자동 조회했습니다.")
        else:
            st.error(f"전달된 artifact_id로 API 호출 실패: {error}")

artifact_default = (incoming_artifact_id or payload.get("artifact_id", "")) or ""
fetch_cols = st.columns([3, 1])
artifact_input = fetch_cols[0].text_input(label="Artifact ID", value=artifact_default, placeholder="예) INTEGRA_SCOPE_TEST")
fetch_cols[1].container(height=10, border=False)
fetch_clicked = fetch_cols[1].button("API 요청", type="primary", use_container_width=True)

if fetch_clicked:
    data, error = fetch_analysis(artifact_input.strip())
    if data:
        st.session_state["analysis_data"] = data
        st.session_state["_analysis_prefetched_artifact"] = artifact_input.strip()
        payload = data
        st.success("API 응답을 불러왔습니다.")
    else:
        st.error(f"API 요청 실패: {error}")

st.divider()

if not payload:
    st.info("분석 데이터를 불러와 주세요.")
    st.stop()

render_overview(payload)
render_analysis(payload.get("analysis") or {})
render_solutions(payload.get("solution") or {})

with st.expander("Raw payload 보기"):
    st.json(payload)
