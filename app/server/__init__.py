"""FastAPI application package for the SAP IS Error Analysis API."""
from starlette.requests import Request

API_NAME = "Integra Scope API"
API_VERSION = "1.0.0"


def _success_response(request: Request, payload: dict):
  request_id = getattr(request.state, "request_id", None)
  if request_id:
    payload = {**payload, "request_id": request_id}
  return payload
