from pathlib import Path
from typing import Dict, Optional

import streamlit as st


# Optional overrides for sidebar labels (keyed by filename stem)
CUSTOM_PAGE_LABELS = {
    "test_analysis": "Test Execution",
}


def _get_page_routes() -> Dict[str, str]:
    """Return display labels mapped to Streamlit page file paths."""
    pages_dir = Path(__file__).parent / "pages"
    routes: Dict[str, str] = {}
    for page_path in sorted(pages_dir.glob("*.py")):
        stem = page_path.stem
        label = CUSTOM_PAGE_LABELS.get(stem,
                                       stem.replace("_", " ").title())
        routes[label] = f"pages/{page_path.name}"
    return routes


PAGE_ROUTES = _get_page_routes()


def hide_sidebar_nav():
    """Hide Streamlit's built-in multi-page sidebar navigation."""
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_nav(current_page: Optional[str] = None):
    """
    Render a custom sidebar radio navigation and switch pages when changed.

    If current_page is None, a placeholder is shown so the first option
    is not auto-selected.
    """
    if not PAGE_ROUTES:
        return

    st.sidebar.title("Menu")

    options = list(PAGE_ROUTES.keys())
    if current_page is None:
        index = None
    else:
        index = options.index(current_page) if current_page in options else 0

    selection = st.sidebar.radio(label="", options=options, index=index)

    if selection == current_page:
        return

    st.switch_page(PAGE_ROUTES[selection])
