import os
from typing import List


def allowed_origins() -> List[str]:
    """Return CORS origins, defaulting to Streamlit dev URLs."""
    env_origins = os.getenv("CORS_ORIGINS")
    if env_origins:
        origins = [
            origin.strip() for origin in env_origins.split(",") if origin.strip()
        ]
        return origins or ["*"]

    return [
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ]


def allowed_methods() -> List[str]:
    return ["*"]


def allowed_headers() -> List[str]:
    return ["*"]
