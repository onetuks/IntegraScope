import re

from typing import Optional, List

from pydantic import BaseModel


class ErrorLogRegulationDto(BaseModel):
    status_code: Optional[int]
    exception: str
    normalized_log: str
    origin_log: str


class ErrorLogRegulationComponent:
    """MPL 응답을 Vector DB에 저장하기 위한 정규화 기능"""

    _URL_RE = re.compile(r"https?://[^\s'\"<>]+", re.IGNORECASE)
    _MPL_RE = re.compile(r"\bMPL\b.*?:\s*([A-Za-z0-9_\-]+)", re.IGNORECASE)
    _STATUS_RE = re.compile(r"\bstatusCode\s*[:=]\s*(\d{3}\b)", re.IGNORECASE)

    def _mask_urls(self, text: str) -> str:
        return self._URL_RE.sub("<URL>", text)

    def _extract_mpl_id(self, text: str) -> Optional[str]:
        m = self._MPL_RE.search(text or "")
        return m.group(1) if m else None

    def _extract_status_code(self, text: str) -> Optional[int]:
        m = self._STATUS_RE.search(text or "")
        if not m:
            return None
        try:
            return int(m.group(1))
        except ValueError:
            return None

    @staticmethod
    def _strip_mpl_line(text: str) -> str:
        lines = (text or "").splitlines()
        kept: List[str] = []
        for line in lines:
            if re.search(r"\bMPL ID\b", line, re.IGNORECASE):
                continue
            kept.append(line)
        return "\n".join(kept).strip()

    @staticmethod
    def _extract_exception(text: str) -> Optional[str]:
        first_line = text.splitlines()[0]
        if ":" not in first_line:
            return None
        return first_line.split(":")[0].strip()

    def normalize_log(self, raw_log: str) -> ErrorLogRegulationDto:
        if raw_log is None or raw_log.strip() == "":
            raise ValueError("log is empty")

        status_code = self._extract_status_code(raw_log)
        no_mpl = self._strip_mpl_line(raw_log).strip()
        masked = self._mask_urls(no_mpl)
        cleaned_lines = [
            ln.strip() for ln in masked.splitlines() if ln.strip()
        ]
        normalized_log = "\n".join(cleaned_lines)
        exception = self._extract_exception(normalized_log)

        return ErrorLogRegulationDto(
            status_code=status_code,
            exception=exception,
            normalized_log=normalized_log,
            origin_log=no_mpl
        )
