"""
SAP Cloud Integration 메시지 처리 로그 응답을 다루기 위한 Pydantic 스키마.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

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


class MessageProcessingLogDto(BaseModel):
  """내부 API 응답 래퍼."""

  message_guid: str = Field(..., description="message guid")
  correlation_id: str = Field(..., description="correlation id")
  artifact_id: str = Field(..., description="Artifact Id")
  artifact_name: str = Field(..., description="Artifact Name")
  artifact_type: str = Field(..., description="Artifact Type")
  package_id: str = Field(..., description="Package Id")
  package_name: str = Field(..., description="Package Name")


class Metadata(BaseModel):
  """OData __metadata 블록."""

  model_config = ConfigDict(extra="ignore")

  id: Optional[str] = Field(None, alias="id")
  uri: Optional[str] = Field(None, alias="uri")
  type: Optional[str] = Field(None, alias="type")


class DeferredLink(BaseModel):
  """__deferred 객체."""

  model_config = ConfigDict(extra="ignore")

  uri: str = Field(..., alias="uri")


class DeferredResource(BaseModel):
  """연관 리소스의 지연 로딩 링크."""

  model_config = ConfigDict(populate_by_name=True)

  deferred: DeferredLink = Field(..., alias="__deferred")


class IntegrationArtifact(BaseModel):
  """통합 플로우 정보."""

  model_config = ConfigDict(populate_by_name=True)

  metadata: Optional[Metadata] = Field(None, alias="__metadata")
  id: str = Field(..., alias="Id")
  name: str = Field(..., alias="Name")
  type: str = Field(..., alias="Type")
  package_id: str = Field(..., alias="PackageId")
  package_name: str = Field(..., alias="PackageName")
  status: str = Field(..., alias="Status")


class MessageProcessingLog(BaseModel):
  """Message Processing Log 단건."""

  model_config = ConfigDict(populate_by_name=True)

  metadata: Optional[Metadata] = Field(None, alias="__metadata")
  message_guid: str = Field(..., alias="MessageGuid")
  correlation_id: Optional[str] = Field(None, alias="CorrelationId")
  application_message_id: Optional[str] = Field(None,
                                                alias="ApplicationMessageId")
  predecessor_message_guid: Optional[str] = Field(None,
                                                  alias="PredecessorMessageGuid")
  application_message_type: Optional[str] = Field(None,
                                                  alias="ApplicationMessageType")
  log_start: Optional[datetime] = Field(None, alias="LogStart")
  log_end: Optional[datetime] = Field(None, alias="LogEnd")
  sender: Optional[str] = Field(None, alias="Sender")
  receiver: Optional[str] = Field(None, alias="Receiver")
  integration_flow_name: Optional[str] = Field(None,
                                               alias="IntegrationFlowName")
  status: str = Field(..., alias="Status")
  alternate_web_link: Optional[str] = Field(None, alias="AlternateWebLink")
  integration_artifact: Optional[IntegrationArtifact] = Field(
      None, alias="IntegrationArtifact")
  log_level: Optional[str] = Field(None, alias="LogLevel")
  custom_status: Optional[str] = Field(None, alias="CustomStatus")
  archiving_status: Optional[str] = Field(None, alias="ArchivingStatus")
  archiving_sender_channel_messages: Optional[bool] = Field(
      None, alias="ArchivingSenderChannelMessages")
  archiving_receiver_channel_messages: Optional[bool] = Field(
      None, alias="ArchivingReceiverChannelMessages")
  archiving_log_attachments: Optional[bool] = Field(
      None, alias="ArchivingLogAttachments")
  archiving_persisted_messages: Optional[bool] = Field(
      None, alias="ArchivingPersistedMessages")
  transaction_id: Optional[str] = Field(None, alias="TransactionId")
  previous_component_name: Optional[str] = Field(None,
                                                 alias="PreviousComponentName")
  local_component_name: Optional[str] = Field(None, alias="LocalComponentName")
  origin_component_name: Optional[str] = Field(None,
                                               alias="OriginComponentName")
  custom_header_properties: Optional[DeferredResource] = Field(
      None, alias="CustomHeaderProperties")
  message_store_entries: Optional[DeferredResource] = Field(
      None, alias="MessageStoreEntries")
  error_information: Optional[DeferredResource] = Field(None,
                                                        alias="ErrorInformation")
  adapter_attributes: Optional[DeferredResource] = Field(None,
                                                         alias="AdapterAttributes")
  attachments: Optional[DeferredResource] = Field(None, alias="Attachments")
  runs: Optional[DeferredResource] = Field(None, alias="Runs")

  @field_validator("log_start", "log_end", mode="before")
  def _parse_sap_dates(cls, value):
    if value is None or isinstance(value, datetime):
      return value
    return parse_sap_datetime(value)


class MplResultSet(BaseModel):
  """OData 'd' 키 아래 results 배열을 담는 컨테이너."""

  model_config = ConfigDict(populate_by_name=True)

  count: Optional[str] = Field(None, alias="__count")
  results: List[MessageProcessingLog] = Field(default_factory=list)


class MplResponse(BaseModel):
  """SAP Cloud Integration 로그 목록 응답."""

  model_config = ConfigDict(populate_by_name=True)

  d: MplResultSet
