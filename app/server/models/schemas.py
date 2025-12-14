"""
SAP Cloud Integration 메시지 처리 로그 응답을 다루기 위한 Pydantic 스키마.

OData 형태 응답 예시:
{
  "d": {
    "results": [
      {
        "__metadata": {...},
        "MessageGuid": "af1c...",
        "CorrelationId": "corr-123",
        "ApplicationMessageId": "APP-1",
        "ApplicationMessageType": "INVOICE",
        "IntegrationArtifact": "DemoIFlow",
        "LogStart": "/Date(1701380100000+0000)/",
        "LogEnd": "/Date(1701380120000+0000)/",
        "Status": "FAILED",
        "Sender": "SENDER_SYS",
        "Receiver": "RECEIVER_SYS",
        "LogLevel": "INFO"
      }
    ]
  }
}
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

_SAP_DATE_RE = re.compile(r"/Date\((?P<millis>-?\d+)(?P<offset>[+-]\d{4})?\)/")


def parse_sap_datetime(raw: str) -> datetime:
  """/Date(밀리초+오프셋)/ 문자열을 UTC datetime으로 변환."""
  match = _SAP_DATE_RE.match(raw)
  if not match:
    raise ValueError(f"Unexpected SAP date format: {raw}")

  millis = int(match.group("millis"))
  offset = match.group("offset")

  tzinfo: timezone = timezone.utc
  if offset:
    sign = 1 if offset.startswith("+") else -1
    hours = int(offset[1:3])
    minutes = int(offset[3:5])
    tzinfo = timezone(sign * timedelta(hours=hours, minutes=minutes))

  # SAP 타임스탬프는 UTC 기준 밀리초
  return datetime.fromtimestamp(millis / 1000, tz=tzinfo).astimezone(
    timezone.utc)


class ErrorType(str, Enum):
  NETWORK = 0,
  FIREWALL = 1,
  MAPPING = 2,
  DATABASE = 3,
  AUTHENTICATION = 4,


class ErrorAnalysisResponse(BaseModel):
  """내부 API 응답 래퍼."""

  log: str = Field(..., description="오류 로그")
  type: ErrorType = Field(..., description="오류 유형")
  cause: str = Field(..., description="오류 원인")
  solution: str = Field(..., description="해결방법")
  meta: Optional[dict] = Field(default=None, description="추가 메타데이터")


class MplLog(BaseModel):
  """Message Processing Log 단건."""

  message_guid: str = Field(..., alias="MessageGuid")
  correlation_id: Optional[str] = Field(None, alias="CorrelationId")
  application_message_id: Optional[str] = Field(None,
                                                alias="ApplicationMessageId")
  application_message_type: Optional[str] = Field(None,
                                                  alias="ApplicationMessageType")
  integration_artifact: Optional[str] = Field(None, alias="IntegrationArtifact")
  status: str = Field(..., alias="Status")
  log_level: Optional[str] = Field(None, alias="LogLevel")
  sender: Optional[str] = Field(None, alias="Sender")
  receiver: Optional[str] = Field(None, alias="Receiver")
  log_start: datetime = Field(..., alias="LogStart")
  log_end: Optional[datetime] = Field(None, alias="LogEnd")

  @field_validator("log_start", "log_end", mode="before")
  @classmethod
  def _convert_sap_date(cls, value):
    if value is None:
      return None
    if isinstance(value, str) and value.startswith("/Date("):
      return parse_sap_datetime(value)
    return value


class MplResultSet(BaseModel):
  """OData 'd' 키 아래 results 배열을 담는 컨테이너."""

  results: List[MplLog] = Field(default_factory=list)


class MplResponse(BaseModel):
  """SAP Cloud Integration 로그 목록 응답."""

  d: MplResultSet
