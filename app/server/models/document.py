class Document:
  def __init__(self, status_code: int, log: str, exc_name: str):
    self.status_code = f"HTTP_STATUS={status_code}"
    self.log = f"LOG={log}"
    self.exc_name = f"EXCEPTION={exc_name}"

  def __str__(self) -> str:
    if self.status_code:
      return f"{self.status_code}\n{self.exc_name}\n{self.log}".strip()
    return f"{self.exc_name}\n{self.log}".strip()
