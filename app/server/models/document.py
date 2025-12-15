class Document:
  def __init__(self, head, body, lead):
    self.head = f"HTTP_STATUS={head}"
    self.body = f"LOG={body}"
    self.lead = f"EXCEPTION={lead}"

  def __str__(self) -> str:
    if self.head:
      return f"{self.head}\n{self.lead}\n{self.body}".strip()
    return f"{self.lead}\n{self.body}".strip()
