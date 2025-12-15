import re
from typing import Optional, List


class RegulationService:
  """MPL 응답을 Vector DB에 저장하기 위한 정규화 기능"""

  _URL_RE = re.compile(r"https?://[^\s'\"<>]+", re.IGNORECASE)
  _MPL_RE = re.compile(r"\bMPL\b.*?:\s*([A-Za-z0-9_\-]+)", re.IGNORECASE)
  _STATUS_RE = re.compile(r"\bstatusCode\s*[:=]\s*(\d{3}\b)", re.IGNORECASE)

  def _extract_first_url(self, text: str) -> Optional[str]:
    m = self._URL_RE.search(text or "")
    return m.group(0) if m else None

  def _mask_urls(self, text: str) -> str:
    return self._URL_RE.sub("<URL>", text)

  def _extract_mpl_id(self, text: str) -> Optional[str]:
    m = self._MPL_RE.search(text or "")
    return m.group(1) if m else None

  def _strip_mpl_line(self, text: str) -> str:
    lines = (text or "").splitlines()
    kept: List[str] = []
    for line in lines:
      if re.search(r"\bMPL ID\b", line, re.IGNORECASE):
        continue
      kept.append(line)
    return "\n".join(kept).strip()

  def _extract_http_status(self, text: str) -> Optional[int]:
    m = self._STATUS_RE.search(text or "")
    if not m:
      return None
    try:
      return int(m.group(1))
    except ValueError:
      return None

  def _extract_exception_name(self, text: str) -> Optional[str]:
    first_line = (text or "").splitlines()[0] if (
        text or "").splitlines() else ""
    if ":" in first_line:
      head = first_line.split(":", 1)[0].strip()
    else:
      head = first_line.strip()

    if "." in head:
      head = head.split(".")[-1]
    return head or None

  def _classify_error_type(self, text: str,
      http_status: Optional[int] = None) -> str:
    t = (text or "").lower()

    if http_status is not None:
      if http_status == 401 or http_status == 403:
        return "AUTH_ERROR"
      if http_status == 404:
        return "NOT_FOUND"
      if http_status == 408:
        return "TIMEOUT"
      if 500 <= http_status <= 599:
        return "SERVER_ERROR"

    if "timeout" in t or "timed out" in t or "read timed out" in t:
      return "TIMEOUT"
    if "connection refused" in t or "connection reset" in t:
      return "NETWORK_ERROR"
    if "ssl" in t or "handshake" in t or "certificate" in t:
      return "TLS_ERROR"
    if "unauthorized" in t or "forbidden" in t or "authentication" in t:
      return "AUTH_ERROR"
    if "not found" in t:
      return "NOT_FOUND"
    if "mapping" in t or "xsl" in t or "xslt" in t:
      return "MAPPING_ERROR"
    if "validation" in t or "schema" in t:
      return "VALIDATION_ERROR"
    if "nullpointerexception" in t:
      return "NPE"
    return "UNKNOWN"

  def build_document_from_log(self,
      log: str = "",
      http_status: Optional[int] = None) -> str:
    no_mpl = self._strip_mpl_line(log)
    masked = self._mask_urls(no_mpl)
    exc_name = self._extract_exception_name(masked)
    body = "\n".join([ln.strip for ln in masked.splitlines() if ln.strip()])
    head = f"HTTP_STATUS={http_status}"
    lead = f"EXCEPTION={exc_name or 'Error'}"

    if head:
      return f"{head}\n{lead}\n{body}".strip()
    return f"{lead}\n{body}".strip()
