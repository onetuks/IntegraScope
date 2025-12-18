from pydantic import BaseModel


class AnalysisOut(BaseModel):
    summary: str
